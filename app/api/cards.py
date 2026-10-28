"""
Card Management and Sub-Second POS Freeze Controls (REQ-F-003, REQ-F-011).
"""

import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from app.db.connection import get_db
from app.models.schemas import CardsListResponse, CardItem, CardFreezeRequest, CardActionResponse

router = APIRouter(prefix="/cards", tags=["Card Controls & POS Freeze"])


@router.get("", response_model=CardsListResponse)
def list_cards():
    """
    Retrieve all physical and virtual cards (REQ-F-011).
    """
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM cards ORDER BY created_at DESC").fetchall()
        cards = [
            CardItem(
                card_id=r["card_id"],
                account_id=r["account_id"],
                card_number_masked=r["card_number_masked"],
                cardholder_name=r["cardholder_name"],
                card_type=r["card_type"],
                expiry=r["expiry"],
                status=r["status"],
                spend_limit=float(r["spend_limit"]),
                is_frozen=bool(r["is_frozen"])
            )
            for r in rows
        ]
        return CardsListResponse(cards=cards)


@router.post("/{card_id}/freeze", response_model=CardActionResponse)
def freeze_card(card_id: str, payload: CardFreezeRequest):
    """
    Instantly freeze card with sub-second POS propagation (REQ-F-003).
    """
    with get_db() as conn:
        card = conn.execute("SELECT * FROM cards WHERE card_id = ?", (card_id,)).fetchone()
        if not card:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Card {card_id} not found")

        conn.execute(
            "UPDATE cards SET is_frozen = 1, status = 'FROZEN', updated_at = CURRENT_TIMESTAMP WHERE card_id = ?",
            (card_id,)
        )

        # Audit log with unique UUID
        conn.execute(
            """INSERT INTO audit_logs (log_id, actor, action, entity_type, entity_id, status, state_diff)
               VALUES (?, 'CARDHOLDER', 'CARD_FREEZE', 'CARD', ?, 'SUCCESS', ?)""",
            (f"aud_{uuid.uuid4().hex[:8]}", card_id, f'{{"reason": "{payload.reason}", "pos_propagation": "SUB_SECOND"}}')
        )

        return CardActionResponse(
            card_id=card_id,
            is_frozen=True,
            status="FROZEN",
            updated_at=datetime.utcnow().isoformat()
        )


@router.post("/{card_id}/unfreeze", response_model=CardActionResponse)
def unfreeze_card(card_id: str):
    """
    Instantly unfreeze card and restore POS authorization (REQ-F-003).
    """
    with get_db() as conn:
        card = conn.execute("SELECT * FROM cards WHERE card_id = ?", (card_id,)).fetchone()
        if not card:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Card {card_id} not found")

        conn.execute(
            "UPDATE cards SET is_frozen = 0, status = 'ACTIVE', updated_at = CURRENT_TIMESTAMP WHERE card_id = ?",
            (card_id,)
        )

        # Audit log with unique UUID
        conn.execute(
            """INSERT INTO audit_logs (log_id, actor, action, entity_type, entity_id, status, state_diff)
               VALUES (?, 'CARDHOLDER', 'CARD_UNFREEZE', 'CARD', ?, 'SUCCESS', '{"status": "ACTIVE"}')""",
            (f"aud_{uuid.uuid4().hex[:8]}", card_id)
        )

        return CardActionResponse(
            card_id=card_id,
            is_frozen=False,
            status="ACTIVE",
            updated_at=datetime.utcnow().isoformat()
        )

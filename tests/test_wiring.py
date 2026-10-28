"""
Full-Stack Cross-Tier Wiring Verification Tests.
"""

from pathlib import Path


def test_api_js_script_tag_injected_in_pages():
    """Verify that all HTML views import /js/api.js for dynamic full-stack wiring."""
    public_dir = Path("public/pages")
    if not public_dir.exists():
        public_dir = Path(".jtc/ARCH-5784/cloned_repo/public/pages")

    html_files = list(public_dir.glob("*.html"))
    assert len(
        html_files) >= 10, f"Expected at least 10 HTML views, found {len(html_files)}"

    for html_file in html_files:
        content = html_file.read_text(encoding="utf-8")
        assert "/js/api.js" in content or "api.js" in content, f"{html_file.name} is missing client API script import."
        assert "/js/app.js" in content or "app.js" in content, f"{html_file.name} is missing interactive app script import."

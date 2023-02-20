def test_about(template_dir):
    assert "ABOUT!" == (template_dir / "pages" / "about.html").read_text()

def test_request(template_dir):
    assert "request" == (template_dir / "pages" / "request.html").read_text()

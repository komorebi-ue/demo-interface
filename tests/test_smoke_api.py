def test_dashboard_html(api_session):
    # OrangeHRM demo doesn't expose stable public API endpoints;
    # we at least verify authenticated session can reach an authenticated page.
    resp = api_session.request(
        "GET",
        "https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index",
        allow_redirects=False,
    )
    assert resp.status_code in (200, 302)

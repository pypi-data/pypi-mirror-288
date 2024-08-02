from codialog import create_app

def test_home_page():
    app = create_app()
    client = app.test_client()

    response = client.get('/')
    assert response.status_code == 200
    assert b"Hello, Flask!" in response.data
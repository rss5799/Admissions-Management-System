#System test 24:  Assert app is created
def test_creating_app():
    from app import create_app
    app = create_app()
    
    assert app is not None
    assert hasattr(app, 'secret_key')
    assert app.secret_key is not None
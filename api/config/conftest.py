import pytest

from config import app, db, Base, settings


@pytest.fixture
def client():
    app.config['DEBUG'] = False
    app.config['TESTING'] = True
    app.config['DATABASE_URI'] = settings.TEST_DATABASE_URI

    with app.test_client() as client:
        with app.app_context():
            db.init_app(app, Base)
            db.create_all()

        yield client
        
        db.Session.commit()
        db.drop_all()

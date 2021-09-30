from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class SQLAlchemy(object):
    def __init__(self):
        self.app = None
        self.Session = None
        self.Base = None

    def init_app(self, app, model_class):
        self.app = app
        self.Base = model_class
        self.engine = create_engine(self.app.config.get(
            "DATABASE_URI"), pool_pre_ping=True)
        self.Session = scoped_session(self.create_session())

        @app.teardown_appcontext
        def remove_session(response):
            self.Session.remove()
            return response

    def create_session(self):
        if not (self.app.config.get("DATABASE_URI")):
            raise RuntimeError("DATABASE_URI needs to be set.")
        else:
            return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def create_all(self):
        self.Base.metadata.create_all(bind=self.engine, checkfirst=True)

    def drop_all(self):
        self.Base.metadata.drop_all(bind=self.engine, checkfirst=True)

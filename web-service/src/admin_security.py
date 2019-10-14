from app import app
from flask_admin import Admin
from models import AdminView, HomeAdminView, User, Role
from flask_security import MongoEngineUserDatastore, Security
from services.db_service import getMongo

USER_DATASTORE = None


def get_datastore():
    return USER_DATASTORE


def create_admin():
    admin = Admin(app, 'RP', url='/', index_view=HomeAdminView(name='Home'))
    admin.add_view(AdminView(User))

    global  USER_DATASTORE
    USER_DATASTORE = MongoEngineUserDatastore(getMongo(), User, Role)
    security = Security(app, USER_DATASTORE)

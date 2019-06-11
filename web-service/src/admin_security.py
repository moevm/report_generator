from app import app
from flask_admin import Admin
from models import AdminView, HomeAdminView, User, Role
from flask_security import MongoEngineUserDatastore, Security
from db_service import getMongo

db = getMongo()

admin = Admin(app, 'RP', url='/', index_view=HomeAdminView(name='Home'))
admin.add_view(AdminView(User))


user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)

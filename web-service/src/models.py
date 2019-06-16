from db_service import getMongo
from flask_security import current_user, UserMixin, RoleMixin
from flask_admin import AdminIndexView
from flask_admin.contrib.mongoengine import ModelView
from flask import redirect, url_for, request
db = getMongo()


class Role(db.Document, RoleMixin):
	name = db.StringField(max_length=80, unique=True)

	def __unicode__(self):
		return self.name


class User(db.Document, UserMixin):
	username = db.StringField(max_length=50, required=True, unique=True)
	email = db.StringField(max_length=100, required=True, unique=True)
	password = db.StringField(max_length=100, required=True)
	github_access_token = db.StringField()
	active = db.BooleanField(default=True)
	roles = db.ListField(db.ReferenceField(Role), default=[])

	def __repr__(self):
		return '<User %r>' % self.username

	def __unicode__(self):
		return str(self.username)


class AdminMixin:

	def is_accessible(self):
		return current_user.has_role('admin')

	def inaccessible_callback(self, name, **kwargs):
		return redirect(url_for('security.login', next=request.url))


class AdminView(AdminMixin, ModelView):
	pass


class HomeAdminView(AdminMixin, AdminIndexView):
	pass

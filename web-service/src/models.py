from app import app
from services.db_service import getMongo
from flask_security import current_user, UserMixin, RoleMixin
from flask_admin import AdminIndexView
from flask_admin.contrib.mongoengine import ModelView
from flask import redirect, url_for, request
from mongoengine import signals
from mail import Mail

ADMIN = 'admin'
GITHUB_LOGIN = 'github_login'
ROLES = 'roles'
EMAIL = 'email'
IS_NEW_USER = 'was_new_user'
LOG_FAIL_EMAIL = 'Cant send to {}'


class Role(getMongo().Document, RoleMixin):
	name = getMongo().StringField(max_length=80, unique=True)

	def __unicode__(self):
		return self.name

	def __repr__(self):
		return self.name


class User(getMongo().Document, UserMixin):
	model = getMongo()
	username = model.StringField(max_length=50, required=True, unique=True)
	email = model.StringField(max_length=100, required=True, unique=True)
	active = model.BooleanField(default=True)
	roles = model.ListField(model.ReferenceField(Role), default=[])
	avatar = model.StringField()

	def __repr__(self):
		return self.email

	def __unicode__(self):
		return str(self.username)

	@classmethod
	def post_save(cls, sender, document, **kwargs):
		if app.config[IS_NEW_USER]:
			_mail = Mail()
			user = list(User.objects)[-1]

			if ADMIN not in user[ROLES]:
				try:
					_mail.send_message(user[EMAIL])
				except Exception:
					print(LOG_FAIL_EMAIL.format(user[EMAIL]))
		else:
			app.config[IS_NEW_USER] = True


signals.post_save.connect(User.post_save, sender=User)


class AdminMixin:

	def is_accessible(self):
		return current_user.has_role(ADMIN)

	def inaccessible_callback(self, name, **kwargs):
		return redirect(url_for(GITHUB_LOGIN, next=request.url))


class AdminView(AdminMixin, ModelView):
	pass


class HomeAdminView(AdminMixin, AdminIndexView):
	pass

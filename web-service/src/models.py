from app import app
from services.db_service import getMongo
from flask_security import current_user, UserMixin, RoleMixin
from flask_admin import AdminIndexView
from flask_admin.contrib.mongoengine import ModelView
from flask import redirect, url_for, request
from mongoengine import signals
from mail import Mail


class Role(getMongo().Document, RoleMixin):
	name = getMongo().StringField(max_length=80, unique=True)

	def __unicode__(self):
		return self.name

	def __repr__(self):
		return self.name


class User(getMongo().Document, UserMixin):
	username = getMongo().StringField(max_length=50, required=True, unique=True)
	email = getMongo().StringField(max_length=100, required=True, unique=True)
	active = getMongo().BooleanField(default=True)
	roles = getMongo().ListField(getMongo().ReferenceField(Role), default=[])
	avatar = getMongo().StringField()

	def __repr__(self):
		return self.email

	def __unicode__(self):
		return str(self.username)

	@classmethod
	def post_save(cls, sender, document, **kwargs):
		if app.config['was_new_user']:
			_mail = Mail()
			user = list(User.objects)[-1]

			if 'admin' not in user['roles']:
				try:
					_mail.send_message(user['email'])
				except Exception:
					print('Cant send to {}'.format(user['email']))
		else:
			app.config['was_new_user'] = True


signals.post_save.connect(User.post_save, sender=User)


class AdminMixin:

	def is_accessible(self):
		return current_user.has_role('admin')

	def inaccessible_callback(self, name, **kwargs):
		return redirect(url_for('github_login', next=request.url))


class AdminView(AdminMixin, ModelView):
	pass


class HomeAdminView(AdminMixin, AdminIndexView):
	pass

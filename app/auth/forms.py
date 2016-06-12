#coding=utf-8
######################################################
#
#Author:          whytin
#Email:           whytin@yeah.net
#QQ:              583501947
#
#Filename:        forms.py
#Last modified:   2016-06-05 13:55
#Description:     
#
######################################################

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(Form):
	email = StringField('邮箱', validators=[Required(), Length(1,64), Email()])
	password = PasswordField('密码', validators=[Required()])
	remember_me = BooleanField('记住我')
	submit = SubmitField('登录')

class RegistrationForm(Form):
	email = StringField('邮箱', validators=[Required(), Length(1,64), Email()])
	username = StringField('用户名', validators=[Required(), Length(1,64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'用户名只能用字母,''数字或者下划线')])
	password = PasswordField('密码', validators=[Required(), EqualTo('password2', message='两次密码必须一致')])
	password2 = PasswordField('确认密码', validators=[Required()])
	submit = SubmitField('注册')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('邮箱已被注册')
	
	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('用户已存在')

class ChangePasswordForm(Form):
	old_password = PasswordField('旧的密码', validators=[Required()])
	password = PasswordField('新的密码', validators=[Required(), EqualTo('password2', message='两次密码必须一致')])
	password2 = PasswordField('确认密码', validators=[Required()])
	submit = SubmitField('更改密码')

class PasswordResetRequestForm(Form):
	email = StringField('邮箱', validators=[Required(), Length(1,64),Email()])
	submit = SubmitField('重置密码')

class PasswordResetForm(Form):
	email = StringField('邮箱', validators=[Required(), Length(1,64), Email()])
	password = PasswordField('新的密码', validators=[Required(),EqualTo('password2', message='两次密码必须一致')])
	password2 = PasswordField('确认密码', validators=[Required()])
	submit = SubmitField('重置密码')
	
	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first() is None:
			raise ValidationError('不存在该邮箱')

class ChangeEmailForm(Form):
	email = StringField('新的邮箱', validators=[Required(), Length(1,64), Email()])
	password = PasswordField('密码', validators=[Required()])
	submit = SubmitField('更改邮箱')
	
	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('你的邮箱地址已更改')

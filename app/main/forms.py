#coding=utf-8
######################################################
#
#Author:          whytin
#Email:           whytin@yeah.net
#QQ:              583501947
#
#Filename:        forms.py
#Last modified:   2016-06-10 14:34
#Description:     
#
######################################################

from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Role, User, Post, Comment
from flask.ext.pagedown.fields import PageDownField


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


class EditProfileForm(Form):
    name = StringField('昵称', validators=[Length(0, 64)])
    location = StringField('地区', validators=[Length(0, 64)])
    about_me = TextAreaField('关于我')
    submit = SubmitField('提交')


class EditProfileAdminForm(Form):
    email = StringField('电子邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField('用户名', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('角色', coerce=int)
    name = StringField('昵称', validators=[Length(0, 64)])
    location = StringField('地区', validators=[Length(0, 64)])
    about_me = TextAreaField('关于我')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('你的邮箱已被注册')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已被使用')

class PostForm(Form):
	title = StringField("标题", validators=[Required(), Length(0,64)])
	body = PageDownField("内容", validators=[Required()])
	submit = SubmitField('提交')


class CommentForm(Form):
	body = StringField('你的看法', validators=[Required()])
	submit = SubmitField('提交')

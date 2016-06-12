#coding=utf-8
######################################################
#
#Author:          whytin
#Email:           whytin@yeah.net
#QQ:              583501947
#
#Filename:        views.py
#Last modified:   2016-06-05 13:31
#Description:     
#
######################################################

from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User, Role, Permission
from ..email import send_email
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		flash('用户名或密码错误')
	return render_template('auth/login.html',form=form)


@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('您已成功退出当前帐号')
	return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(email=form.email.data,
				username=form.username.data,
				password=form.password.data)
		db.session.add(user)
		db.session.commit()
		token = user.generate_confirmation_token()
		send_email(user.email, '请确认你的账号', 'auth/email/confirm', user=user, token=token)
		flash('已向你的邮箱发出确认邮件，请在一小时内确认')
		return redirect(url_for('main.index'))
	return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		flash('已经确认你的邮箱，谢谢！')
	else:
		flash('无效或过期的链接')
	return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
	if current_user.is_authenticated:
		current_user.ping()
		if not current_user.confirmed and request.endpoint[:5] != 'auth.':
			return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('main.index'))
	return render_template('auth/unconfirmed.html')

@auth.route('/confirm')
@login_required
def resend_confirmation():
	token = current_user.generate_confirmation_token()
	send_email(current_user.email,'请确认你的帐号', 'auth/email/confirm', user=current_user, token=token)
	flash('已重新向你的邮箱发出确认邮件，请在一小时内确认')
	return redirect(url_for('main.index'))

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
	form = ChangePasswordForm()
	if form.validate_on_submit():
		if current_user.verify_password(form.old_password.data):
			current_user.password = form.password.data
			db.session.add(current_user)
			flash('密码更改成功')
			return redirect(url_for('main.index'))
		else:
			flash('密码错误')
	return render_template('auth/change_password.html', form=form)

@auth.route('/reset', methods=['GET','POST'])
def password_reset_request():
	if not current_user.is_anonymous:
		return redirect(url_for('main.index'))
	form = PasswordResetRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			token = user.generate_reset_token()
			send_email(user.email, '重置你的密码', 'auth/email/reset_password', user=user, token=token, next=request.args.get('next'))
		flash('已向你的邮箱发出确认重置密码的邮件，请在一小时内处理')
		return redirect(url_for('auth.login'))
	return render_template('auth/reset_password.html', form=form)

@auth.route('/reset/<token>', methods=['GET','POST'])
def password_reset(token):
	if not current_user.is_anonymous:
		return redirect(url_for('main.index'))
	form = PasswordResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is None:
			return redirect(url_for('main.index'))
		if user.reset_password(token, form.password.data):
			flash('你的密码重置成功')
			return redirect(url_for('auth.login'))
		else:
			return redirect(url_for('main.index'))
	return render_template('auth/reset_password.html', form=form)

@auth.route('/change-email', methods=['GET','POST'])
@login_required
def change_email_request():
	form = ChangeEmailForm()
	if form.validate_on_submit():
		if current_user.verify_password(form.password.data):
			new_email = form.email.data
			token = current_user.generate_email_change_token(new_email)
			send_email(new_email, '确认你的邮箱', 'auth/email/change_email', user=current_user, token=token)
			flash('已向你的邮箱发出确认新邮箱的邮件，请在一小时内处理')
			return redirect(url_for('main.index'))
		else:
			flash('错误的邮箱或者密码')
	return render_template('auth/change_email.html', form=form)

@auth.route('/change-email/<token>')
@login_required
def change_email(token):
	if current_user.change_email(token):
		flash('你的邮箱已重置成功')
	else:
		flash('错误的请求')
	return redirect(url_for('main.index'))


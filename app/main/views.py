#coding=utf-8
######################################################
#
#Author:          whytin
#Email:           whytin@yeah.net
#QQ:              583501947
#
#Filename:        views.py
#Last modified:   2016-06-05 11:50
#Description:     
#
######################################################

from flask import render_template, redirect, url_for, abort, flash, request, current_app
from flask.ext.login import login_required, current_user
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, PostForm, CommentForm
from .. import db
from ..models import Role, User, Post, Permission, Comment
from ..decorators import admin_required


@main.route('/')
def index():
	page = request.args.get('page', 1, type=int)
	pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
	posts = pagination.items 
	return render_template('index.html', posts=posts, pagination=pagination)
	


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@main.route('/post/<int:id>', methods=('GET', 'POST'))
def get_article(id):
	post = Post.query.get_or_404(id)
	form = CommentForm()
	if form.validate_on_submit():
		comment = Comment(body=form.body.data, post=post, author=current_user._get_current_object())
		db.session.add(comment)
		flash('评论已提交')
		return redirect(url_for('.get_article', id=post.id, page=-1))
	page = request.args.get('page', 1, type=int)
	if page == -1:
		page = (post.comments.count() - 1) / current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
	pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'], error_out=False)
	comments = pagination.items
	return render_template('article.html', post=post, form=form, comments=comments, pagination=pagination)

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
	post = Post.query.get_or_404(id)
	if current_user != post.author and not current_user.can(Permission.ADMINISTER):
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.body = form.body.data
		db.session.add(post)
		flash('重新发布成功')
		return redirect(url_for('.get_article', id=post.id))
	form.title.data = post.title
	form.body.data = post.body
	return render_template('edit_post.html', form=form)
		

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('你的资料修改成功')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-post', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, body=form.body.data, author=current_user._get_current_object())
		db.session.add(post)
		return redirect(url_for('.index'))
	return render_template('edit_post.html', form=form)

@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('你的资料修改成功')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


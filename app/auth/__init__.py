######################################################
#
#Author:          whytin
#Email:           whytin@yeah.net
#QQ:              583501947
#
#Filename:        __init__.py
#Last modified:   2016-06-05 13:30
#Description:     
#
######################################################

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views

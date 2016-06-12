######################################################
#
#Author:          whytin
#Email:           whytin@yeah.net
#QQ:              583501947
#
#Filename:        __init__.py
#Last modified:   2016-06-05 11:42
#Description:     
#
######################################################

from flask import Blueprint

main = Blueprint('main', __name__)


from . import views, error
from ..models import Permission

@main.app_context_processor
def inject_permission():
	return dict(Permission=Permission)

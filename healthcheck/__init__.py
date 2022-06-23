# -*- coding: utf-8 -*-

from collections import UserDict
from random import sample
from attr import has
from flask import Flask, flash, redirect
from flask_login import LoginManager

from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import datetime
from healthcheck.login import User

app = Flask(__name__)
app.debug = True
app.secret_key ='fg-ap-12HealthCheckerSCK'

#app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(minutes=1)


# flask -login
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(user_id):
    # 사용자 정보 조회
    user_info = User.get_user_info(user_id)
    # user_loader함수 반환값은 사용자 '객체'여야 한다.
    # 결과값이 dict이므로 객체를 새로 생성한다.
    login_info = User(user_id=user_info['data'][0])

    return login_info
    
# login_required로 요청된 기능에서 현재 사용자가 로그인되어 있지 않은 경우
# unauthorized 함수를 실행한다.
@login_manager.unauthorized_handler


def unauthorized():
    # 로그인되어 있지 않은 사용자일 경우 첫화면으로 이동
    flash("User needs to be logged in to view this page")
    return redirect("/login")


#print(error_list)


from .view.appLogin import *
from .view.appCheck import *
from .view.appSignup import *

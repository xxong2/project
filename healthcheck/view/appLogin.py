from healthcheck import app
from flask import render_template, redirect, request, jsonify, session, flash
from flask_login import login_user, logout_user, current_user
import hashlib
from healthcheck.login import User


@app.route('/login')
def login():
    return render_template("login.html", methods=['POST','GET'])


@app.route('/login/get_info', methods=['POST','GET'])
def login_get_info():
    user_id = request.form.get('userID')
    user_pw_re = request.form.get('userPW')
    
    user_pw = hashlib.sha256(user_pw_re.encode('utf-8')).hexdigest()
     
    if not user_id:
        return redirect('/relogin')

    # 사용자가 입력한 정보가 회원가입된 사용자인지 확인
    user_info = User.get_user_info(user_id, user_pw)
    

    if user_info['result'] != 'fail' and user_info['count'] != 0:
        # 사용자 객체 생성
        login_info = User(user_id=user_info['data'][0])
        print(login_info)
        # 사용자 객체를 session에 저장
        login_user(login_info, remember=True)
        session['userID'] = user_id
        session['logFlag'] = True
        
        return jsonify({'result': 'success',  'msg': 'Login Success!'})
    else:
        
        return redirect('/relogin')
        


# # 로그인 실패 시 재로그인
@app.route('/relogin')
def relogin():
    re_text = "로그인에 실패했습니다. 다시 시도해주세요."
    print(re_text)
    return render_template('login.html', login_result_text= re_text)


# 로그아웃
@app.route('/logout')
def logout():
    # session 정보를 삭제한다.
    logout_user()
    session.pop('userID',None)
    session['logFlag'] = False
    return redirect('/')

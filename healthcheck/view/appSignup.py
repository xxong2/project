from healthcheck import app
from flask import request, render_template, jsonify

from healthcheck.config import conn
from flask_login import login_required
import hashlib


@app.route('/usersignup' ,methods=['POST','GET'])
@login_required
def user_signup():
    # 회원가입
    
    if request.method =='GET':
        print("겟은 잘되었다")
        return render_template('usersignup.html')
           
    elif request.method=='POST':
        print("Post")
        user_id_receive = request.form['user_id_give']
        user_name_receive = request.form['user_name_give']
        user_name_pw_receive = request.form['user_pw_give']
        user_email_receive = request.form['user_email_give']
        # user_id_receive = request.form['Id']
        # user_name_receive = request.form['name']
        # user_name_pw_receive = request.form['pw']
        # user_email_receive = request.form['email']
                
        #암호화 
        user_name_pw = hashlib.sha256(user_name_pw_receive.encode('utf-8')).hexdigest()
                
        sql = "INSERT INTO hc_user (user_id,user_name,user_pw,user_email) VALUES (%s, %s, %s, %s);"
            
        cur = conn.cursor()
        cur.execute(sql,(user_id_receive,user_name_receive,user_name_pw,user_email_receive))
        print(sql)
        conn.commit()

        return jsonify({'result': 'success', 'msg': '저장이 완료되었습니다!'})
    
    #return render_template('usersignupnotused.html')

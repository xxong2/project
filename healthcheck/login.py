
from flask import flash, render_template, redirect, request, session, jsonify
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user
import hashlib
from healthcheck.config import conn



class User(UserMixin):
    
    def __init__(self, user_id):
        self.user_id = user_id
    
    def get_id(self):
        return str(self.user_id)
    
    @staticmethod
    def get_user_info(user_id, user_pw=None):
        result = dict()

        try:
            sql = ""
            sql += f"SELECT user_id, user_email "
            sql += f"FROM hc_user "
            if user_pw:
                sql += f"WHERE user_id = '{user_id}' AND user_pw = '{user_pw}'; "
            else:
                sql += f"WHERE user_id = '{user_id}'; "
            
            print("sql:",sql)
            cur = conn.cursor()
            cur.execute(sql)
            db_result = cur.fetchone()
            result['result'] = 'success'
            result['data'] = db_result
            result['count'] = len(result['data'])  
            
            cur.close()
            print(user_id,": ",result)
           
        except Exception:
            result['result'] = 'fail'
            result['data'] = Exception
            print(user_id,": ",result)
        finally:
            return result




 

def unauthorized():
    # 로그인되어 있지 않은 사용자일 경우 첫화면으로 이동
    flash("User needs to be logged in to view this page")
    return redirect("/login")

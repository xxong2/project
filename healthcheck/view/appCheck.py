
from flask import Flask, flash, redirect, request, render_template, jsonify, session, url_for
from healthcheck import app

import datetime

import requests
from healthcheck.config import proxies
from healthcheck.config import conn
from healthcheck.mailservice import MailService
from flask_login import login_required
import urllib3



headers= {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36"}
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@app.route('/')
def homepage():
    cur = conn.cursor()
    cur.execute('SELECT sites.site_owner, sites.site_dns, sites.owner_email, sites.site_status FROM sites ORDER BY site_id ASC')
    rows = cur.fetchall()
    cur.close()
        
    list =[]
    for row in rows:
        list.append(row)
        print('get methods',row,'\n')
        
        
    return render_template('index.html',sites = list)



@app.route('/index',methods=['GET', 'POST'])
def read_sites():
    if request.method =="GET":
        cur = conn.cursor()
        cur.execute('SELECT sites.site_owner, sites.site_dns, sites.owner_email, sites.site_status FROM sites ORDER BY site_id ASC')
        rows = cur.fetchall()
        cur.close()
        
        list =[]
        for row in rows:
            list.append(row)
            print('get methods', row,'\n')
        
        print("아주 잘되었다!! ")
        return jsonify({'result': 'success', 'sites': list})


    else:
        now = datetime.datetime.now()
        hs_id=now.strftime('%Y%m%d%H')
        cur = conn.cursor()
        sql= "SELECT sites.site_id FROM sites ORDER BY site_id ASC;"
        cur.execute(sql)
        seq = [r[0] for r in cur.fetchall()]
        
        
        flag =0 # 히스토리 테이블에 존재 여부 
        sql= "SELECT history_id FROM hc_history WHERE history_id='{history_id}';".format(history_id = hs_id)
        cur.execute(sql)
        lst = [r[0] for r in cur.fetchall()]
        if len(lst) != len(seq):
            flag = 1
        else:
            return jsonify({'result': 'success',  'msg': '이미 저장되었습니다.\n다음으로 오는 정각에 시도해주세요.'})
                
        error_list = []
        site_list = []
        error_Msg = []
        
        for i in range(0,len(seq)):
            
            sql= "SELECT sites.site_dns FROM sites WHERE sites.site_id = {s_id};".format(s_id = seq[i])
            cur.execute(sql)
            rows = [r[0] for r in cur.fetchall()]
            
            
            for link in rows:
                try:
                    re = requests.get(link, proxies=proxies, verify=False, headers=headers,timeout=15)
                    d = datetime.datetime.now()
                    #id 
                    if re.status_code / 100 == 2: 
                        status = re.status_code
                        sql = "UPDATE public.sites SET site_status='Success' WHERE site_id={s_id};".format(s_id = seq[i])
                        insert_sql ="INSERT INTO public.hc_history (history_id,sites_site_id,click_time,status_result) VALUES (%s, %s, %s, %s);"
                        
                        print(sql,"\n")
                        
                    elif re.status_code / 100 == 4: 
                        status = re.status_code
                        error_list.append (seq[i])
                        site_list.append (link)
                        error_Msg = "status"
                        sql = "UPDATE public.sites SET site_status='Fail' WHERE site_id={s_id};".format(s_id = seq[i])
                        insert_sql ="INSERT INTO public.hc_history (history_id,sites_site_id,click_time,status_result) VALUES (%s,%s, %s, %s);"
                        
                        
                    else: 
                        status = re.status_code
                        error_list.append (seq[i])
                        site_list.append (link)
                        error_Msg.append(status)
                        sql = "UPDATE public.sites SET site_status='Error' WHERE site_id={s_id};".format(s_id = seq[i])
                        insert_sql ="INSERT INTO public.hc_history (history_id,sites_site_id,click_time,status_result) VALUES (%s,%s, %s, %s);"
                        
                except Exception:
                    status = "Error"
                    error_list.append (seq[i])
                    site_list.append (link)
                    error_Msg.append( "Unknown Error")
                    d = datetime.datetime.now()
                    sql = "UPDATE public.sites SET site_status='Error' WHERE site_id={s_id};".format(s_id = seq[i])
                    insert_sql ="INSERT INTO public.hc_history (history_id,sites_site_id,click_time,status_result) VALUES (%s,%s, %s, %s);"
                        
                cur.execute(sql)
                conn.commit()
                
                if flag == 1:
                    cur.execute(insert_sql,(hs_id, seq[i], d, status))
                    conn.commit()
                
                
        # print(error_list)
        # print(site_list)
        # print(error_Msg)
        
        if len(error_list) != 0 :
            MailService(site_list, error_list, error_Msg)
        
        return jsonify({'result': 'success',  'msg': '저장이 완료되었습니다!'})




## HTML을 주는 부분
@app.route('/admin')
@login_required

def admin_home():
    return render_template('admin.html')



## API 역할을 하는 부분
@app.route('/review', methods=['POST'])
def write_review():
    site_owner_receive = request.form['site_owner_give']
    site_url_receive = request.form['site_url_give']
    owner_email_receive = request.form['owner_email_give']
    
    sql = "INSERT INTO public.sites (site_owner,site_dns,owner_email,site_status) VALUES (%s, %s, %s,%s);"
    cur = conn.cursor()
    cur.execute(sql,(site_owner_receive,site_url_receive,owner_email_receive,'NO DATA'))
    print(sql,(site_owner_receive,site_url_receive,owner_email_receive,'NO DATA'))
    conn.commit()

    return jsonify({'result': 'success', 'msg': '저장이 완료되었습니다!'})

@app.route('/review', methods=['GET'])
def read_reviews():
    cur = conn.cursor()
    
    cur.execute('SELECT site_owner,site_dns,owner_email FROM sites ORDER BY site_id ASC')
    rows = cur.fetchall()
    cur.close()
    
    list =[]
    for row in rows:
        list.append(row)
    return jsonify({'result': 'success', 'reviews': list})

@app.route('/delete', methods=['POST'])
def delete_review():
    site_url_receive = request.form['site_url_give']
    
    sql = "DELETE FROM public.sites WHERE site_dns = '%s';"
    cur = conn.cursor()
    cur.execute(sql % site_url_receive)
    print(sql)
    conn.commit()
    return jsonify({'result': 'success', 'msg': '저장이 완료되었습니다!'})

@app.route('/delete', methods=['GET'])
def delete_reviews():
    cur = conn.cursor()
    
    cur.execute('SELECT site_owner,site_dns,owner_email FROM sites ORDER BY site_id ASC')
    rows = cur.fetchall()
    cur.close()
    
    list =[]
    for row in rows:
        list.append(row)
    #print(list)
    return jsonify({'result': 'success', 'reviews': list})


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html", methods=['POST','GET'])





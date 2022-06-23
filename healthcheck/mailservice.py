from .config import conn
import smtplib
from email.mime.text import MIMEText


error_detail = "<TEST!!>\nPlease check out the <{site}> site!\nThere is an Error.\nType: {msg}"
sender = 'Cloud_Svc_DWH@bmw.co.kr'
port = 1025


def MailService(site_list, error_lst, error_Msg):
    if len(error_lst)!=0:
        
        for i in range(0,len(error_lst)):
            cur = conn.cursor()
    
            sql= "SELECT owner_email FROM sites WHERE site_id={s_id};".format(s_id = error_lst[i])
            cur.execute(sql)
            email_lst = [r[0] for r in cur.fetchall()]
            for email in email_lst:
                receivers = email
                msg =MIMEText(error_detail.format(site = site_list[i], msg = error_Msg[i])) 
                msg['Subject'] = '[Test mail] Error'
                msg['From'] = sender
                msg['To'] = receivers
                with smtplib.SMTP('mail.bmwgroup.net', 587) as server:
                    server.ehlo()
                    server.starttls()
                    server.login('PM84339@europe.bmw.corp', 'eogksalsrnrakstp-05')
                    server.sendmail(sender, receivers, msg.as_string())
                    print("Successfully sent email:", receivers)
                
        print("Success")

    else:
        print("There is no error")
        return 

#=====================================================================================

# sender = 'Cloud_Svc_DWH@bmw.co.kr'
# receivers = 'Jisong.ahn@bmw.co.kr'
 
# port = 1025
# msg = MIMEText('This is test mail')
# msg['Subject'] = 'Test mail'
# msg['From'] = sender
# msg['To'] = receivers
 
# with smtplib.SMTP('mail.bmwgroup.net', 587) as server:
#     server.ehlo()
#     server.starttls()
#     server.login('PM84339@europe.bmw.corp', 'eogksalsrnrakstp-05')
#     server.sendmail(sender, receivers, msg.as_string())
#     print("Successfully sent email")

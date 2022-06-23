from dotenv import load_dotenv
import os
import psycopg2 as pg2

load_dotenv()


if os.name == 'nt':
    q_id = 'qte0538'
    q_password= os.environ.get('QPASSWORD')

    proxies = {
    "http": "http://{0}:{1}@proxy.muc:8080".format(q_id, q_password),
    "https": "http://{0}:{1}@proxy.muc:8080".format(q_id, q_password),
    "no_proxy": "localhost,127.0.0.0,127.0.1.1,127.0.1.1,local.home,10.6.15.99,aws.cloud.bmw,.bmwgroup.net,.muc"
    }
    
else:
    print(os.environ.get('HOST'))
    proxies = {
    "http": "http://proxy.ccc-ng-1.ap-northeast-2.aws.cloud.bmw:8080",
    "https": "http://proxy.ccc-ng-1.ap-northeast-2.aws.cloud.bmw:8080",
    "no_proxy": "localhost,127.0.0.0,127.0.1.1,127.0.1.1,local.home,10.6.15.99,aws.cloud.bmw,.bmwgroup.net,.muc"
    }



conn=pg2.connect(database='hc',
             host=os.environ.get('HOST'),
             port=os.environ.get('PORT'),
             user='hc_js',
             password=os.environ.get('PASSWORD')
             )  

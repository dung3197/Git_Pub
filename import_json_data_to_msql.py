import json
from sqlite3 import Cursor
import pymysql
from urllib.request import urlopen

url = "https://625e1d1e6c48e8761ba540c2.mockapi.io/transaction"
response = urlopen(url)
data_json = json.loads(response.read())
# json_object = json.dumps(data_json, indent=4)
# with open("/home/dungnt/etl/etl/mockdata.json", "w") as outfile:
#     outfile.write(json_object)
# json_data=open("/home/dungnt/etl/etl/mockdata.json").read()
# json_object1=json.dumps(json.loads(json_data))
# print(json_object1)

con=pymysql.connect(host='123.30.234.234',user='dyan',password='abc@1234',database='gify_test')

cursor=con.cursor()

for item in data_json:
    id=item.get("id")
    # createat=item.get("createdAt")
    fromacc=item.get("from_account")
    toacc=item.get("to_account")
    amounts=item.get("amounts")
    cursor.execute("insert into jdata(id,from_account,to_account,amounts) value(%s,%s,%s,%s)",(id,fromacc,toacc,amounts))

con.commit()
con.close()

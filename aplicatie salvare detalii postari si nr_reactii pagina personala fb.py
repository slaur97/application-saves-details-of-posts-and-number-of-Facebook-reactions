
import requests
import mysql.connector
import json
import os
TOKEN="EAAE33ZCnTzW0BO5oxZAZALBjVrBmYB16ZBYcnVIRblcTZBjTDU3rkj2lEfCZBvaNIXJu2WnOUa6ATPPY2tB6ZAJBaRGdSBfEkWMrYZAQFcjR9tJjGRjcrgnZBjxbvpZCckYN6h0D6T9XIWLHPbZC46aVukuWmJG2i8IeaDn3weZAZAEfJC5RoV5v9620wLTuUA26Ncriam8T5ZBjphzBwauUpnlVxgTt4rtWYvIuyW2bcyt76jgRxYGEW5lJNSQ53pIzSibwZDZD"
CALE_DIR="C:/Users/Laurentiu/Desktop/Blabla"
CALE_SALVARE_RASPUNSURI="C:/Users/Laurentiu/Desktop/Blabla/Reactii raspunsuri primite"
url='https://graph.facebook.com/v18.0/7059159594166088/posts'
con=mysql.connector.connect(host ='127.0.0.1',user ='root',password ='root',database ='api')
cursor=con.cursor()

def prelucrare_requests(url):
    headers={'Authorization': 'Bearer '+TOKEN}
    raspuns=requests.get(url=url,headers=headers)
    fisier=raspuns.json()
   
    for element in fisier['data']:
        creare_folder(element['id'])
        cursor.execute(f"""INSERT INTO detalii 
                       VALUES(Null,'{element['created_time']}',null,'{element['id']}',
                       {prelucrare_reactii(element['id'],'LIKE')},
                       {prelucrare_reactii(element['id'],'LOVE')},
                       {prelucrare_reactii(element['id'],'WOW')},
                       {prelucrare_reactii(element['id'],'HAHA')})""")
        con.commit()
    with open(CALE_DIR+'/Postari/file.json','a')as jsonFile:
        json.dump(fisier,jsonFile)
    if(fisier['data']!=[]):
        link_next=fisier['paging']['next']
        return link_next
    else:
        return False

def prelucrare_reactii(id,tip_reactie):
        CALE=f"C:/Users/Laurentiu/Desktop/Blabla/Reactii raspunsuri primite/{id}"
        url=f"https://graph.facebook.com/v18.0/{id}/reactions?type={tip_reactie}&summary=true"
        headers={'Authorization': 'Bearer '+TOKEN}
        raspuns=requests.get(url=url,headers=headers)
        fisier=raspuns.json()
        try:
            nr_reactii=fisier['summary']['total_count']
        except:
            print("Nu exista summury")
        creare_json_reactii(CALE,tip_reactie,nr_reactii)
        return nr_reactii

def creare_folder(id):
    path = os.path.join(CALE_SALVARE_RASPUNSURI, id) 
    os.mkdir(path) 
def creare_json_reactii(CALE,tip_reactie,nr_reactii):
    with open(CALE+"/"+tip_reactie+".json",'w')as jsonFile:
        json.dump(nr_reactii,jsonFile)

while(url!=False):
    url=prelucrare_requests(url)









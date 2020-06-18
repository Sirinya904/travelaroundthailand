from flask import Flask , request
import requests
import pandas as pd
app = Flask(__name__)

import geopy.distance as ps
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open("CJE vs Big").sheet1



token = "PTnsgCeHaXxGv7wEbI1m0sMPc/upIL2bucyGWKGtcwKGd/KydstPlMgfdTc8nBNAPoke0V+sCFrjyVcR61kfK6X1dTFSg3N/gbsayDtWh8c+fTDt6CkCZ7bq50UYBDiwL14QkwhC+9LnCXYRziB9rAdB04t89/1O/w1cDnyilFU="

def flexjson(data):
    app = []

    for i in range(len(data)):
        item = data.iloc[i]
        print(item)
        datatime = item['Time'].split(" ")
        dyflex = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://assets.brandinside.asia/uploads/2017/03/botnoi-1111.jpg",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "action": {
                "type": "uri",
                "uri": "http://linecorp.com/"
                }
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "Botnoi Restaurant",
                    "weight": "bold",
                    "size": "xl"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "text",
                            "text": "Q NO.",
                            "color": "#aaaaaa",
                            "size": "sm",
                            "flex": 1
                        },
                        {
                            "type": "text",
                            "text": str(i),
                            "wrap": True,
                            "color": "#666666",
                            "size": "sm",
                            "flex": 5
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                        {
                            "type": "text",
                            "text": "Name"
                        },
                        {
                            "type": "text",
                            "text": item['Name']
                        }
                        ],
                        "spacing": "sm"
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                        {
                            "type": "text",
                            "text": "Seat"
                        },
                        {
                            "type": "text",
                            "text": str(item['Seats'])
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                        {
                            "type": "text",
                            "text": "Date"
                        },
                        {
                            "type": "text",
                            "text": str(datatime[0])
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                        {
                            "type": "text",
                            "text": "Time"
                        },
                        {
                            "type": "text",
                            "text":  str(datatime[1]) + " น."
                        }
                        ]
                    }
                    ]
                }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [

                    
                {
                    "type": "button",
                    "style": "primary",
                    "height": "sm",
                    "action": {
                        "type": "postback",
                        "label": "ได้รับโต๊ะแล้ว",
                        "data": "ได้รับโต๊ะแล้ว"
                    },
                    "color": "#3399ff"
                },
                {
                    "type": "button",
                    "style": "primary",
                    "height": "sm",
                    "action": {
                        "type": "postback",
                        "label": "ยกเลิกการจอง",
                        "data": "ยกเลิกการจอง"
                    },
                    "color": "#663300"
                },
                {
                    "type": "spacer",
                    "size": "sm"
                }
                ],
                "flex": 0
            }
        }

        app.append(dyflex)

    jsonbody = {
                "type": "flex",
                "altText": "This is a Flex Message",
                "contents": {
                    "type": "carousel",
                    "contents": app
                }   
    }
    return jsonbody


def ReplyMessageAPi(replyToken, message):
    print("message : ", message)
    jsonbody = {
        "replyToken":replyToken ,
        "messages":[
            message  
        ]
    }

    headers = {
        'Content-type': 'application/json',
        'Authorization' : 'Bearer ' + token
    }
    
    response = requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, json=jsonbody)    
    print("response : " , response.json())
    return "ok" ,  200


@app.route('/')
def hello_world():  
   return 'Hello World' 


@app.route('/webhook' , methods=['POST'])
def webhook():
    data = request.get_json()
    print(data)
    googlesheet = sheet.get_all_records()
    listdata = pd.DataFrame(googlesheet)
    print("listdata : " , listdata)
    try:
        replyToken = data['events'][0]['replyToken']
        typeMessage = data['events'][0]['type']
        if typeMessage == "message":
            
            message = data['events'][0]['message']['text']

            if message == "คิวโต๊ะเล็ก":
                print("message : 1" , message)
                item = listdata[listdata['Seats'] >= 1]
                item = item[item['Seats'] <= 2]



                message = flexjson(item)
                ReplyMessageAPi(replyToken , message)
            elif message == "คิวโต๊ะกลาง":
                print("message : 2" , message)
                item = listdata[listdata['Seats'] >= 3]
                item = item[item['Seats'] <= 4]
                message = flexjson(item)
                ReplyMessageAPi(replyToken , message)
            elif message == "คิวโต๊ะใหญ่":
                print("message : 3" , message)
                item = listdata[listdata['Seats'] > 4 ]
                message = flexjson(item)
                ReplyMessageAPi(replyToken , message)
            else:
                print("message : " , message)
                print("replyToken : " , replyToken)
                ReplyMessageAPi(replyToken , message)

        if typeMessage == "postback":

            print("postback")
            googlesheet = sheet.get_all_records()
            listdata = pd.DataFrame(googlesheet)
            item = listdata[listdata['Name'] == 'คุณครีม']
            number = list(item.index)[0] + 2
            sheet.update_cell(number , 4 , "Completed")
            pass

    except Exception as e:
        print("error : ", e)
    return "ok" , 200
    

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5000, debug=True)



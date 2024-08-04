import requests
import time
from datetime import datetime

current_date = datetime.now()

formatted_date = current_date.strftime("%y년 %m월 %d일")
formatted_time = current_date.strftime("%H시 %M분 %S초")

url = "https://api.kakaowork.com/v1/messages.send_by_email"

def return_Payload(type, color, codename, email_adress, msg):
    payload = {
        "email": email_adress,
        "text": type+": " + codename,
        "blocks": [
            {
                "type": "header",
                "text": type,
                "style": color
            },
            {
                "type": "description",
                "term": "코드명 :",
                "content": {
                    "type": "text",
                    "text": codename
                },
                "accent": True
            },
            {
                "type": "description",
                "term": "일자 :",
                "content": {
                    "type": "text",
                    "text": formatted_date
                },
                "accent": True
            },
            {
                "type": "description",
                "term": "시간 :",
                "content": {
                    "type": "text",
                    "text": formatted_time
                },
                "accent": True
            },
            {
                "type": "text",
                "text": msg
            }
        ]
    }
    return payload

def return_headers(api_key):
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    return header


def Info(codename, msg, email_adress_list, api_key):
    for email_adress in email_adress_list:
        try:
            payload = return_Payload('Info','yellow',codename, email_adress, msg)

            response = requests.post(url, headers=return_headers(api_key), json=payload)
            time.sleep(0.1)
        except:
            pass

def Success(codename, msg, email_adress_list, api_key):
    for email_adress in email_adress_list:
        try:
            payload = return_Payload('Success','blue',codename, email_adress, msg)
            response = requests.post(url, headers=return_headers(api_key), json=payload)
            time.sleep(0.1)
        except:
            pass

def Error(codename, msg, email_adress_list, api_key):
    for email_adress in email_adress_list:
        try:
            payload = return_Payload('Error','red',codename, email_adress, msg)
            response = requests.post(url, headers=return_headers(api_key), json=payload)
            time.sleep(0.1)
        except:
            pass

# 기본형
def txt(text, email_adress_list, api_key):
    for email_adress in email_adress_list:
        try:
            payload = {
                "email": email_adress,
                "text": text,
            }
            response = requests.post(url, headers=return_headers(api_key), json=payload)
            time.sleep(0.1)
        except:
            pass
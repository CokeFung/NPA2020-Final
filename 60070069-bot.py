import requests, json, time
from pprint import pprint
from flask import Flask, request
from Secret import *

username = 'admin'
password = 'cisco'


def getLoopbackInterfaceStatus():
    try:
        requests.packages.urllib3.disable_warnings()
        url = "https://10.0.15.102/restconf/data/ietf-interfaces:interfaces-state/interface=Loopback60070069"
        headers = {
            "Accept": "application/yang-data+json",
            "Content-type":"application/yang-data+json"
        }
        basic_auth = (username, password)
        response = json.loads(requests.get(url, auth=basic_auth, headers=headers, verify=False).text)
        # pprint(response['ietf-interfaces:interface']['oper-status'])
        return response['ietf-interfaces:interface']['oper-status']
    except:
        return 'host down'
    


  
def sentMsgtoWebex(my_token, room_id, text):
    url = "https://webexapis.com/v1/messages"
    header = {
        "Authorization": "Bearer %s" % my_token,
        "content-type": "application/json"
    }
    webex_payload = {"roomId":room_id, 'text':text}
    webex_response = requests.post(url=url, headers=header, json=webex_payload).json()
    return webex_response

def getMsgFromWebex(my_token, room_id):
    url = "https://webexapis.com/v1/messages"
    header = {
        "Authorization": "Bearer %s" % my_token,
        "content-type": "application/json"
    }
    param = {"roomId":room_id, 'max':1}
    response = requests.get(url=url, headers=header, params=param).json()
    return response

def main():
    cur_state=''
    my_token = "NzRhMTM0NzctZjMwZC00Y2QyLWI4ZDctNzkzMGI0ZTg0NmQyMWE0ZGRjNjEtMjZh_PF84_consumer"
    room_id = "Y2lzY29zcGFyazovL3VzL1JPT00vNjA5Nzk5NDAtNTU3My0xMWViLWEzNzUtY2JkMGE4ZjAxYTA3"
    message_response = {}
    while cur_state.lower() != "end":
        time.sleep(1)
        message = getMsgFromWebex(my_token, room_id)
        if not message_response == message:
            message_response = message
            cur_state = message['items'][0]['text']
            print("stat:", cur_state)
        if "60070069" in cur_state:
            text = getLoopbackInterfaceStatus()
            if text == "host down":
                "60070069's host is down"
            else:
                text = "Loopback60070062 - Operational status is " + text
            sentMsgtoWebex(my_token, room_id, text)
main()
import json
import os
import time
import requests
from datetime import datetime
from requests.structures import CaseInsensitiveDict
from dotenv import load_dotenv
from bs4 import BeautifulSoup

project_folder = os.path.expanduser('')
load_dotenv(os.path.join(project_folder, '.env'))

TOKEN = os.getenv("TOKEN")
chat_id = os.getenv("chat_id")
user_agent = os.getenv("user_agent")
Cookie = os.getenv("Cookie")

headers = CaseInsensitiveDict()
headers["Cookie"] = Cookie
headers["user_agent"] = user_agent

URL_TELEGRAM = f"https://api.telegram.org/bot{TOKEN}"

URL_Placement = "https://www.aitplacements.in/api/trpc/notice.publishedNoticeList?batch=1&input=%7B%220%22%3A%7B%22pageNos%22%3A1%7D%7D"

URL_Website = "https://www.aitplacements.in/dashboard"

website_text = f"Please check the aitplacement website for more details {URL_Website}"

list_of_notices1 = [0]

while True:
    list_of_id = []
    list_of_notices = []
    li = []
    list_of_new_id = []

    x = requests.get(URL_Placement, headers=headers)
    [results] = x.json()
    d = results["result"]["data"]["notices"]
    for i in d:
        list_of_notices.append([i["title"]])
        list_of_id.append(i["id"])
    if list_of_notices != list_of_notices1:
        request_telegram = requests.get(
            f"{URL_TELEGRAM}/sendMessage?chat_id={chat_id}&text={list_of_notices}")

        for i in list_of_notices:
            if i not in list_of_notices1:
                list_of_new_id.append(list_of_notices.index(i))

    for i in list_of_new_id:
        url_1 = f"https://www.aitplacements.in/api/trpc/notice.noticeDetail?batch=1&input=%7B%220%22%3A%7B%22id%22%3A%22{list_of_id[i]}%22%7D%7D"
        y = requests.get(url_1, headers=headers)
        [xy] = y.json()
        mm = xy['result']['data']

        pre_body = mm.get('body')
        soup = BeautifulSoup(pre_body, "html.parser")
        body = soup.get_text()
        body = body.replace('%', '%25')
        body = body.replace('#', '%23')
        body = body.replace('+', '%2B')
        body = body.replace('*', '%2A')
        body = body.replace('&', '%26')

        name_of_notice = list_of_notices[i][0]
        name_of_notice = name_of_notice.replace('%', '%25')
        name_of_notice = name_of_notice.replace('#', '%23')
        name_of_notice = name_of_notice.replace('+', '%2B')
        name_of_notice = name_of_notice.replace('*', '%2A')
        name_of_notice = name_of_notice.replace('&', '%26')

        request_telegram = requests.get(
            f"{URL_TELEGRAM}/sendMessage?chat_id={chat_id}&text={name_of_notice}")
        request_telegram = requests.get(
            f"{URL_TELEGRAM}/sendMessage?chat_id={chat_id}&text={body}")

        pre_attachment = mm.get('attachments')
        if pre_attachment == []:
            attachment = pre_attachment
            request_telegram = requests.get(
                f"{URL_TELEGRAM}/sendMessage?chat_id={chat_id}&text={attachment}")
        else:
            for i in range(len(pre_attachment)):
                attachment = pre_attachment[i].get("url")
                attachment = attachment.replace('%', '%25')
                attachment = attachment.replace('#', '%23')
                attachment = attachment.replace('+', '%2B')
                attachment = attachment.replace('*', '%2A')
                attachment = attachment.replace('&', '%26')

                request_telegram = requests.get(
                    f"{URL_TELEGRAM}/sendMessage?chat_id={chat_id}&text={attachment}")

        request_telegram = requests.get(
            f"{URL_TELEGRAM}/sendMessage?chat_id={chat_id}&text={website_text}")

        list_of_notices1 = list_of_notices

    time.sleep(7*60)

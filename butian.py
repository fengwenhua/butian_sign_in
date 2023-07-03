# -*- coding: utf-8 -*-
"""
cron: 1 0 0 * * *
new Env('butian');
"""

from sendNotify import send
import requests
import os
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings()


def start(cookie, token):
    max_retries = 20
    retries = 0
    msg = ""
    while retries < max_retries:
        try:
            msg += "[*] 第{}次执行签到\n".format(str(retries+1))
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': cookie,
                'Origin': 'https://forum.butian.net',
                'Referer': 'https://forum.butian.net/',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            }

            data = {
                '_token': token,
            }

            res = requests.post(
                'https://forum.butian.net/sign', headers=headers, data=data)
            res_text = res.text

            success = False

            soup = BeautifulSoup(res_text, 'html.parser')
            sign_res_element = soup.select_one('div.side-sign dt button')
            if sign_res_element:
                content = sign_res_element.text.strip()
                print(content)
                msg += '[+] ' + content + '\n'
                success = True
                # 已签到
            else:
                print("[-] 未找到签到结果")
                msg += "[-] 未找到签到结果"

            sign_msg_element = soup.select_one('div#alert_message')
            if sign_msg_element:
                content = sign_msg_element.text.replace('×', '').strip()
                print(content)
                msg += '[+] '+content + '\n'
                # 签到成功!经验 +1，金币 +1
                # 今日已签到，不能重复签到
            else:
                print("[-] 未找到本次签到细节")
                msg += "[-] 未找到本次签到细节"

            if success:
                print("签到结果: ", msg)
                send("butian 签到结果", msg)
                break  # 成功执行签到，跳出循环
            elif retries >= max_retries:
                print("达到最大重试次数，签到失败。")
                send("butian 签到结果", msg)
                break
            else:
                retries += 1
                print("等待20秒后进行重试...")
                time.sleep(20)

        except Exception as e:
            print("签到失败，失败原因:"+str(e))
            send("butian 签到结果", str(e))
            retries += 1
            if retries >= max_retries:
                print("达到最大重试次数，签到失败。")
                break
            else:
                print("等待20秒后进行重试...")
                time.sleep(20)


if __name__ == '__main__':
    cookie = os.getenv("BUTIAN_COOKIE")
    token = os.getenv("BUTIAN_TOKEN")

    start(cookie, token)

#!/usr/bin/env python

import time
import requests
import lxml.html
import pynotify



def getCookie(url):
    #url="https://mypage.etisalat.lk/bbportal/pkg"
    req = requests.get(url)
    cookie=req.headers['set-cookie']
    cookie=cookie.partition(";")[0].partition("=")[2]


    return cookie


def getDom(url):
    value=getCookie(url)
    cookies=dict(JSESSIONID=value)

    html = requests.get(url,cookies=cookies).content
    dom = lxml.html.fromstring(html)

    return dom


def scrapData(dom):
    # current_data=dom.cssselect("#usageValUsed")
    # #print current_data[0].text_content().strip()

    # percentage=dom.cssselect("#usageValPercent")
    # #print percentage[0].text_content().strip()

    # #last_month=dom.
    #total_due=dom.cssselect("#totalDue")
    #print total_due[0].text_content().strip()


    id_list=["#usageValUsed","#usageValPercent","#creditLimit","#totalDue","#lastBill","#dataRate","#dataQuota","#msisdn"]

    data={id:dom.cssselect(id)[0].text_content().strip() for id in id_list}

    return data


def notify(data):
    pynotify.init("Basic")
    text="Current data usage: %s (%s%%) \nTotal Due amount: %s\n" %(data["#usageValUsed"],data["#usageValPercent"],data["#totalDue"])

    n=pynotify.Notification("Etisalat data usage",text)
    n.set_urgency(pynotify.URGENCY_CRITICAL)

    print text
    n.show()


def main():
    url="https://mypage.etisalat.lk/bbportal/pkg"
    dom = getDom(url)
    data=scrapData(dom)
    notify(data)

main()

# def not_main():
#     url="https://mypage.etisalat.lk/bbportal/pkg"
#     req = requests.get(url)
#     print req.status_code

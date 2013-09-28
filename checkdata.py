#!/usr/bin/env python

import time
import requests
import lxml.html
import pynotify



def getCookie(url):
    """get session values from the specified url"""
    req = requests.get(url)
    cookie=req.headers['set-cookie']
    cookie=cookie.partition(";")[0].partition("=")[2]


    return cookie


def getDom(url):
    """get the dom for the specified url"""
    value=getCookie(url)
    cookies=dict(JSESSIONID=value)

    html = requests.get(url,cookies=cookies).content
    dom = lxml.html.fromstring(html)

    return dom


def scrapData(dom):
    """scrap the dom for the required set of data"""

    id_list=["#usageValUsed","#usageValPercent","#creditLimit","#totalDue","#lastBill","#dataRate","#dataQuota","#msisdn"]

    data={id:dom.cssselect(id)[0].text_content().strip() for id in id_list}

    return data


def notify(data):
    """notify the user with a simple pop-up message"""
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

if __name__=='__main__':
    main()

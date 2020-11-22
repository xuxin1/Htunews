


# 在这里调用了一些 实现 数据分析  和 发送邮件需要的库

import urllib.request
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import time
from bs4 import BeautifulSoup


#   三个函数   mail askurl datalist


def mail(news):   #发送邮件函数
    my_sender = '734532469@qq.com'  # 发件人邮箱账号
    my_pass = 'password'  # 发件人邮箱密码
    my_user = '201356257@qq.com'  # 收件人邮箱账号，我这边发送给自己

    ret = True
    try:
        # i=str(i)
        text = str(news)
        msg = MIMEText('来自徐鑫的邮件', 'plain', 'utf-8')
        msg['From'] = formataddr(["FromRunoob", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["FK", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = text  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret


def askurl(url):  # 访问网址
    head = {
        "User-Agent": " Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
    }  # head浏览器标识  防止反爬虫
    get = urllib.request.Request(url=url, headers=head)  # 传参 就收服务器返回数据
    date = urllib.request.urlopen(get)  # 打开页面
    # print(date.read().decode("utf-8"))
    return date


def datalist():  # 获取通知列表
    data = askurl("https://www.htu.edu.cn/8955/list.htm")

    jiexi = BeautifulSoup(data, "html.parser")  # bs数据解析  网页数据命名为 jiexi
    yuanshi_shuju = []  # 上一次数据
    xin_shuju = []

    for i in range(2, 10):  # 匹配8条数据
        i = str(i)
        cssindex = "html body div.list_main.clearfix div.list_right div.right_bottom div div#wp_news_w15 ul.wp_article_list li.list_item.i" + i + " div.fields.pr_fields span.Article_Title a"
        yuanshi_shuju.append(jiexi.select(cssindex))
    return yuanshi_shuju


news = []
flashlist = []
original_data = datalist()


while True:
    flashlist = datalist()
    if original_data == flashlist:  #如果没有新的通告
        time.sleep(3)
    else:           #如果有新通告
        for item in range(len(flashlist)):
            if item in original_data:
                pass
            else:
                news.append(flashlist[item])
        # 发送邮件
        mail(news)
        # 重置原始数据列表
        original_data[:] = flashlist[:]
        # 重置 news列表
        news = []


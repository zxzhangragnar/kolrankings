
###########################################
## twikit文档：
# https://twikit.readthedocs.io/en/latest/twikit.html
###########################################
import asyncio
from twikit import Client

import smtplib
from email.mime.text import MIMEText
from email.header import Header

from datetime import datetime
import pytz

import os 

# Enter your account information
USERNAME = '@billtester73890'
EMAIL = 'billzhang2025@gmail.com'
PASSWORD = 'billtester2025'

## 换账号也提示 "code":366,"message":"flow name LoginFlow is currently not accessible"， 应该使ip地址被封了
# USERNAME = '@bill20029464456'
# EMAIL = 'zhangzixuan2021@gmail.com'
# PASSWORD = 'a1111billklaus'

# client = Client('en-US')
client = Client(language='en-US', 
                user_agent='Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0',
               )

async def main():
    # Asynchronous client methods are coroutines and
    # must be called using `await`.
    await client.login(
        auth_info_1=USERNAME,
        auth_info_2=EMAIL,
        password=PASSWORD
    )

    # if os.path.exists("cookies.json"):
    #     client.load_cookies("cookies.json")
    # else:
    #     await client.login(
    #         auth_info_1=USERNAME, auth_info_2=EMAIL, password=PASSWORD
    #     )
    #     client.save_cookies("cookies.json")

    ###########################################
    # 创建时区对象
    utc = pytz.UTC
    cst = pytz.timezone('Asia/Shanghai')
    # 获取当前的北京时间
    current_beijing_time = datetime.now(cst).strftime("%Y-%m-%d %H:%M:%S")

    # QUERY = '(from:elonmusk) lang:en until:2020-01-01 since:2018-01-01'
    # QUERY = 'from:elonmusk CA since:2024-10-05 23:59:59'
    # QUERY = '(from:elonmusk) lang:en since:2024-10-06'

    QUERY = '(from:elonmusk) since:2024-10-06'

    # Search Latest Tweets
    tweets = await client.search_tweet(QUERY, 'Latest', 20)

    # 定义要检测的关键词列表
    keywords = ["CA", "address", "Token", "launch", "buy", "Crypto", "ICO"]
    filtered_tweets = []

    for tweet in tweets:
        matched_keywords = [keyword for keyword in keywords if keyword.lower() in tweet.text.lower()]

        if matched_keywords:  # 如果推文包含任意关键词
            # 转换发布时间为中国北京时间
            utc_time = datetime.strptime(tweet.created_at, "%a %b %d %H:%M:%S %z %Y")
            beijing_time_created_at = utc_time.astimezone(cst)
            # 提取推文的关键信息
            tweet_info = {
                "id": tweet.id,
                "created_at": beijing_time_created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "author": tweet.user.name,
                "keywords": matched_keywords,
                "content": tweet.text,
                "link": f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
            }
            filtered_tweets.append(tweet_info)

    receivers = '3257649830@qq.com,zhangzixuan2021@gmail.com'
    # 输出筛选后的推文, 发送到邮箱
    # for tweet in filtered_tweets:
    #     print(tweet)
    # 将筛选后的推文信息转换为字符串
    result_string = ""
    for tweet in filtered_tweets:
        result_string += (
            f"ID: {tweet['id']}\n"
            f"发布时间: {tweet['created_at']}\n"
            f"作者: {tweet['author']}\n"
            f"涉及的关键词: {', '.join(tweet['keywords'])}\n"
            f"正文内容: {tweet['content']}\n"
            f"链接: {tweet['link']}\n"
            "-----------------------------\n"
        )

    sendemail(result_string, 'sniper: ' + current_beijing_time, receivers)



def sendemail(msg_text, msg_subject, receivers):

    # 第三方 SMTP 服务
    mail_host="smtp.163.com"  #设置服务器
    mail_user="zhangzixuan2021101@163.com"    #用户名
    mail_pass="VSvi2BGEP67KUYkw"   #口令  


    sender = 'zhangzixuan2021101@163.com'
    # receivers = '3257649830@qq.com,zhangzixuan2021@gmail.com'  # 接收邮件
    
    message = MIMEText(msg_text, 'plain') # 正文
    # message['From'] = Header("Web3Sniper.com") # 发件人别名
    message['From'] = Header("zhangzixuan2021101@163.com" ) # 发件人
    message['To'] =  Header(receivers) # 收件人 群发
    message['Subject'] = Header(msg_subject) # 主题

    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host,25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers.split(','), message.as_string())
        print ("send email success")
    except smtplib.SMTPException:
        print ("Error: send email fail")

asyncio.run(main())











###########################################
## twikit文档：
# https://twikit.readthedocs.io/en/latest/twikit.html
###########################################
import asyncio
from twikit import Client

import smtplib
from email.mime.text import MIMEText
from email.header import Header

from datetime import datetime, timedelta
import pytz
import os 

# Enter your account information
USERNAME = '@billtester73890'
EMAIL = 'billzhang2025@gmail.com'
PASSWORD = 'billtester2025'

# client = Client('en-US')
client = Client(language='en-US', 
                user_agent='Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0')

# 假设已经导入了正确的邮件发送函数和推文获取函数
# from your_mail_module import sendemail
# from your_twitter_client_module import get_tweets, client

# =========================
# 1. 认证和 Cookie 处理部分
# =========================
async def login_or_load_cookies(client, username, email, password, cookie_file="cookies.json"):
    """登录 Twitter 或从 cookie 文件加载登录信息。"""
    if os.path.exists(cookie_file):
        client.load_cookies(cookie_file)
    else:
        await client.login(auth_info_1=username, auth_info_2=email, password=password)
        client.save_cookies(cookie_file)


# =====================
# 2. 时间处理部分
# =====================
def get_beijing_and_previous_eastern_time():
    """获取北京时间和美国东部时间的前一天日期。"""
    # 创建时区对象
    cst = pytz.timezone('Asia/Shanghai')
    # 获取当前的北京时间
    current_beijing_time = datetime.now(cst).strftime("%Y-%m-%d %H:%M:%S")

    # 获取美国东部时间的前一天
    eastern = pytz.timezone('US/Eastern')
    current_eastern_time = datetime.now(eastern)
    previous_day = current_eastern_time - timedelta(days=1)

    # 格式化为 yyyy-mm-dd 格式
    query_date = previous_day.strftime('%Y-%m-%d')

    return current_beijing_time, query_date


# ======================
# 3. 推文过滤处理部分
# ======================
async def get_filtered_tweets(client, usernames, query_date, case_sensitive_keywords, case_insensitive_keywords, timezone):
    """获取指定用户的推文，并根据关键词进行筛选。"""
    filtered_tweets_array = []

    for kol_name in usernames:
        query = f"(from:{kol_name}) since:{query_date}"
        # 异步获取推文数据
        tweets = await client.search_tweet(query, 'Latest', 20)
        filtered_tweets = []

        for tweet in tweets:
            # 筛选推文中包含指定关键词的推文
            matched_keywords = []
            # 检查大小写敏感关键词（"CA"）
            matched_keywords.extend([keyword for keyword in case_sensitive_keywords if keyword in tweet.text])
            # 检查大小写不敏感关键词
            matched_keywords.extend([keyword for keyword in case_insensitive_keywords if keyword.lower() in tweet.text.lower()])

            if matched_keywords:
                # 转换发布时间为中国北京时间
                utc_time = datetime.strptime(tweet.created_at, "%a %b %d %H:%M:%S %z %Y")
                beijing_time_created_at = utc_time.astimezone(timezone)
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

        filtered_tweets_array.append({kol_name: filtered_tweets})

    return filtered_tweets_array


# ============================
# 4. 格式化推文内容为字符串部分
# ============================
def format_tweets(filtered_tweets_array):
    """将过滤后的推文格式化为字符串输出。"""
    result_string = ""
    for user_tweets in filtered_tweets_array:
        # 获取用户名和推文列表
        user = list(user_tweets.keys())[0]
        tweets = list(user_tweets.values())[0]

        # 将每条推文格式化为字符串
        user_tweets_str = f"User: @{user}\n==========\n"
        for tweet in tweets:
            user_tweets_str += (
                f"ID: {tweet['id']}\n"
                f"发布时间: {tweet['created_at']}\n"
                f"作者: {tweet['author']}\n"
                f"涉及的关键词: {', '.join(tweet['keywords'])}\n"
                f"正文内容: {tweet['content']}\n"
                f"链接: {tweet['link']}\n"
                "-----------------------------\n"
            )
        # 将格式化结果加入总字符串
        result_string += user_tweets_str + "\n"

    return result_string

# =================
# 5. 发送邮件函数
# =================
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

# =================
# 6. 主程序入口
# =================
async def main():
    # 1. 认证处理
    await login_or_load_cookies(client, USERNAME, EMAIL, PASSWORD)

    # 2. 获取时间
    current_beijing_time, query_date = get_beijing_and_previous_eastern_time()

    # 3. 获取并筛选推文
    kols = ['elonmusk', 'realDonaldTrump', 'POTUS', 'Caitlyn_Jenner', 'MikeTyson', 'IGGYAZALEA']  # 用户名列表

    # 定义要检测的关键词列表（"CA" 大小写敏感）
    case_sensitive_keywords = ["CA"]
    case_insensitive_keywords = ["Token", "address", "coin", "launch", "buy", "Crypto", "ICO", "tax"]
    # keywords = ["CA", "address", "Token", "launch", "buy", "Crypto", "ICO", 'coin']
    cst = pytz.timezone('Asia/Shanghai')  # 设置中国时区
    filtered_tweets_array = await get_filtered_tweets(client, kols, query_date, case_sensitive_keywords, case_insensitive_keywords, cst)

    # 4. 格式化推文
    formatted_tweets = format_tweets(filtered_tweets_array)

    # 5. 发送邮件
    receivers = '3257649830@qq.com,zhangzixuan2021@gmail.com'
    sendemail(formatted_tweets, f'sniper: {current_beijing_time}', receivers)

asyncio.run(main())

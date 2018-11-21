import requests
import smtplib
import socket

from lxml import etree
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from smtplib import SMTPRecipientsRefused,SMTPServerDisconnected
from multiprocessing import Process

url = 'http://www.budejie.com/'
headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
	'Host':'www.budejie.com'
}

# email settings
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'xxxxxx@qq.com'

EMAIL_HOST_PASSWORD = 'password'
EMAIL_SUBJECT_PREFIX = '愿博你一笑(来自xxx)'
EMAIL_SENDER = 'xxxxxx@qq.com'
EMAIL_RECEIVER = 'xxxxxx@qq.com'

# 线程列表
# process_list = []

# def download_image(url):
# 	path = url.split('/')[-1]
# 	response = requests.get(url)
# 	img = response.content

# 	with open('./images/{path}'.format(path=path), 'wb') as f:
# 		f.write(img)

# 	print('下载成功: ' + path)

def get_joke(url=url):
	html = requests.get(url=url, headers=headers).text
	selector = etree.HTML(html)

	joke_list_xpath = selector.xpath("//div[@class='j-r-c']/div[@class='j-r-list']")
	joke_list_1 = joke_list_xpath[0]
	joke_list_2 = joke_list_xpath[1]
	joke_list = []

	for joke_info in joke_list_1.xpath("./ul/li"):
		joke = {}
		joke['created_time'] = joke_info.xpath("./div[@class='j-list-user']//span[contains(@class,'u-time')]/text()")[0] if joke_info.xpath("./div[@class='j-list-user']//span[contains(@class,'u-time')]/text()") else ''
		joke['desc'] = joke_info.xpath("./div[@class='j-r-list-c']/div[@class='j-r-list-c-desc']/a/text()")[0] if joke_info.xpath("./div[@class='j-r-list-c']/div[@class='j-r-list-c-desc']/a/text()") else ''
		joke['image'] = joke_info.xpath("./div[@class='j-r-list-c']/div[@class='j-r-list-c-img']/a/img/@data-original")[0] if joke_info.xpath("./div[@class='j-r-list-c']/div[@class='j-r-list-c-img']/a/img/@data-original") else ''
		# 下载图片
		# p = Process(target=download_image,args=(joke['image'],))
		# p.start()
		# process_list.append(p)
		joke['like'] = int(joke_info.xpath("./div[@class='j-r-list-tool']//li[@class='j-r-list-tool-l-up']/span/text()")[0]) if joke_info.xpath("./div[@class='j-r-list-tool']//li[@class='j-r-list-tool-l-up']/span/text()") else '0'
		
		joke_list.append(joke)

	for joke_info in joke_list_2.xpath("./ul/li"):
		joke = {}
		joke['created_time'] = joke_info.xpath("./div[@class='j-list-user']//span[contains(@class,'u-time')]/text()")[0] if joke_info.xpath("./div[@class='j-list-user']//span[contains(@class,'u-time')]/text()") else ''
		joke['desc'] = joke_info.xpath("./div[@class='j-r-list-c']/div[@class='j-r-list-c-desc']/a/text()")[0] if joke_info.xpath("./div[@class='j-r-list-c']/div[@class='j-r-list-c-desc']/a/text()") else ''
		joke['image'] = joke_info.xpath("./div[@class='j-r-list-c']/div[@class='j-r-list-c-img']/a/img/@data-original")[0] if joke_info.xpath("./div[@class='j-r-list-c']/div[@class='j-r-list-c-img']/a/img/@data-original") else ''
		# 下载图片
		# p = Process(target=download_image,args=(joke['image'],))
		# p.start()
		# process_list.append(p)
		joke['like'] = int(joke_info.xpath("./div[@class='j-r-list-tool']//li[@class='j-r-list-tool-l-up']/span/text()")[0]) if joke_info.xpath("./div[@class='j-r-list-tool']//li[@class='j-r-list-tool-l-up']/span/text()") else '0'
		
		joke_list.append(joke)

	return joke_list

def send_email(joke, email_host=EMAIL_HOST, email_host_user=EMAIL_HOST_USER, email_host_password=EMAIL_HOST_PASSWORD, email_recevier=EMAIL_RECEIVER):
	msg = MIMEMultipart('related')
	content = MIMEText('<html><body><h2>{title}</h2><img src="{src}" alt="imageid"><h2>好梦,晚安</h2></body></html>'.format(title=joke['desc'], src=joke['image']), 'html', 'utf-8')
	print('image source: ' + joke['image'])
	msg.attach(content)
	msg['Subject'] = EMAIL_SUBJECT_PREFIX
	msg['From'] = email_host_user
	msg['To'] = email_recevier

	# with open('./images/{path}'.format(path=joke['image'].split('/')[-1]), 'rb') as f:
	# 	img = f.read()

	# img = MIMEImage(img)
	# img.add_header('Content-ID', 'imageid')
	# msg.attach(img)

	client = smtplib.SMTP_SSL(email_host, EMAIL_PORT)
	client.login(email_host_user,email_host_password)
	try:
		client.sendmail(email_host_user, [email_recevier,], msg.as_string())
		print('发送成功')
		client.quit()
	except SMTPRecipientsRefused:
		print('邮箱地址错误')
	except socket.gaierror:
		print('网络连接失败') 
	except SMTPServerDisconnected:
		print('服务器发送错误') 
	except Exception as e:
		raise e

if __name__ == '__main__':
	joke_list = sorted(get_joke(), key=lambda joke:joke['like'])

	# 主进程等待子线程完成
	# for p in process_list:
	# 	p.join()

	# 发送赞的数量最多的那个joke
	send_email(joke=joke_list[-1])

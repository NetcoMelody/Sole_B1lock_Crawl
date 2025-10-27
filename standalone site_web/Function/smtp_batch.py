import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from email.mime.image import MIMEImage
class email_send:
    def __init__(self, receiver_email):
        email_str = receiver_email
        email_list = email_str.split(',')
        print (email_list)
        self.sender_email = '17816258635@163.com'
        self.smtp_host = 'smtp.163.com'
        self.auth_code = 'WPtjWi8A8DKYnuYW'
        self.receiver_email = email_list

    def send_email(self, receiver_email):
        msg = MIMEMultipart('mixed')
        msg['from'] = formataddr(pair=('我是测试者', self.sender_email), charset='utf-8')
        msg['to'] = formataddr(pair=('你是被测试的', receiver_email), charset='utf-8')
        msg['subject'] = Header("Thank you for joing Soleb1ock! Unlock Exclusive Deals and Best Prices Today", charset='utf-8')

        html_text = """
Hi Fam! 🙌<br>
<br>
Thank you for joining the family! We're excited to have you with us and can't wait for you to have your perfect pair. 🤝<br>
<br>
The Highly sought-after Jordan 4 Undefeated is now live on soleb1ock.com<br> 
Don't miss your chance to cop this exclusive drop - we've got you covered with this exclusive release.  👌<br>
<br>
<p><a href='https://soleb1ock.com/product/undefeated-jordan-air-4-retro-2025-greenib1519-200/'><img src="cid:1" weight=800 height=800></a></p>
<br>
Why shop with us?
<ul> 
<li>Best Prices Guaranteed - save more compared to other websites!</li>
<li>Authentic & Brand New - Straight from brands, guaranteed!</li>
<li>Exclusive Discount Coupon - Use at checkout for extra savings!</li>
<li>Trusted & Highly Rated - Serving sneakerheads for years with top reviews.</li>
</ul>
<br>
<p><a href='https://soleb1ock.com/'><img src="cid:2" weight=800 height=800></a></p>
<br>
👉 Can't find the pair you're looking for?<br>
<br>
Message us on Facebook or Instagram @sole_b1ock or reach out via Whatsapp 👇 scan QR<br>
<br>
<p><img src="cid:3" weight=400 height=300></p>
"""
        msg.attach(MIMEText(html_text, 'html', 'utf-8'))
        with open('D:/PythonProject_UV/Fusion/static/1.png', 'rb') as file:
            image_resource_1 = MIMEImage(file.read())
        image_resource_1.add_header('Content-ID', '<1>')
        msg.attach(image_resource_1)

        with open('D:/PythonProject_UV/Fusion/static/2.png', 'rb') as file:
            image_resource_2 = MIMEImage(file.read())
        image_resource_2.add_header('Content-ID', '<2>')
        msg.attach(image_resource_2)

        with open('D:/PythonProject_UV/Fusion/static/3.png', 'rb') as file:
            image_resource_3 = MIMEImage(file.read())
        image_resource_3.add_header('Content-ID', '<3>')
        msg.attach(image_resource_3)

        smtp_conn = smtplib.SMTP_SSL(self.smtp_host, 465, timeout=120)
        smtp_conn.ehlo()
        smtp_conn.login(user=self.sender_email, password=self.auth_code)
        smtp_conn.sendmail(from_addr=self.sender_email, to_addrs=receiver_email, msg=msg.as_string())
        print('发送成功')
        smtp_conn.close()

    def email_main(self):
        for i in self.receiver_email:
            self.send_email(i)


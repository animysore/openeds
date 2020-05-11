import sys
import time
import pandas as pd
import smtplib
from selenium import webdriver
from datetime import date, datetime
from email.mime.text import MIMEText

MY_EMAIL_ADDRESS = 'animus.unofficial@gmail.com'
PASSWORD = 'F0C181443CEF414DED08672F9DF1123C9481F4B1F5C48C987D67C0E5666DFCB3'
HOST = 'smtp.gmail.com'
PORT = 587
EMAILS = 'aniruddha.mysore@gmail.com, animus.unofficial@gmail.com, adish.rao98@gmail.com'

def scrape():
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	browser = webdriver.Chrome(chrome_options=options)
	browser.get('https://evalai.cloudcv.org/web/challenges/challenge-page/603/leaderboard/1680')

	while True:
		try: 
			tbody = browser.find_element_by_css_selector('tbody')
			break
		except:
			time.sleep(1)

	rows = tbody.find_elements_by_css_selector('tr')
	data = []
	for r in rows:
		cells = r.find_elements_by_css_selector('td')
		data.append(list(map(lambda c: c.text, cells) ))

	df = pd.DataFrame(data, columns = ['Position', 'Team', 'Score', 'Submitted On' ]) 
	browser.close()
	return df

def diff(df):
	old = pd.read_csv('data.csv')
	df.to_csv('data.csv', index=False)
	
	if old['Team'].to_list() == df['Team'].to_list(): return False

	return True

# Setup server
def server_setup(host,port):
  server = smtplib.SMTP(host,port)
  server.starttls()
  server.login(MY_EMAIL_ADDRESS,PASSWORD)
  return server

# Send Mails
def send_mail(server):
  # Setup the parameters of the message
	msg = MIMEText(f'''
		Check the leaderboard here - https://evalai.cloudcv.org/web/challenges/challenge-page/603/leaderboard/1680 \n
		Last updated {datetime.now().isoformat()}
	''')
	msg['From'] = MY_EMAIL_ADDRESS
	msg['To'] = EMAILS
	msg['Subject'] = f"OpenEDS Leaderboard has been updated! - {date.today().isoformat()}"

	# Try to send the mail, else print the 
	try:
		server.send_message(msg)
		print('Mail Sent')
	except:
		print('Mail Failure')
		sys.exit(0)

def main():
	# Change the respective HOST and PORT address
	server = server_setup(HOST,PORT)
	df = scrape()
	if diff(df):
		send_mail(server)
	
main()

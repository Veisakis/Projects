import os
import requests
from datetime import date
from bs4 import BeautifulSoup


def sendMessage(msg):
	bot_token = os.environ['TELEGRAM_TOKEN']
	bot_chatID = os.environ['TELEGRAM_CHATID']
	url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={bot_chatID}&text={msg}&disable_notification=True'

	status = requests.get(url)
	return status.json()	


date = date.today().strftime("%d%m")
base = "https://www.sansimera.gr/almanac/"

r = requests.get(base+date)
soup = BeautifulSoup(r.text, 'lxml')

timeline = soup.find('ul', class_='timeline')

for item in timeline.find_all('li', limit=2):
	fact = item.a.get_text() + ": " + item.p.get_text()
	sendMessage(fact)

import os
import requests
from datetime import date
from bs4 import BeautifulSoup


def sendMessage(msg):
	bot_token = os.environ['TELEGRAM_TOKEN']
	bot_chatID = os.environ['TELEGRAM_CHATID']
	url = "https://api.telegram.org/bot{token}/sendMessage?chat_id={id}&text={message}".format(token=bot_token, id=bot_chatID, message=msg)

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

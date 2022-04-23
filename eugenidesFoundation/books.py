import os
import requests
from bs4 import BeautifulSoup

base = "https://www.eef.edu.gr/"
urls = []

with open('urls', 'r') as f:
	for url in f.readlines():
		urls.append(url.strip('\n'))

counter = 1
for url in urls:
	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'lxml')

	for link in soup.find_all('div', class_="download-item"):
		pdf = base + link.a.get('href')
		print(f'{counter:<4}: Downloading {pdf}')
		#os.system("wget " + pdf)
		counter += 1

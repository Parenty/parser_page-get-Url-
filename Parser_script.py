#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re
import requests
from bs4 import BeautifulSoup
import time
import lxml
import json
from requests.exceptions import ConnectionError

start_time = time.time()
list_urls = []

Host = 'https://43253.shot-uchi.ru'
Teacher_first_page = '/teachers/stats/main'
count_while = 0
links_while = []
final_list = []


# Создаем авторизованную сессию
s = requests.Session()
resp = s.get(Host)
html_text = resp.text
token = (re.search('(?<=\<meta name=\"csrf-token\" content=\")(.+)(?=\" />)', html_text)).group()

data = {#"utf8": '%E2%9C%93',
			"authenticity_token": token,
			#"next": '/home',
			"login": 'teacher3315@uchi.ru',
			"password": '1'
	 }

r = s.post(Host, data = data)
if r.status_code == 500:
	print('500-ка при логине')
	sys.exit()


# Функция, которая вытаскивает со страницы все ссылки и ее статус код
def get_html_and_stcode(url):
	try:
		r2 = s.get(url, timeout = 30)
		a = [r2.text, r2.status_code]
	except (ConnectionError, ConnectionResetError) as e:
		print(e)
		a = ['нет соединения', 'нет ответа']
	# r = post_html_and_stcode(Host).get(url, timeout = 5)
	# r = requests.get(url, timeout = 5)
	
	return a	
			#возвращает html-код страницы и статус код


# Достаем только код страницы
def get_html(page_andst):
	text_html = page_andst[0]
	return text_html


# Достаем только статус-код
def get_status_code(page_andst):
	s_code = page_andst[1]
	return s_code


# Парсим страницу и достаем все ссылки
def get_only_url(html_page):
	soup = BeautifulSoup(html_page, 'lxml') #создаю объект супа
	list_urls = []
	for i in soup.find_all('link', href = True): #ищу все ссылки с тэгом link
		link = str(i.get('href'))
		list_urls.append(link)

	for i in soup.find_all('a', href = True): #ищу все ссылки с тэгом a
		link = str(i.get('href'))
		list_urls.append(link)

		# достаю остальные ссылки (начинающиеся с http)
	# only_url = re.findall('((?<=href=")([\/].+)(?= [\/]))', html_page)
	only_url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', html_page)
	for i in only_url:
		list_urls.append(i)


	return list_urls



# Достаю абсолютно все ссылки с сайта и их статус код
def get_links_while(url):

	links_while.append(url)

	global count_while

	# while count_while != 1:                   #len(links_while)

	

	while count_while != len(links_while):

		current_url = links_while[count_while]

		req = get_html_and_stcode(current_url)
		count_while = count_while + 1
		req_html = get_html(req)
		req_st_code = get_status_code(req)

		urls_while = get_only_url(req_html)

		links_and_response = {"url": current_url, "status_code": req_st_code}
		final_list.append(links_and_response)

		print(links_and_response)
		print('\n')
		print(count_while)

		for link in urls_while:

			if not '/logout' in link:

				if link.startswith('/') and not link.startswith('//') and not 'card' in link:
					link = Host + link

				if link.startswith(Host) and link not in links_while:
					links_while.append(link)			

		if count_while == len(links_while):
			print('Все ссылки найдены!')





def main():
	global count
	get_links_while(Host+Teacher_first_page)
	print('всего ссылок ' + str(len(links_while)))

	# Записываю результаты в файл
	with open("statuscode.json", "w", encoding = "utf-8") as file:
		json.dump(final_list, file, indent = 4)
		file.close()


if __name__ == '__main__':
	main()

print('--- %.3f seconds ---' % (time.time()-start_time))



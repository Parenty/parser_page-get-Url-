#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup
import time
import lxml
import json

start_time = time.time()
list_urls = []

Host = 'https://43059.shot-uchi.ru'
Teacher_first_page = '/teachers/stats/main'
links = set()
count = 0
list_of_stcode = []




def post_html_and_stcode(url):

	s = requests.Session()
	resp = s.get(url)
	html_text = resp.text
	token = (re.search('(?<=\<meta name=\"csrf-token\" content=\")(.+)(?=\" />)', html_text)).group()


	data = {#"utf8": '%E2%9C%93',
			"authenticity_token": token,
			#"next": '/home',
			"login": 'dmitriev@uchi.ru',
			"password": '1'
	 }

	r = s.post(url, data = data)

	return s

def get_html_and_stcode(url):
	r = post_html_and_stcode(Host).get(url)
	# r = requests.get(url)
	a = [r.text, r.status_code]
	return a	
			#возвращает html-код страницы и статус код

def get_html(page_andst):
	text_html = page_andst[0]
	return text_html


def get_status_code(page_andst):
	s_code = page_andst[1]
	return s_code


def get_only_url(html_page):
	soup = BeautifulSoup(html_page, 'lxml') #создаю объект супа
	#list_urls = []
	for i in soup.find_all('link', href = True): #ищу все ссылки с тэгом link
		link = str(i.get('href'))
		list_urls.append(link)

	for i in soup.find_all('a', href = True): #ищу все ссылки с тэгом a
		link = str(i.get('href'))
		list_urls.append(link)

		#достаю остальные ссылки (начинающиеся с http)
	only_url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', html_page)
	for i in only_url:
		list_urls.append(i)

	for i in list_urls:
		if not i.startswith('/'):
			list_urls.remove(i)


	unique_urls = set(list_urls)

	return unique_urls



def get_all_links(url, maxdepth = 2):

	global count
	
	links_recursive = []
	# post_html_and_stcode(Host)
	request = get_html_and_stcode(url)
	request_html = get_html(request)
	request_st_code = get_status_code(request)

	urls = get_only_url(request_html)
	# print(len(urls))
	# print(urls)
	url_stcode = {'url': url, 'status_code': request_st_code}
	list_of_stcode.append(url_stcode)
	# for i in urls:
	# 	print(i)
	# 	print('\n')
	print(url_stcode)
	print('\n')
	count = count + 1
	print(count)
	print('\n')

	# print(links_recursive)
	for link in urls:
		if link.startswith('/') and not link.startswith('//'):
			link = Host + link
		if link.startswith(Host) and link not in links:
			# print(link)
			links.add(link)
			links_recursive.append(link)
			# print(link)
			# print(str(len(links))+' links')
			# print(str(len(links_recursive))+' links_recursive')
			# print('\n')
	# print(links)
	# print(links_recursive)
	if maxdepth > 0:
		for link in links_recursive:
			get_all_links(link, maxdepth = maxdepth - 1)




def main():
	global count
	get_all_links(Host+Teacher_first_page)

	with open("statuscode.json", "w", encoding = "utf-8") as file:
		for i in list_of_stcode:
			json.dump(i, file, indent = 4)
		file.close()

			
		
	# for i in list_of_stcode:
	# 	print(i)
	for link in links:
		print(link)
	print(len(links))
	# print(links)
	# for link in links:
	# 	count = count + 1
	# 	print(link)
	# 	print(count)
	# 	print('\n')











if __name__ == '__main__':
	main()

print('--- %.3f seconds ---' % (time.time()-start_time))



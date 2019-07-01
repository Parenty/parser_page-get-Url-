#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup
import time
import lxml


start_time = time.time()
list_urls = []

Host = 'https://43059.shot-uchi.ru'
pages_to_parse = []
# parsed_pages = []
site_links = []
links = set()

def get_html_and_stcode(url):
	r = requests.get(url)
	a = [r.text, r.status_code]
	return a	
			#возвращает html-код страницы и статус код


def post_html_and_stcode(url):
	#url = "https://43059.shot-uchi.ru/"
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

	#print(r.text)
	a = [r.text, r.status_code]
	return a
	#print(a)



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

	# for i in list_urls:
	# 	if i.startswith('//') and not Host in i:
	# 		list_urls.remove(i)

	unique_urls = set(list_urls)

	return unique_urls


def get_first_page(Host):
	first_page_list = post_html_and_stcode(Host)
	first_page = get_html(first_page_list)
	first_st_code = get_status_code(first_page_list)
	pages_to_parse = []
	pages_to_parse = get_only_url(first_page)
	# print(pages_to_parse)
	# print('\n')
	# print(len(pages_to_parse))
	return pages_to_parse

def get_all_links(url, maxdepth = 1):
	
	links_recursive = []

	request = get_html_and_stcode(url)
	request_html = get_html(request)
	request_st_code = get_status_code(request)

	urls = get_only_url(request_html)
	# print(urls)


	# print(links_recursive)
	for link in urls:
		if link.startswith('/') and not link.startswith('//'):
			link = link + Host
		if link.startswith(Host) and link not in links:
			print(link)
			links.add(link)
			links_recursive.append(link)
			# print(links)
			# print(links_recursive)
	# print(links)
	# print(links_recursive)
	if maxdepth > 0:
		for link in links_recursive:
			get_all_links(link, maxdepth = maxdepth - 1)




def main():
	#loginbot('https://43059.shot-uchi.ru/')
	post_html_and_stcode(Host)
	get_first_page(Host)
	get_all_links(Host)
	# print(links)
	# for link in links:
	# 	print(link)
	
	# url = Host
	# main_page_list = post_html_and_stcode(url) #код страницы и статус-код
	# main_page = get_html(main_page_list) #код страницы
	# st_code = get_status_code(main_page_list) #статус-код
	# list_url = [url, st_code]
	# # print(list_url)
	# # print('\n')
	# main_pageurl = get_only_url(main_page)
	# #print(main_pageurl)

	# print(len(main_pageurl))
	# # print(main_pageurl)


	# for i in main_pageurl:
	# 	if i.startswith('/') and not i.startswith('//'):
	# 		i = Host+i
	# 	if not i.startswith(Host):
	# 		pass
	# 	else:
	# 	# else:
	# 	# 	pass
	# 	# if not 'uchi' in i:
	# 	# 	pass
	# 	# else:
	# 	#else:
	# 		#i=i
	# 		second_pages_list=get_html_and_stcode(i)
	# 		second_pages = get_html(second_pages_list)
	# 		second_stcode = get_status_code(second_pages_list)
	# 		second_url=get_only_url(second_pages)
	# 		# print(len(second_url))
	# 		list_url_2 = [i, second_stcode]
	# 		# print(i)
	# 		print(list_url_2) 
	# 		print('\n')
	# 		# print(len(second_url))

	# 		# for j in second_url:
	# 		# 	print(j)
	# 		# 	print('\n')









if __name__ == '__main__':
	main()

print('--- %.3f seconds ---' % (time.time()-start_time))



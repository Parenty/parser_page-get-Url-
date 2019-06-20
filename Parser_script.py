#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup
import time


start_time = time.time()

def get_html_and_stcode(url):
	r = requests.get(url)
	a = [r.text, r.status_code]
	return a	
			#возвращает html-код страницы и статус код


def loginbot():
	s = requests.Session()
	resp = s.get("https://43059.shot-uchi.ru/")
	html_text = resp.text
	token = re.search('(?<=\<meta name=\"csrf-token\" content=\")(.+)(?=\" />)', html_text)
	print(s.cookies.get_dict())
	#print(token)


	data = {#"utf8": '%E2%9C%93',
			"authenticity_token": token,
			#"next": '/home',
			"login": 'dmitriev@uchi.ru',
			"password": '123'
	 }

	r = s.post('https://43059.shot-uchi.ru/', data = data)

	#print(r.text)
	print(r.status_code)


"""
def get_html(page_andst):
	text_html = page_andst[0]
	return text_html


def get_status_code(page_andst):
	s_code = page_andst[1]
	return s_code


def get_only_url(html_page):
	only_url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', html_page)
	return only_url
"""
def main():
	loginbot()
	"""
	url = 'https://httpbin.org/'
	main_page_list = get_html_and_stcode(url) #код страницы и статус-код
	main_page = get_html(main_page_list) #код страницы
	st_code = get_status_code(main_page_list) #статус-код
	list_url = [url, st_code]
	print(list_url)
	print('\n')
	main_pageurl = get_only_url(main_page)

	for i in main_pageurl:
		second_pages_list=get_html_and_stcode(i)
		second_pages = get_html(second_pages_list)
		second_stcode = get_status_code(second_pages_list)
		second_url=get_only_url(second_pages)
		list_url_2 = [i, second_stcode]
		print(list_url_2) 
		print('\n')

		#for j in second_url:
				#print(j)
				#print('\n')







"""
if __name__ == '__main__':
	main()

print('--- %.3f seconds ---' % (time.time()-start_time))



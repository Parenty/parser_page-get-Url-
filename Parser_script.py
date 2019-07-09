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
count_while = 0
links_while = []

list_of_stcode = []
final_list = []
# check_list = []
# check_url = []


s = requests.Session()
resp = s.get(Host)
html_text = resp.text
token = (re.search('(?<=\<meta name=\"csrf-token\" content=\")(.+)(?=\" />)', html_text)).group()

data = {#"utf8": '%E2%9C%93',
			"authenticity_token": token,
			#"next": '/home',
			"login": 'dmitriev@uchi.ru',
			"password": '1'
	 }

r = s.post(Host, data = data)



# def post_html_and_stcode(url):

# 	s = requests.Session()
# 	resp = s.get(url)
# 	html_text = resp.text
# 	token = (re.search('(?<=\<meta name=\"csrf-token\" content=\")(.+)(?=\" />)', html_text)).group()


# 	data = {#"utf8": '%E2%9C%93',
# 			"authenticity_token": token,
# 			#"next": '/home',
# 			"login": 'dmitriev@uchi.ru',
# 			"password": '1'
# 	 }

# 	r = s.post(url, data = data)

	# return s

# s = post_html_and_stcode(Host)
def get_html_and_stcode(url):
	r2 = s.get(url, timeout = 30)
	# r = post_html_and_stcode(Host).get(url, timeout = 5)
	# r = requests.get(url, timeout = 5)
	a = [r2.text, r2.status_code]
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
	list_urls = []
	for i in soup.find_all('link', href = True): #ищу все ссылки с тэгом link
		link = str(i.get('href'))
		list_urls.append(link)

	for i in soup.find_all('a', href = True): #ищу все ссылки с тэгом a
		link = str(i.get('href'))
		list_urls.append(link)

		# достаю остальные ссылки (начинающиеся с http)
	only_url = re.findall('((?<=href=")([\/].+)(?= [\/]))', html_page)
	only_url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', html_page)
	for i in only_url:
		list_urls.append(i)

	# for i in list_urls:
	# 	if not i.startswith('/'):
	# 		list_urls.remove(i)


	# unique_urls = set(list_urls)

	return list_urls




def get_links_while(url):

	links_while = [url]

	global count_while

	# while count_while != 1:                   #len(links_while)

	for i in links_while:

		# count_while = count_while + 1

		if count_while == len(links_while):

			req = get_html_and_stcode(i)
			req_html = get_html(req)
			req_st_code = get_status_code(req)

			links_and_response = {"url": i, "status_code": req_st_code}
			final_list.append(links_and_response)

			print(links_and_response)
			print('\n')
			print(count_while)

			print("Все ссылки пройдены")

			return

		else:

			count_while = count_while + 1

			req = get_html_and_stcode(i)
			req_html = get_html(req)
			req_st_code = get_status_code(req)

			urls_while = get_only_url(req_html)

			links_and_response = {"url": i, "status_code": req_st_code}
			final_list.append(links_and_response)

			print(links_and_response)
			print('\n')
			print(count_while)

			for link in urls_while:

				if not '/logout' in link:

					if link.startswith('/') and not link.startswith('//'):
						link = Host + link

					if link.startswith(Host) and link not in links_while:
						links_while.append(link)






def get_all_links(url, maxdepth = 4): #maxdepth - глубина рекурсии. Для учи, рекомендую ставить "3" - основные урлы будут проверены

	global count
	
	links_recursive = []
	# s = post_html_and_stcode(Host)
	request = get_html_and_stcode(url)
	request_html = get_html(request)
	request_st_code = get_status_code(request)

	urls = get_only_url(request_html)
	# print(len(urls))
	# print(urls)
	url_stcode = {'url': url, 'status_code': request_st_code}
	list_of_stcode.append(url_stcode)

	# check_list.append(url_stcode)
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
		if not '/logout' in link:

			if link.startswith('/') and not link.startswith('//'):
				link = Host + link
			if link.startswith(Host) and link not in links and not link in links_recursive:
				# print(link)
				links.add(link)
				links_recursive.append(link)
				# print(link)
				# print(str(len(links))+' links')
				# print(str(len(links_recursive))+' links_recursive')
				# print('\n')
	# print(str(len(links))+' links')
	# print(str(len(links_recursive))+' links_recursive')
	if maxdepth > 0:
		# print(str(len(links_recursive))+' links_recursive')
		# print(str(len(links))+' links')
		for link in links_recursive:
			# check_url.append(link)
			get_all_links(link, maxdepth = maxdepth - 1)




def main():
	global count
	get_links_while(Host+Teacher_first_page)
	# get_all_links(Host+Teacher_first_page)
	# print(len(check_url))

	# with open("statuscode.json", "w", encoding = "utf-8") as file:
	# 	json.dump(list_of_stcode, file, indent = 4)
	# 	file.close()

	with open("statuscode.json", "w", encoding = "utf-8") as file:
		json.dump(final_list, file, indent = 4)
		file.close()

			
		
	# for i in list_of_stcode:
	# 	print(i)
	# for link in links:
	# 	print(link)
	# print(len(links))
	# print(links)
	# for link in links:
	# 	count = count + 1
		# print(link)
		# print(count)
		# print('\n')

	# print(len(check_list))
	# print(str(len(check_url))+ 'сколько урлов')










if __name__ == '__main__':
	main()

print('--- %.3f seconds ---' % (time.time()-start_time))



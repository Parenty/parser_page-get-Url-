#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup


def get_html(url):
	r = requests.get(url)
	return r.text	
			#возвращает html-код страницы


def main():
	s_1 = get_html('https://uchi.ru/')
	#print(s_1)
	parser = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', s_1)
	for i in parser:
		print(i) 
		print('\n')








if __name__ == '__main__':
	main()


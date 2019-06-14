import requests
from bs4 import BeautifulSoup


def get_html(url):
	r = requests.get(url)
	return r.text				#возвращает html-код страницы



def get_all_links(html):
	soup = BeautifulSoup(html, 'lxml')
	divs = soup.find('div', class_ = 'footer__link--wrap').find_all('a', class_='footer__link')
	liks = []

	for a in divs:
		href_a = a.find('a', class_ = 'footer__link').get('href') #string
		links.append(a)

	return links



def main():
	url='https://uchi.ru/'
	all_links = get_all_links(get_html(url))


	for i in all_liks:
		print(i)






if __name__ == '__main__':
	main()
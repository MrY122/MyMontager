import requests
from bs4 import BeautifulSoup as bs

Sources = ["https://www.cybersport.ru/search?kw=Minecraft"]

names = []
links = []
times = []
original_links = []

for i in range(len(Sources)):
	r = requests.get(Sources[i])
	html = bs(r.text, "html.parser")
	div = html.find("article", {"class":"search-results__news news"})
	block = div.find_all("a", {"class":"revers"})
	
	for elem in block:
		names.append(elem.text)

		link = "https://cybersport.ru" + str(elem.get("href"))
		links.append(link)

		#Начало парсинга каждой отдельной страницы
		new_r = requests.get(link)
		new_html = bs(new_r.text, "html.parser")

		time = new_html.find("time")
		times.append(time.text[:10])

		original_link = new_html.find("a", {"class":"btn btn--link color--gray-8a"})
		try:
			original_links.append(original_link.get("href"))
		except:
			original_links.append(None)

print(names)
print(links)
print(times)
print(original_links)
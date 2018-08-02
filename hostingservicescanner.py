from selenium import webdriver
import wget

#link - tu mozna okreslic ile wynikow ma byc pobranych, w ponizszym linku pobieranych jest 50
url = 'http://wrzucacz.pl/browse/0/0/10/1/all/date/desc/files.html'
#istniejaca baza plikow
files_list = 'linki.txt'

#filtry - rozszerzenia plikow, ktore nas nie interesuja
exclude = ['.mp3','.torrent','.jpg','.jpeg','.png','.mp4','.avi','files.html','.JPG','.mid','.gif']

#ustawienie przegladarki headless
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options)

#tworzenie listy wszystkich linkow ze strony
def links (elements):
	links = []
	for element in elements:
		temp = element.get_attribute("href")
		if not temp in links:
			links.append(temp)
	return (links)

#filtrowanie linkow na podsatwie listy exclude
def filter_res(links):
	links_clean = []
	for link in links:
		if not any ([excl in link for excl in exclude]):
			links_clean.append(link)
	return (links_clean)

#jesli sa nowe pliki - pobranie & wpis na koncu bazy plikow:
def new_files(check):	
	with open(files_list,"a") as myfile:
		for i in check:
			wget.download(i,"./wrzucacz")
			myfile.write(i+'\n')	
	myfile.close()



def main():
	driver.get(url)
	elements = driver.find_elements_by_css_selector("a[href*=%s]" % 'file')
	link_list = links(elements)
	driver.close()
	filtered = filter_res(link_list)
	file_old = open(files_list).read().splitlines()
	check = list(set(filtered) -set(file_old))
	if check:
		new_files(check)

if __name__=="__main__":
	main()




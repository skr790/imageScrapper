#!/usr/bin/python3
from bs4 import BeautifulSoup as soup
from urllib.parse import urljoin
import os,re,requests,sys
#debg=open("debug_ImgScrap.txt","a")

#function to remove thumbnails
def cleanup(path):
	os.chdir(path)
	print ("Cleaning Up in:{}"+path) 
	files = os.listdir()
	for fl in files:
		if os.stat(fl).st_size < 1500 and os.path.isfile(fl):
			os.remove(fl)



#downloads url(s) to specified path
def download(urls,path):

	if not os.path.exists(path):
		os.makedirs(path)


	for url in urls:
	
		filename=url.split('/')[-1]

		print ("Downloading {}".format(url))
		#url=re.sub(r'thumb.','',url)
		data=requests.get(url)
		
		file=open(path+"/"+filename,"wb")
		for chunk in data.iter_content(chunk_size=2048):
			if chunk:
				file.write(chunk)
		file.close()

	cleanup(path)

#main driver...very IMP
def scrap(url,dirr):
	preurl=re.sub(url.split("/")[-1],"",url)
	page=requests.get(url)
	html=soup(page.text,"html.parser")
	images=html.findAll('img')
	imglinks=[]
	for img in images:
		imglinks.append(urljoin(url,img.get("src")))
		#debg.write(urljoin(url,img.get("src"))+"\n")

	#debg.close
	imglinks=set(imglinks)
	subpath=re.sub('[^A-Za-z0-9]+','',url.split('/')[2])[:9]
	download(imglinks,dirr+"/imageScrapper/"+subpath)

def main():	
	url=input("enter url:")
	print("You are working in:"+os.getcwd())
	dirr=input("Enter dir to Dump:")
	scrap(url,dirr)


if __name__ == "__main__":main()

import re, urllib
import pandas as pd
from bs4 import BeautifulSoup
from subprocess import call

query = "tujko+jo+paaya+original+hd+youtube"

def get_youtube_link(query):
	site = urllib.request.urlopen("http://duckduckgo.com/html/?q="+query)
	data = site.read()
	soup = BeautifulSoup(data, "html.parser")

	my_list = soup.find("div", {"id": "links"}).find_all("div", {'class': re.compile('.*web-result*.')})[0:15]

	(result__snippet, result_url) = (list() for i in range(2))

	for i in my_list:         
		try:
		    result_url.append(i.find("a", {"class": "result__url"}).get_text().strip("\n").strip())
		except:
		    result_url.append(None)
		if result_url:
			break

	return ("https://" + result_url[0])

def mp4_downloader(link, location):
	import ipdb; ipdb.set_trace()
	# command = "youtube-dl " + link +" -c"
	# -o "~/Desktop/%(title)s.%(ext)s"
	command = "youtube-dl -o" + location + " " + link +" -c"
	call(command.split(), shell=False)


link = get_youtube_link(query)
mp4_downloader(link, '/home/saurabh/Downloads/Videos/video.mp4')

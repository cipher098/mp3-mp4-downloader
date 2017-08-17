import os

import sys
import re, urllib
import pandas as pd
from bs4 import BeautifulSoup
from subprocess import call


def get_youtube_link(query):
	site = urllib.request.urlopen("http://duckduckgo.com/html/?q="+query+ '&t=hb&iax=1&ia=videos')
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
	command = "youtube-dl -o" + location + " " + link +" -c"
	call(command.split(), shell=False)


def mp3_downloader(link, location):
	command = "youtube-dl --extract-audio --audio-format mp3 --prefer-ffmpeg -o" + location + " " + link
	call(command.split(), shell=False)


def make_query(phrase):
	query = phrase.strip()
	query = query.replace("   ", " ")
	query = query.replace("  ", " ")
	query = query.replace(" ", "+")
	query = query + "+official+song+hd+youtube"
	return query	


def get_input(input_list):
	format = ''
	phrase = ''
	location = ''
	for a in input_list[1:]:
		if format == 'audio' or format == 'video':
			if a[0] == '/':
				location = a
				break
		elif a == '-a':
			format = 'audio'
		elif a == '-v':
			format = 'video'	
		else:
			phrase = phrase + a + ' '


	if not location:
		location = os.environ['HOME'] + '/Downloads'

	if location[-1] == '/':
		location = location[0:-1]

	if not format:
		format = 'audio'
	return (phrase, format, location)


def main():
	phrase, format, location = get_input(sys.argv)
	query = make_query(phrase)
	link = get_youtube_link(query)
	# print(query, link)
	# print (location)
	if format == 'video':
		mp4_downloader(link, location+'/%(title)s.%(ext)s')
	else:
		mp3_downloader(link, location+'/%(title)s.%(ext)s')


if __name__ == "__main__":
	main()

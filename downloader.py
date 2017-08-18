import os
import sys
import re, urllib
import youtube_dl
import pandas as pd
# from bs4 import BeautifulSoup
# from subprocess import call
from google import search


# def get_youtube_link(query):
#   site = urllib.request.urlopen("http://duckduckgo.com/html/?q=" +query+ '&t=hb&iax=1&ia=videos')
#   data = site.read()
#   soup = BeautifulSoup(data, "html.parser")

#   my_list = soup.find("div", {"id": "links"}).find_all("div", {'class': re.compile('.*web-result*.')})[0:15]

#   (result__snippet, result_url) = (list() for i in range(2))

#   for i in my_list:         
#       try:
#           result_url.append(i.find("a", {"class": "result__url"}).get_text().strip("\n").strip())
#       except:
#           result_url.append(None)
#       if result_url:
#           break

#   return ("https://" + result_url[0])


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


def get_youtube_link(query):
    link = search(query, tld="co.in", num=1, stop=1, pause=2)
    for j in link:
        return j

def mp4_downloader(link, location):
    # command = "youtube-dl -o" + location + " " + link +" -c"
    # call(command.split(), shell=False)
    ydl_opts = {
    'outtmpl' : location + '/%(title)s.%(ext)s',
    'progress_hooks': [my_hook],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])


def mp3_downloader(link, location):
    # command = "youtube-dl --extract-audio --audio-format mp3 --prefer-ffmpeg -o" + location + " " + link
    # call(command.split(), shell=False)
    ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],      
    'outtmpl': location + '%(title)s.%(ext)s',
    'noplaylist' : True,
    'prefer_ffmpeg' : True,
    'progress_hooks': [my_hook],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])


def make_query(phrase):
    query = phrase.strip()
    query = query.replace("   ", " ")
    query = query.replace("  ", " ")
    # query = query.replace(" ", "+")
    # query = query + "+original+version+song+hd+youtube"
    query = query + "original version song hd youtube"
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
    if format == 'video':
        mp4_downloader(link, location+'/%(title)s.%(ext)s')
    else:
        mp3_downloader(link, location+'/%(title)s.%(ext)s')


if __name__ == "__main__":
    main()

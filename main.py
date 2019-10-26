from __future__ import unicode_literals
import sys
import spotipy # awesome wrapper for Spotify
import spotipy.util as util

import os



def convert2MP3():

	script_path = os.getcwd()
	directory = os.path.join(script_path, "Downloaded")


	for root, dirs, files in os.walk(directory):
		
		for file in files:

			src = os.path.join(directory,str(file))
			tmp = str(file)[:-4]
			filename = tmp+".mp3"
			dst = os.path.join(directory,filename)

			os.rename(src,dst)

def setMetadata(filepath, artist, album, title):

	audio = EasyID3(filepath)

	audio['artist'] = artist
	audio['title'] = title
	audio['album'] = album

	audio.save()
    


def downloader(link, filename):

	import youtube_dl

	# This downloads a list of youtube links

	problem = "./&%-"

	for each in problem:
		if each in filename:
			filename = filename.replace(each,"")

	ydl_opts = {
	    'format': 'bestaudio/best',
	    'outtmpl': "/Downloaded/"+filename+".%(ext)s",
	    'postprocessors': [{
	        'key': 'FFmpegExtractAudio',
	        'preferredcodec': 'mp3',
	        'preferredquality': '128',
	    }],
	}


	with youtube_dl.YoutubeDL(ydl_opts) as ydl:

		try:
			ydl.download([link])
			print(filename + ' is downloaded!')

		except:
			pass	








def searchYoutube(trackName, artist):

	import urllib.request
	import urllib.parse
	import re

	
	query = trackName + artist
	query_string = urllib.parse.urlencode({"search_query" : query})
	html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
	search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())

	# this regex was lifted from this cool bloke's page: 
	# https://www.codeproject.com/Articles/873060/Python-Search-Youtube-for-Video

	
	link = "http://www.youtube.com/watch?v=" + search_results[0]

	downloader(link,trackName+' by '+artist)
	


scope = 'user-top-read'
songList, links = [], []

username = input("Enter Your Spotify Username: ")


token = util.prompt_for_user_token(username, scope, client_id="87b136708f154032b21b7f3e618867a2",\
													client_secret="e114dac3aeb94e83b68e601209af778b",\
													redirect_uri="http://localhost:8080/callback")

if token:
	sp = spotipy.Spotify(auth=token)
	results = sp.current_user_top_tracks(limit=20,time_range='short_term')
	
	for item in results['items']:

		artist = item['artists'][0]['name']
		trackName = item['name']
		song = (trackName, artist)

		print(song)

		songList.append(song)


else:
	print("Can't get token for "+username)	    	

for song in songList:

	searchYoutube(song[0],song[1])


print("Please wait while I convert it to mp3!")

convert2MP3()

print("\n\n\n\n\n\nFinished! Please check the folder in the current directory.")	




# !/bin/sh

read -p 'Song: ' song
read -p 'Format(Press a for audio and v for video): ' song_type
read -p 'Location: ' location

if [ ${song_type:-a} == 'v' ]
then
	song_type=video
	a_or_v=-v
else
	song_type=audio
	a_or_v=-a
fi

if [ "${location:-0}" == 0 ];then
	location=$HOME/Downloads/
fi

# Cannot download song without phrase.
while [ "${song:-0}" == 0 ]
do
	read -p 'Phrase of song not given try again: ' song
done

source ~/youtubeDownloader/youtubeDownloader_env/bin/activate
python ~/youtubeDownloader/mp3-mp4-downloader/downloader.py $song $a_or_v $location
deactivate

# !/bin/sh

virtualenv -p python3 ~/youtubeDownloader/youtubeDownloader_env
source ~/youtubeDownloader/youtubeDownloader_env/bin/activate
pip install youtube-dl
pip install pandas
pip install google
deactivate

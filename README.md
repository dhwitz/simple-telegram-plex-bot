# simple-telegram-plex-bot

Used to download files to qbittorrent through a telegram bot.

Requires the qbittorrent web interface to be enabled to port 8081.

Send the bot a magnet link and it will download it and then notify you when your download completes.

There are also several commands:
* /status - shows the number of things downloading and in queue
* /queue - shows a list of all items in the queue
* /delete - deletes a currenty downloading item by name
* /anime - send the media to a different folder

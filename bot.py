import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
from qbittorrent import Client

update_id = None
current_queue = {}

def main():
    """Run the bot."""
    global update_id
    # Telegram Bot Authorization Token

    bot = telegram.Bot('______________') #token goes here

    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            bit(bot)
            sendUpdates(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1

def sendUpdates(bot):
    global current_queue
    temp = gettorrents()
    hashlist = []
    for dictn in temp:
        hashlist.append(dictn['hash'])
    for hashes in list(current_queue):
        if hashes not in hashlist:
            bot.sendMessage(current_queue[hashes][0], "Your download '" + current_queue[hashes][1] + "' has finished.")
            current_queue.pop(hashes)

def gettorrents():
    torrentlist = []
    qb = Client('http://127.0.0.1:8081/')
    temp = qb.torrents()
    for dictn in temp:
        torrentlist.append({ 'name' : "Torrent Name: " + dictn['name'], 'progress' : "Progress: " + "{:.1%}".format(dictn['progress']), 'state' : "State: " + dictn['state'], 
                            'hash' : dictn['hash'], 'eta' : "ETC: " + str(dictn['eta']//60) + " minutes"})
    return torrentlist
def bit(bot):
    global update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

        if update.message:          
            if update.message.text == None:
                continue

            if 'magnet:?' in update.message.text:
                qb = Client('http://127.0.0.1:8081/')
                qb.download_from_link(update.message.text)
                temp = qb.torrents()
                for dictn in temp:
                    if dictn['hash'] not in current_queue:
                        current_queue[dictn['hash']] = [update.message.chat_id, dictn['name']]
                update.message.reply_text("Torrent has been added to the list.")


            if update.message.text == "/status":
                temp = gettorrents()
                queue = 0
                downloading = 0
                
                for item in temp:
                    if item['state'] == ("State: " + 'downloading'):
                        downloading += 1
                    if item['state'] == ("State: " + 'queuedDL'):
                        queue += 1
                update.message.reply_text(str(len(temp)) + "/20 torrents are active.\n" + str(downloading) +"/5 are downloading, and " + str(queue) + "/15 are in the queue.")
            
            
            if update.message.text == "/queue":
                temp = gettorrents()
                tempstring = "Current Active Torrents:\n \n"
                for dictn in temp:       
                    tempstring += dictn['name'] + '\n'
                    tempstring += dictn['eta'] + ", " + dictn['progress'] + ", " + dictn['state'] + "\n" + "\n"
                update.message.reply_text(tempstring)
                
            if "/delete" in update.message.text:
                temp = gettorrents()
                for item in temp:
                    if item['name'] == ("Torrent Name: "  + update.message.text[8:]):
                        qb = Client('http://127.0.0.1:8081/')
                        qb.delete_permanently(item['hash'])
                        current_queue.pop(item['hash'])
                temp = gettorrents()
                tempstring = "Current Active Torrents:\n \n"
                for dictn in temp:         
                    tempstring += dictn['name'] + '\n'
                    tempstring += dictn['eta'] + ", " + dictn['progress'] + ", " + dictn['state'] + "\n" + "\n"
                update.message.reply_text(tempstring)
if __name__ == '__main__':
    while True:
        try:
            main()
        except:
            continue
        

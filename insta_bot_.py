from instagrapi import Client
import json, csv, asyncio
from telebot.async_telebot import AsyncTeleBot
from telebot import types


bot = AsyncTeleBot('5619487724:AAFeBptlX1aJ9IEAFLMUXN3JZBImJ35quWk') 

audit = []
index_list = []

def info_photo(link):
    like = []
    comment = []
    cl = Client()
    cl.login('oleks3099', '!P^#5s^*g7&')
    media_id = cl.media_pk_from_url(link)
    likes = cl.media_likers(media_id)
    comments = cl.media_comments(media_id, 0)
    for i in range(len(likes)):
        people_like = likes[i].dict()['username']
        like.append(people_like)
    for i in range(len(comments)):
        text_comments = comments[i].dict()['text']
        comment.append(text_comments)
    return [like, comment]


def write_csv(list_like_comment, name_file):
    list_csv = [["People who liked", "Comments"]]
    count_like = len(list_like_comment[0])
    count_comment = len(list_like_comment[1])
    difference = count_like-(count_like-count_comment)
    list_del_like = list_like_comment[0][difference:]
    for like, comment in zip(list_like_comment[0], list_like_comment[1]):
        like_comment = [like, comment]
        list_csv.append(like_comment)
    for i in range(len(list_del_like)):
        not_used_like = [list_del_like[i], '']
        list_csv.append(not_used_like)
    with open(f'instagram{name_file}.csv', 'w') as data:
        writer = csv.writer(data)
        for row in list_csv:
            writer.writerow(row)


@bot.message_handler(commands=['start']) 
async def start(message):
    audit.append([str(message.chat.id)])
    index_list.append(str(message.chat.id))
    index_list.append(int(len(audit)-1))  
    await bot.send_message(message.chat.id, f'Hello {message.from_user.first_name} send me link')
    audit[index_list[index_list.index(str(message.chat.id)) + 1]].append('status_link')

@bot.message_handler(content_types=['text']) 
async def text(message):
    if audit[index_list[index_list.index(str(message.chat.id)) + 1]][1] == 'status_link' and 'https://www.instagram.com' in message.text:
        try:
            await bot.send_message(message.chat.id, 'Processing please wait a minute and also please do not send any more links')
            write_csv(info_photo(message.text), audit[index_list[index_list.index(str(message.chat.id)) + 1]][0])
            await bot.send_document(message.chat.id, open(f'instagram{audit[index_list[index_list.index(str(message.chat.id)) + 1]][0]}.csv', 'rb'))
        except:
            await bot.send_message(message.chat.id, 'You sent the wrong link to the image or try again')


while True:
    try:
        asyncio.run(bot.polling(non_stop=True, interval=1, timeout=0))
    except KeyboardInterrupt:
        exit()
    except Exception:
        time.sleep(5)

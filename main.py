import telethon
import time
import asyncio
import os, sys
import re
import requests
from telethon import TelegramClient, events
#from random_address import real_random_address
import names
from datetime import datetime
import random
from keep_alive import live
from defs import getUrl, getcards, phone

# The API ID and API Hash of your Telegram app. You can get it from my.telegram.org.
API_ID = 25667398 # api_id
API_HASH = '5d0918b44383d0410074c3dcdcb2dd26' #Api_hash
SEND_CHAT = '@bin_scrapper' # يوزر القناه او الشات 

# Creating a new TelegramClient instance, and then creating an empty list.
client = TelegramClient('session', API_ID, API_HASH)
ccs = []

# It's a list of chats that you want to listen to.
chats = [
  '@bin_scrapper'
]
#ذي قنوات جاهزه تبي تزيد من عندك زيد هنا
# It's reading the file and splitting it into lines.
with open('cards.txt', 'r') as r:
  temp_cards = r.read().splitlines()

# It's getting the cards from the file and adding them to the list.

for x in temp_cards:
  car = getcards(x)
  if car:
    ccs.append(car[0])
  else:
    continue


@client.on(events.NewMessage(chats=chats, func=lambda x: getattr(x, 'text')))
async def my_event_handler(m):
  if m.reply_markup:
    text = m.reply_markup.stringify()
    urls = getUrl(text)
    if not urls:
      return
    text = requests.get(urls[0]).text
  else:
    text = m.text
  cards = getcards(text)
  if not cards:
    return
  cc, mes, ano, cvv = cards
  if cc in ccs:
    return
  ccs.append(cc)
  bin = requests.get(f'https://projectslost.xyz/bin/?bin={cc}')
  extra = cc[0:0 + 12]
  if not bin:
    return
  bin_json = bin.json()
  #datab = bin_json['data']
  binl = bin_json["query"]
  typeq = bin_json["type"]
  #vendor = bin_json['vendor']
  level = bin_json["level"]
  bank = bin_json["bank"]["name"]
  country = bin_json["country"]["name"]
  emoji = bin_json["country"]["flag"]
  code = bin_json["country"]["ISO2"]

  fotoweb = 'https://d.top4top.io/p_2628ixtn21.jpg'

  fullinfo = f"{cc}|{mes}|{ano}|{cvv}"

  text = f"""
➳ BIN SCRAPPER
╰─˖*════════ ♕么♕════════

➳: 💳𝑪𝑪: **`{cc}|{mes}|{ano}|{cvv}`**

➳: 🌟𝘽𝙄𝙉: **`{binl}`**

➳: ⚜️𝑰𝑵𝑭𝑶: **`{typeq} - {level}`**

➳:🏦𝑩𝑨𝑵𝑲: **`{bank}`**

➳:🗺𝑪𝑶𝑼𝑵𝑻𝑹𝒀: **`{country} - {emoji} - {code}`**

➳:⚙️`{extra}xxxx|{mes}|{ano}|rnd`


╰─˖*════════ ♕么♕════════
"""

  print(f'{cc}|{mes}|{ano}|{cvv} - Aprovada [a+]')
  with open('scrap.txt', 'a') as w:
    w.write(fullinfo + '\n')
  await client.send_message(SEND_CHAT,
                            text,
                            link_preview=False,
                            file='scrap.jpg')
  await asyncio.sleep(38)


@client.on(events.NewMessage(outgoing=True, pattern=re.compile(r'.lives')))
async def my_event_handler(m):
  # emt = await client.get_entity(1582775844)
  # print(telethon.utils.get_input_channel(emt))
  # print(telethon.utils.resolve_id(emt))
  await m.reply(file='cards.txt')# الملف اللي ينحفظ فيه السكراب اللي ينزل بلقناه


live()
client.start()
client.run_until_disconnected
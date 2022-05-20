import asyncio
import re
import datetime

from telethon import events, custom
from datetime import datetime
from EmikoRobot import telethn as bot
from EmikoRobot.events import register


edit_time = 5
""" =======================Kobo Kanaeru====================== """
file1 = "https://telegra.ph/file/fccf074e6d1b333c635e8.jpg"
file2 = "https://telegra.ph/file/79c74ae56bb5a59511727.jpg"
file3 = "https://telegra.ph/file/958b115b91dc56437de7f.jpg"
file4 = "https://telegra.ph/file/7bcc93bff54ec80184d59.jpg"
file5 = "https://telegra.ph/file/ce349a523b465ebcc0e43.jpg"
""" =======================Kobo Kanaeru====================== """

@register(pattern="/myinfo")
async def proboyx(event):
    chat = await event.get_chat()
    current_time = datetime.utcnow()
    betsy = event.sender.first_name
    button = [[custom.Button.inline("Click Here",data="information")]]
    on = await bot.send_file(event.chat_id, file=file2,caption= f"♡ Hey {betsy}, I'm Kobo Kanaeru\n♡ I'm Created By Ako & Human\n♡ Click The Button Below To Get Your Info", buttons=button)

    await asyncio.sleep(edit_time)
    ok = await bot.edit_message(event.chat_id, on, file=file3, buttons=button) 

    await asyncio.sleep(edit_time)
    ok2 = await bot.edit_message(event.chat_id, ok, file=file5, buttons=button)

    await asyncio.sleep(edit_time)
    ok3 = await bot.edit_message(event.chat_id, ok2, file=file1, buttons=button)

    await asyncio.sleep(edit_time)
    ok7 = await bot.edit_message(event.chat_id, ok6, file=file4, buttons=button)

    await asyncio.sleep(edit_time)
    ok4 = await bot.edit_message(event.chat_id, ok3, file=file2, buttons=button)

    await asyncio.sleep(edit_time)
    ok5 = await bot.edit_message(event.chat_id, ok4, file=file1, buttons=button)

    await asyncio.sleep(edit_time)
    ok6 = await bot.edit_message(event.chat_id, ok5, file=file3, buttons=button)

    await asyncio.sleep(edit_time)
    ok7 = await bot.edit_message(event.chat_id, ok6, file=file5, buttons=button)

    await asyncio.sleep(edit_time)
    ok7 = await bot.edit_message(event.chat_id, ok6, file=file4, buttons=button)

@bot.on(events.callbackquery.CallbackQuery(data=re.compile(b"information")))
async def callback_query_handler(event):
  try:
    boy = event.sender_id
    PRO = await bot.get_entity(boy)
    NEKO = "YOUR DETAILS BY KOBO\n\n"
    NEKO += f"FIRST NAME : {PRO.first_name} \n"
    NEKO += f"LAST NAME : {PRO.last_name}\n"
    NEKO += f"YOU BOT : {PRO.bot} \n"
    NEKO += f"RESTRICTED : {PRO.restricted} \n"
    NEKO += f"USER ID : {boy}\n"
    NEKO += f"USERNAME : {PRO.username}\n"
    await event.answer(NEKO, alert=True)
  except Exception as e:
    await event.reply(f"{e}")

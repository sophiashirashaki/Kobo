from bs4 import BeautifulSoup
import urllib
import glob
import io
import os
import re
import aiohttp
import urllib.request
from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup
from PIL import Image
from search_engine_parser import GoogleSearch

import bs4
import html2text
from bing_image_downloader import downloader
from telethon import *
from telethon.tl import functions
from telethon.tl import types
from telethon.tl.types import *

from EmikoRobot import *

from EmikoRobot.events import register
from EmikoRobot import telethn as tbot

opener = urllib.request.build_opener()
useragent = "Mozilla/5.0 (Linux; Android 9; SM-G960F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36"
opener.addheaders = [("User-agent", useragent)]


@register(pattern="^/google (.*)")
async def _(event):
    if event.fwd_from:
        return

    webevent = await event.reply("searching........")
    match = event.pattern_match.group(1)
    page = re.findall(r"page=\d+", match)
    try:
        page = page[0]
        page = page.replace("page=", "")
        match = match.replace("page=" + page[0], "")
    except IndexError:
        page = 1
    search_args = (str(match), int(page))
    gsearch = GoogleSearch()
    gresults = await gsearch.async_search(*search_args)
    msg = ""
    for i in range(len(gresults["links"])):
        try:
            title = gresults["titles"][i]
            link = gresults["links"][i]
            desc = gresults["descriptions"][i]
            msg += f"❍[{title}]({link})\n**{desc}**\n\n"
        except IndexError:
            break
    await webevent.edit(
        "**Search Query:**\n`" + match + "`\n\n**Results:**\n" + msg, link_preview=False
    )


@register(pattern="^/image (.*)")
async def img_sampler(event):
    if event.fwd_from:
        return

    query = event.pattern_match.group(1)
    jit = f'"{query}"'
    downloader.download(
        jit,
        limit=4,
        output_dir="store",
        adult_filter_off=False,
        force_replace=False,
        timeout=60,
    )
    os.chdir(f'./store/"{query}"')
    types = ("*.png", "*.jpeg", "*.jpg")  # the tuple of file types
    files_grabbed = []
    for files in types:
        files_grabbed.extend(glob.glob(files))
    await tbot.send_file(event.chat_id, files_grabbed, reply_to=event.id)
    os.chdir("/app")
    os.system("rm -rf store")


opener = urllib.request.build_opener()
useragent = "Mozilla/5.0 (Linux; Android 9; SM-G960F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36"
opener.addheaders = [("User-agent", useragent)]


@register(pattern=r"^/reverse(?: |$)(\d*)")
async def okgoogle(img):
    """For .reverse command, Google search images and stickers."""
    if os.path.isfile("okgoogle.png"):
        os.remove("okgoogle.png")

opener = urllib.request.build_opener()
useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.68"
opener.addheaders = [("User-agent", useragent)]


async def reverse(update: Update, context: CallbackContext):
    msg = update.effective_message
    chat_id = update.effective_chat.id
    rtmid = msg.message_id
    imagename = "googlereverse.png"

    if os.path.isfile(imagename):
        os.remove(imagename)

    if reply := msg.reply_to_message:
        if reply.sticker:
            file_id = reply.sticker.file_id
        elif reply.photo:
            file_id = reply.photo[-1].file_id
        elif reply.document:
            file_id = reply.document.file_id
        else:
             await msg.reply_text("Reply To An Image Or Sticker To Lookup!")
             return

        image_file = await context.bot.get_file(file_id)
        image_file.download(imagename)
    else:
        await msg.reply_text(
            "Please Reply To A Sticker, Or An Image To Search It!", parse_mode=ParseMode.MARKDOWN,
        )
        return

    MsG = await context.bot.send_message(chat_id,
                                   "Let Me See...",
                                   reply_to_message_id=rtmid,
    )
    try:
        searchUrl = "https://www.google.com/searchbyimage/upload"
        multipart = {
            "encoded_image": (imagename, open(imagename, "rb")),
            "image_content": "",
        }
        response = requests.post(searchUrl, files=multipart, allow_redirects=False)
        fetchUrl = response.headers.get("Location")

        os.remove(imagename)
        if response != 400:
            MsG.edit_text("Downloading...")
        else:
            MsG.edit_text("Google Told Me To Go Away...")
            return

        match = ParseSauce(f"{fetchUrl}&hl=en")
        guess = match.get("best_guess")
        MsG.edit_text("Uploading...")
        if match.get("override") and (
            match.get("override") != "" or match.get("override") is not None
        ):
            imgspage = match.get("override")
        else:
            imgspage = match.get("similar_images")

        buttuns = []
        if guess:
            MsG.edit_text("Hmmm....")
            search_result = guess.replace("Possible related search: ", "")
            buttuns.append([InlineKeyboardButton(text="Images Link", url=fetchUrl)])
        else:
            MsG.edit_text("Couldn't Find Anything!")
            return

        if imgspage:
            buttuns.append([InlineKeyboardButton(text="Similar Images", url=imgspage)])

        MsG.edit_text("*Search Results*: \n\n`{}`".format(search_result),
                      parse_mode=ParseMode.MARKDOWN,
                      reply_markup=InlineKeyboardMarkup(buttuns),
        )

    except BadRequest as Bdr:
        MsG.edit_text(f"ERROR! - _Couldn't Find Anything!!_ \n\n*Reason*: BadRequest!\n\n{Bdr}", parse_mode=ParseMode.MARKDOWN)
    except TelegramError as Tge:
        MsG.edit_text(f"ERROR! - _Couldn't Find Anything!!_ \n\n*Reason*: TelegramError!\n\n{Tge}", parse_mode=ParseMode.MARKDOWN)
    except Exception as Exp:
        MsG.edit_text(f"ERROR! - _Couldn't Find Anything!!_ \n\n*Reason*: Exception!\n\n{Exp}", parse_mode=ParseMode.MARKDOWN)


def ParseSauce(googleurl):
    source = opener.open(googleurl).read()
    soup = BeautifulSoup(source, "html.parser")

    results = {"similar_images": "", "override": "", "best_guess": ""}

    try:
        for bess in soup.findAll("a", {"class": "PBorbe"}):
             url = "https://www.google.com" + bess.get("href")
             results["override"] = url
    except:
        pass

    for similar_image in soup.findAll("input", {"class": "gLFyf"}):
         url = "https://www.google.com/search?tbm=isch&q=" + urllib.parse.quote_plus(similar_image.get("value"))
         results["similar_images"] = url

    for best_guess in soup.findAll("div", attrs={"class": "r5a77d"}):
         results["best_guess"] = best_guess.get_text()

    return results
   

@register(pattern="^/app (.*)")
async def apk(e):

    try:
        app_name = e.pattern_match.group(1)
        remove_space = app_name.split(" ")
        final_name = "+".join(remove_space)
        page = requests.get(
            "https://play.google.com/store/search?q=" + final_name + "&c=apps"
        )
        lnk = str(page.status_code)
        soup = bs4.BeautifulSoup(page.content, "lxml", from_encoding="utf-8")
        results = soup.findAll("div", "ZmHEEd")
        app_name = (
            results[0].findNext("div", "Vpfmgd").findNext("div", "WsMG1c nnK0zc").text
        )
        app_dev = results[0].findNext("div", "Vpfmgd").findNext("div", "KoLSrc").text
        app_dev_link = (
            "https://play.google.com"
            + results[0].findNext("div", "Vpfmgd").findNext("a", "mnKHRc")["href"]
        )
        app_rating = (
            results[0]
            .findNext("div", "Vpfmgd")
            .findNext("div", "pf5lIe")
            .find("div")["aria-label"]
        )
        app_link = (
            "https://play.google.com"
            + results[0]
            .findNext("div", "Vpfmgd")
            .findNext("div", "vU6FJ p63iDd")
            .a["href"]
        )
        app_icon = (
            results[0]
            .findNext("div", "Vpfmgd")
            .findNext("div", "uzcko")
            .img["data-src"]
        )
        app_details = "<a href='" + app_icon + "'>📲&#8203;</a>"
        app_details += " <b>" + app_name + "</b>"
        app_details += (
            "\n\n<code>Developer :</code> <a href='"
            + app_dev_link
            + "'>"
            + app_dev
            + "</a>"
        )
        app_details += "\n<code>Rating :</code> " + app_rating.replace(
            "Rated ", "⭐ "
        ).replace(" out of ", "/").replace(" stars", "", 1).replace(
            " stars", "⭐ "
        ).replace(
            "five", "5"
        )
        app_details += (
            "\n<code>Features :</code> <a href='"
            + app_link
            + "'>View in Play Store</a>"
        )
        app_details += "\n\n===> [Kobokan](https://t.me/KoboKanaeru_Robot) <==="
        await e.reply(app_details, link_preview=True, parse_mode="HTML")
    except IndexError:
        await e.reply("No result found in search. Please enter **Valid app name**")
    except Exception as err:
        await e.reply("Exception Occured:- " + str(err))


__mod_name__ = "Search"

__help__ = """
❂ /google <query>*:* Perform a google search
❂ /image <query>*:* Search Google for images and returns them\nFor greater no. of results specify lim, For eg: `/img hello lim=10`
❂ /app <appname>*:* Searches for an app in Play Store and returns its details.
❂ /reverse: Does a reverse image search of the media which it was replied to.
❂ /gps <location>*:* Get gps location.
❂ /github <username>*:* Get information about a GitHub user.
❂ /country <country name>*:* Gathering info about given country
❂ /imdb <Movie name>*:* Get full info about a movie with imdb.com
❂ Kobo <query>*:* Kobokan answers the query

  💡Ex: `Kobo where is Japan?`
"""

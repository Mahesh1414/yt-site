import os, datetime, sys, json
from pyrogram.types import ReplyKeyboardMarkup


x = datetime.datetime.utcnow()
i = x + datetime.timedelta(hours=3)
y = i.strftime("%Y-%m-%d_%I:%M%P")
print(y)
print("My PID is:", os.getpid())


stk0 = "CAADBAADrgcAAnILQFPgjUtxHDj-oQI"
stk1 = "CAADBAADlQoAAo8RQFOWkvFydBKJlwI"
stk2 = "CAADBAADSAsAAn_eOFPurvLfXO2hzAI"
stk3 = "CAADBAAD0QoAAkKSOFND8vqd0dBlhQI"
stk4 = "CAADBAADRgkAAhzwOFMQTCV2uQABp4wC"
stk5 = "CAADBAADHwoAAgTjOFPwcaIN8VE3uQI"
stk6 = "CAADBAAD2AgAAv1sOFOBvhMuUqdpVgI"
stk7 = "CAADBAAD_AkAAzI4U1zm0zS8ZmfzAg"
stk8 = "CAADBAADZQoAAvmvQFN_0Kq6nbL7IAI"
fthl = "CAACAgEAAxkBAAEDhMhhv1eWCc2bLbg8V5ZW2w7v5lVz0QAClQEAAjT0-UWjXL_zWuG_FiME"

start_msg0 = "Hi human,"
start_msg1 = "I am very fast **YOUTUBE DOWNLOADER** from @bryllbots \n\nI can download youtube video and youtube music from link very fast\n\nJust send any youtube link and grab a coffee till.\n\nSupport Group :- @bryllbots_support"

help_text = """ Hi %s,

Welcome to **@bryll_youtubedl_bot** 👋

I can download youtube/youtube music links with instant speed
just send a link and grab a coffee

🔴🔴 **Notes** 🔴🔴
┏━━━━━━━━━━━━━━━━━━━━━━
• **Bot** is completely free for use,
• So please don't abuse/spam the bot
• After **Download Finshes** you can save to your downloads directory,
• Directly by long pressing a song then **Click save to Downloads**
• Reply to **/report** to report any bugs
• Make sure you report the error link too
• Check out **/about**
┗━━━━━━━━━━━━━━━━━━━━━━━

** ⚠️ REPORT any bugs at @bryllbots_support ⚠️ **"""

about_text = """
╭────[🔅YᴏᴜᴛᴜʙᴇDL Bᴏᴛ🔅]───⍟
│
├<b>🤖 Bot Name : <a href='https://t.me/bryll_youtubedl_bot'>YoutubeDL Bot</a></b>
│
├<b>📢 Channel : <a href='https://t.me/bryllbots'>BRYLL BOTS</a></b>
│
├<b>💢 Source : <a href='https://t.me/bryllbots'>Click Here</a></b>
│
├<b>🌐 Server : <a href='https://heroku.com'>Heroku</a></b>
│
├<b>📕 Library : <a href='https://github.com/pyrogram'>Pyrogram 1.2.8</a></b>
│
├<b>㊙ Language: <a href='https://www.python.org'>Python 3.9.4</a></b>
│
├<b>👨‍💻 Developer : BRYLL CODERS</b>
│
╰──────[Thanks 😊]───⍟"""

msg0 = "**Fetching Link...**"
msg1=  "**Sorry But I can't get this link for you** (private content)"
msg2 = "**Downloading.....**"
msg3 = "**Download Finished**\n\n**Uploading**......"
msg4 = "**Please choose a Video format** you would like to download\n\nChoose Formats without Audio, If you want a Higher Audio quality"
msg5 = "**Please choose Audio quality** for the Video you selected"
msg6 = "**Got a 429 error (HTTP Too many reqests)** \nplease report any problems to @bryllbots_support \n I will reboot now, Please retry after 1 min"
msg7 = "**Video downloaded, Downloading Audio....**"
msg8 = "**Error code %s** Kindly report this"
msg9 = "**Joining Video with Audio you Selected....**"
msg10 = "**Huh?** you don't want video or audio,\nthen what do you want??"
msg11 = "**Please Send a Valid Youtube/YoutubeMusic Link**"
msg12 = "**Sorry, the Link you requested is age-restricted**"
msg13 = "**Sorry, this video is Private**"
msg14 = "**Sorry, this video is Region Blocked**"
msg15 = "**Sorry, this video is UnAvailable on YOUTUBE** rightnow"
msg16 = "**Regex Error, Please report this issue** along with the link"

logger1 = "**New user!!**"
logger2 = "**User Says**:\n\n"
logger3 = "**User Wants To report** \n\n"
logger4 = "you have to say something like **/report video isn't playable**\nOr reply to a message\n\n** ⚠️ REPORT any bugs at @bryllbots_support  ⚠️ **"
logger5 = "**User is Happy** says thanks "

shut_url = "https://api.heroku.com/apps/86156820-2ef7-44d6-b663-44e1727bda32/dynos/worker.1/actions/stop"
shut_headers = { 'Accept': 'application/vnd.heroku+json; version=3', 'Authorization': 'Bearer 00b0709c-e8ee-417e-b826-0d4647462534',}

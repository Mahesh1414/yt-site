from pytube.__main__ import YouTube
import pytube.exceptions as pytex
import asyncio, os, time, requests, uuid
from stuff import msg0, msg1, msg2, msg3, msg4, msg6, msg7, msg8, msg9, msg10, msg11, msg12, msg13, msg14, msg15, msg16, stk0, stk1, stk3, fthl, shut_url, shut_headers
#from saveProgress import Save
from urllib.request import urlretrieve

blackbar = "●"
whitebar = "○"

# mjson = message in json
# vopt  = video options
# aopt  = audio optiona
# tid   = task id #generated using uuid
# fin   = final info fetched

class pyt:

 def __init__(self, l):
     self.msg   = None
     self.mjson = None
     self.vopt  = None
     self.aopt  = None
     self.link  = l
     self.tid   = uuid.uuid4().hex

     self.stream = None
     self.title  = None
     self.artist = None
     self.thumb  = None
     self.length = None
     self.info   = None

 def setItagV(self, itag):
     self.itagV = itag
     return None
 def setItagA(self, itag):
     self.itagA = itag
     return None
 def getItagV(self):
     return self.itagV
 def getItagA(self):
     return self.itagA
 def getSteams(self):
     return self.stream

 # quick way to form json for error messages
 # instead of writing same code over and over
 # pass status is it error? is it info?
 # then pass the message, sticker is optional
 async def reply(self,status="info",m=None,sticker=None):
     m = {
       'id'    : self.tid,
       'status': status,
       'stkr'  : sticker,
       'msg'   : m}
     return m

 async def fetch(self):
    link = self.link
    try:
       yt = YouTube(url=link, on_progress_callback=self.pytubeProg, on_complete_callback=self.downDone)
       s = yt.streams
       v = s.filter(mime_type="video/mp4").order_by("resolution")
       a = s.filter(mime_type="audio/mp4").order_by("bitrate")

    except pytex.RegexMatchError: return (await self.reply("error",msg16,stk3), None)
    except pytex.AgeRestrictedError: return (await self.reply("error",msg12,stk3), None)
    except pytex.VideoPrivate: return (await self.reply("error",msg13,stk3), None)
    except pytex.VideoRegionBlocked: return (await self.reply("error",msg14,stk3), None)
    except pytex.VideoUnavailable: return (await self.reply("error",msg15,stk3), None)

    except Exception as e:
       if "429" in str(e):
          print(msg6, str(e))
          return (await self.reply('error',msg6,stk0), None)

       print(e)
       return (await self.reply('error',str(e),stk0), None)

    author = yt.author
    title = yt.title
    lengthInSeconds = yt.length
    uploadDate = yt.publish_date.strftime("%Y-%m-%d")
    views = yt.views
    channel = yt.channel_url
    thumbnail = yt.thumbnail_url

    mins = 0; secs = 0
    length = ""
    while 11111:
        if lengthInSeconds > 59:
            lengthInSeconds -= 60; mins += 1
        else:
            secs = lengthInSeconds; length = f"{mins}:{secs}"
            break

    msgFetch = {
             'title':   title,
             'artist':  author,
             'channel': channel,
             'length':  length,
             'hits':    views,
             'udate':   uploadDate}

    theButtonsV = []
    theButtonsA = []

    for stream in v:
        itag = str(stream.itag)
        mtype = stream.type
        res = stream.resolution
        size = self.humanbytes(stream.filesize_approx)
        is_progressive = stream.is_progressive
        if is_progressive: tex = "Video&Audio"
        else: tex = "Video Only"

        buttonText = f"{res} {tex} {size}"
        if size is None: buttonText = f"{res} {tex}"
        data = f"{itag} | {mtype} | {is_progressive}"
        theButtonsV.append({'tex': buttonText, 'callbk':data})

    for stream in a:
        itag = str(stream.itag)
        mtype = stream.type
        abr = stream.abr
        size = self.humanbytes(stream.filesize_approx)
        buttonText = f"{abr} audio {size}"
        if size is None: buttonText = f"{abr} audio"
        data = f"{itag} | {mtype} | {False}"
        theButtonsA.append({'tex': buttonText, 'callbk':data})

    m = {
       'id': self.tid,
       'status' : 'info',
       'stkr'   : None,
       'thumb'  : thumbnail,
       'msg'    : msgFetch,
       'buttonsV': theButtonsV,
       'buttonsA': theButtonsA,
       }

    self.stream = s
    self.msg = m
    self.title = title
    self.artist = author
    self.thumb = thumbnail
    self.length = yt.length
    self.info = msgFetch

    return (m,self)


 async def download(self, is_progressive):
    streams = self.getSteams()
#    global ms, typeToDownload
#    ms = m
    print(self.thumb , is_progressive)

    if not is_progressive:
        vItag = self.getItagV()
        aItag = self.getItagA()

        try:
           pathV = None
           pathA = None

           if vItag != "idwV":
              readyV = streams.get_by_itag(vItag)
              typeToDownload = f"V|{self.title}|{self.info}"
              pathVi = readyV.download(); pathVii, tt = pathVi.split(".mp4")
              pathffm = pathVii + ".mp4"
              pathV = pathVii + "V.mp4"
              os.rename(pathVi, f"{pathV}")

           if aItag != "idwA":
              readyA = streams.get_by_itag(aItag)
              typeToDownload = f"A|{self.title}|{self.info}"
              pathAu = readyA.download(); pathA, tt = pathAu.split(".mp4")
              pathffmA = pathA + ".mp3"
              pathA = pathA + "A.mp4"
              os.rename(pathAu, f"{pathA}")

           print(str(pathV), str(pathA))
           if pathA == None  and pathV == None:
              await m.message.edit_text(msg10)
              await m.message.reply_sticker(stk1)
              return  "processed"

           elif pathV == None:
              try:
                 thumb = urlretrieve(self.thumb)[0]
                 cmd = f"ffmpeg -i '{pathA}' -i '{thumb}' -map 0:0 -map 1:0  -q 0 -id3v2_version 3 -metadata title='{self.title}' -metadata artist='{self.artist}'  -metadata:s:v title='Album cover' -metadata:s:v comment='Cover (front)' '{pathffmA}'"
              except Exception as e:
                 print(str(e));
                 cmd = f"ffmpeg -i '{pathA}' -q 0 -id3v2_version 3 -metadata title='{self.title}' -metadata artist='{self.artist}'  -metadata:s:v title='Album cover' -metadata:s:v comment='Cover (front)' '{pathffmA}'"
              path = f"{pathffmA}"
           elif pathA == None:
              cmd = "echo 'videoOnly'"; path = f"{pathV}"
           elif pathA != None  and pathV != None:
              cmd = f"ffmpeg -i '{pathV}' -i '{pathA}' -map 0:0 -map 1:0 -c copy -qscale:v 0 -qscale:a 0 '{pathffm}'"
              path = f"{pathffm}"

           code = await self.runShell(cmd)
           if code != 0:
              m = await self.reply('error',msg8%code,stk0)
              return (m,"processed")

#           await m.message.edit_text(self.info + "**Uploading...**")
        except Exception as e:
           if "429" in str(e):
              m = await self.reply('error',msg6,stk0)
              print(msg6, str(e))
              return (m,"processed")

           print(e)
           m = await self.reply('error',e,stk0)
           return (m,"processed")
    else:
        print('second')
        pathA = None; pathV = "V"
        vItag = self.getItagV()
        ready = streams.get_by_itag(vItag)
        typeToDownload = f"VA|{self.title}|{self.info}"
        try: path = ready.download()
        except Exception as e:
           if "429" in str(e):
              print(msg6, str(e))
              m = await self.reply('error',msg6,stk0)
              return (m,"processed")

           print(e)
           m = await self.reply('error',e,stk0)
           return (m,"processed")

    try:
       os.system(f"mv '{path}' ./Downloads/")
       if pathV: os.remove(pathV)
       if pathA: os.remove(pathA)
    except Exception as e: print(e)
    m = {
       'id': self.tid,
       'status' : 'info',
       'stkr'   : None,
       'thumb'  : self.thumb,
       'msg'    : self.info,
       'down'   : path,
       }

    return (m,'processed')

 def downDone(self,path, uu):
#    loop = asyncio.get_event_loop()
#    asyncio.ensure_future(notifyUser(), loop=loop)
    print('placeholder')

 def pytubeProg(self,s, c, b):
#    loop = asyncio.get_event_loop()
#    asyncio.ensure_future(tHePrOgReSsHoOk(s, c, b), loop=loop)
    print('placeholder')

 async def tHePrOgReSsHoOk(stream, chunk, bytes_remaining):
    filesize = stream.filesize
    Mediasize = humanbytes(stream.filesize)
    downloadprogress = len(chunk) / stream.filesize * 100
        # chunk is bytes downloaded you divide chunk with
        # file size to get a percent %

    if downloadprogress <= 1: # 1
       blackbars = 0; whitebars = 20
    elif downloadprogress <= 5: # 2 3 4 5
       blackbars = 1; whitebars = 19
    elif downloadprogress <= 10: # 6 7 8 9 10
       blackbars = 2; whitebars = 18
    elif downloadprogress <= 15: # 11 12 13 14 15
       blackbars = 3; whitebars = 17
    elif downloadprogress <= 20: # 16 17 18 19 20
       blackbars = 4; whitebars = 16
    elif downloadprogress <= 25: blackbars = 5; whitebars = 15;
    elif downloadprogress <= 30: blackbars = 6; whitebars = 14;
    elif downloadprogress <= 35: blackbars = 7; whitebars = 13;
    elif downloadprogress <= 40: blackbars = 8; whitebars = 12;
    elif downloadprogress <= 45: blackbars = 9; whitebars = 11;
    elif downloadprogress <= 50: blackbars = 10; whitebars = 10;
    elif downloadprogress <= 55: blackbars = 11; whitebars = 9;
    elif downloadprogress <= 60: blackbars = 12; whitebars = 8;
    elif downloadprogress <= 65: blackbars = 13; whitebars = 7;
    elif downloadprogress <= 70: blackbars = 14; whitebars = 6;
    elif downloadprogress <= 75: blackbars = 15; whitebars = 5;
    elif downloadprogress <= 80: blackbars = 16; whitebars = 4;
    elif downloadprogress <= 85: blackbars = 17; whitebars = 3;
    elif downloadprogress <= 90: blackbars = 18; whitebars = 2;
    elif downloadprogress <= 95: blackbars = 19; whitebars = 1;
    elif downloadprogress <= 100: blackbars = 20; whitebars = 0;
    messa = blackbar*blackbars + whitebar*whitebars
    print(messa)

    global ms, typeToDownload
    letter, fileName, info = typeToDownload.split("|")
    type = "Video"
    if letter == "A": type = "Audio"
    tex = f"""
╭───[**Dᴏᴡɴʟᴏᴀᴅɪɴɢ Yᴏᴜʀ Fɪʟᴇ**]───⍟
│
├<b>📁 Fɪʟᴇ Nᴀᴍᴇ : {fileName}</b>
│
├<b>🗂 Fɪʟᴇ Sɪᴢᴇ : {Mediasize}</b>
│
├<b>✅ Dᴏɴᴇ : {downloadprogress}%</b>
│
├<b>📥 : [{messa}]</b>
╰─────────────────⍟"""

    await ms.message.edit_text(info + "\n\n" + tex)


 async def notifyUser(self):
    global ms, typeToDownload
    letter, fileName, info = typeToDownload.split("|")
    if letter == "VA":
       await ms.message.edit_text(info + "\n\n" + msg3)
    elif letter == "V":
       await ms.message.edit_text(info + "\n\n" + msg7)
    elif letter == "A":
       try: await ms.message.edit_text(info + "\n\n" + msg9)
       except Exception as e: print(str(e))

 async def runShell(self,cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'[cmd exited with {proc.returncode}]')
    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr and proc.returncode != 0:
        print(f'[stderr]\n{stderr.decode()}')
    return proc.returncode


 def humanbytes(self,size):
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'

def restartDyno():
    requests.post(shut_url, headers=shut_headers)

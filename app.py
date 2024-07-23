class c:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

import os
from telnetlib import theNULL
from tokenize import String
os.system("color")

print(f"{c.CYAN}#====================#{c.ENDC}")
print(f"Importing requisits... \n")

import json
import io
import re
import math
import requests
import webbrowser
from bs4 import BeautifulSoup
import FreeSimpleGUI as sg
from FreeSimpleGUI import Window, Text, Button, Push, Titlebar, theme_list, theme, LOOK_AND_FEEL_TABLE, TIMEOUT_KEY
import pyperclip as pc
from PIL import Image
import cloudscraper
import os.path

#def p(string:str, col:str, indent:int) -> str:

#                           ==================================== Does Game List Exist? ====================================
unsanit = False
print(f"Checking games list...")

check_file = os.path.isfile('./GameOutput.json')
if check_file == False:
    #Do game list download thing
    print(f"{c.RED}-->    Games list not found! Making one now... {c.ENDC}")
    URL = "https://dlpsgame.com/list-all-game-ps4/"
    print(f"-->    Requesting Content")
    page = requests.get(URL)
    print(page)

    print(f"-->    Scraping Page")
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("ol", class_="display-posts-listing")

    posts = results.find_all("li", class_="listing-item")
                
    print(f"-->    Got "+str(len(posts))+" posts! - Dumping to file now.")

    data = {}
    maindata = {}
    numero = 1

    for post_element in posts:
                    #notif("dumping game "+str(numero)+" of "+str(len(posts)))
        link_url = post_element.find_all("a")[0]["href"]
        gameName = post_element.text

        data[gameName.encode('utf-8')] = {
            "link" : link_url.encode('utf-8'),
            "CUSA" : "NONE",
            "gamedl" : "NONE",
            "updl" : "NONE",
            "dlcdl" : "NONE",
            "release" : "NONE",
            "genre" : "NONE",
            "lang" : "NONE",
            "GameSize" : "NONE",
            "ImageLink" : "NONE",
        }
        maindata.update(data)

        numero = numero + 1
    with open("GameOutput.json", "w") as write_file:
        json.dump(str(maindata), write_file)
    print(f"{c.GREEN}Successfully dumped games. Proceeding... {c.ENDC}")
#========================================================================================#
print(f"\nChecking for api key file...")
check_file = os.path.isfile('./apikey.txt')
if check_file == False:
    print(f"{c.RED}-->   API Key file not found! Making one now... {c.ENDC}")
    with open("apikey.txt", "w") as write_file:
        write_file.write("")
#                           ==================================== Sanitising Game List ====================================

print(f"\nReading games list... \n")

def loadList():
    unsanit = False

    with open('GameOutput.json', 'rb+') as filehandle: #Cleaning up import impurities
        st = str(filehandle.read())
        filehandle.seek(-1, 2)
        if filehandle.read() == b'"':
            unsanit = True

    if unsanit == True: #Cleaning up import impurities
        with open('GameOutput.json', 'r') as data: #Cleaning up import impurities
            loaded = data.read()
            s = loaded.strip('\"')

        with open('GameOutput.json', 'w') as data: #Cleaning up import impurities
            data.write(s)

    with open('GameOutput.json', 'r') as data: #Cleaning up import impurities
        loaded = data.read()
        p = re.compile('(?<!\\\\)\'')
        s = p.sub('\"', loaded)

    with open('GameOutput.json', 'w') as data: #Cleaning up import impurities
        data.write(s)

    with open("GameOutput.json", "r", encoding='utf-8-sig') as f: # Counting game amount
        string = f.read()
        listOfGames = eval(string)
        txt = "Got "+str(len(listOfGames))+" Games"

    return listOfGames, txt

#                           ==================================== Populating Game List ====================================
print(f"Parsing Games List...")
class Item(): # Defining item for metatable
    def __init__(self, gameName, link, gameCUSA, gamedl, updl, dlcdl, release, genre, lang, gameSize, ImageData):
        self.gameName = gameName
        self.link = link
        self.gameCUSA = gameCUSA
        self.gamedl = gamedl
        self.updl = updl
        self.dlcdl = dlcdl
        self.release = release
        self.genre = genre
        self.lang = lang
        self.gameSize = gameSize
        self.ImageData = ImageData

    def __str__(self):
        return self.gameName
    
my_item_list = []

gamesListRaw, gameAmount = loadList()

for game in gamesListRaw: # Adding to item list
    #print(game, a[game])
    gameInfo = gamesListRaw[game]
    gameName = game.decode()
    #print(gameInfo['link'])
    obj = Item(gameName, gameInfo['link'], gameInfo['CUSA'], gameInfo['gamedl'], gameInfo['updl'], gameInfo['dlcdl'], gameInfo['release'], gameInfo['genre'], gameInfo['lang'], gameInfo['GameSize'], gameInfo['ImageLink'])

    my_item_list.append(obj)


def checkCache(c):
    cached = False
    for a in c:
        if a != 'link' and c[a] != 'NONE':
            cached = True
    print('iscached? '+cached)


#                           ==================================== Functions ====================================

def setclipboard(text):
    pc.copy(text)

def gb2mb(size):
    return(size * 1000)

def mb2gb(size):
    return(size / 1000)

def strip(string:str): # Needs to strip the letter 'p'
    string = str(string)
    return re.sub('[^A-Za-z0-9 ]+', '', string)

def download(lnk:str):
    with open("apikey.txt", "r", encoding='utf-8-sig') as f: # grab text
        key = f.read()

    URL = 'http://api.alldebrid.com/v4/user?agent=myAppName&apikey='+key
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(URL, headers=headers).text
    soup = BeautifulSoup(page, features='html.parser')

    jsonResponse = json.loads(page)
    print("API Authorisation "+jsonResponse['status'], flush=True)

    if jsonResponse['status'] == 'success':
        URL = 'https://api.alldebrid.com/v4/link/unlock?agent=myAppName&apikey='+key+'&link='+lnk
        headers = {'User-Agent': 'Mozilla/5.0', 'link': ''}
        page = requests.get(URL, headers=headers).text
        soup = BeautifulSoup(page, features='html.parser')
        jsonResponse = json.loads(page)
        if jsonResponse['status'] == 'success':
            webbrowser.open(jsonResponse['data']['link'])
        else:
            if jsonResponse['status'] == 'error':
                notif(jsonResponse['error']['code'] + ' | ' +jsonResponse['error']['message'], True)

    else:
        notif("Invalid API Key!!", True)

def getImageData(url:str):
    jpg_data = (
        cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "mobile": False})
        .get(url)
        .content
    )
    pil_image = Image.open(io.BytesIO(jpg_data))
    png_bio = io.BytesIO()
    pil_image.save(png_bio, format="PNG")
    png_data = png_bio.getvalue()
    return png_data

def GetSize(a):
    return "10GB"

def getDLfromArchive(link, sector):
    page = requests.get(str(link))


    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("main", id="content")
    if results == "None": #results will return 'None' if nothing found
        print(f"{c.RED}[ERROR] --> Archive Content search returned NONE (Cloudflare Flagged?)")

    divs = results.find_all("div")
    for div in divs:
        posts = div.find_all("p")
        if posts:
            for post in posts:
                if str(post).find("Game") != -1 or str(post).find("Update") != -1 or str(post).find("DLC") != -1:
                    links = post.find_all('a')
                    for alink in links:
                        if alink['href'].find("1fichier") != -1 or alink['href'].find("mega") != -1 or alink['href'].find("mediafire") != -1 or alink['href'].find("filecrypt") != -1:
                            #print("Haha gotcha 1fichier, from"+sector+" :"+str(alink['href']))
                            return str(alink['href'])
    
    return "N/A"

def GetContent(url:str, name:str):
    GameCUSA, genre, lang, release = ["ERR"]*4 # Seriously python?
    GameDL, UpdateDL, DLCDL = ["None Available"]*3
    GameSize, UpdateSize, DLCSize = ["0mb"]*3

    TotalGB, TotalMB = ["?? GB"]*2
    imageLink = ""
    url = url.decode('ASCII')
    print(f"\n---------------")
    print(f"\nGetting Content...")

    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(str(url), headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    #===================================================================#
    #                          Getting Game Icon

    results = soup.find("div", class_="post-body entry-content")
    if results == "None": #results will return 'None' if nothing found
        print(f"{c.RED}[ERROR] --> Content search returned NONE (Cloudflare Flagged?)")
    
    posts = results.find_all("img", width=True, height=True)

    for link in posts:
        if link['src'].find("2.bp.blogspot") and link['width'] =="165":
            imageLink = link['src']
            pass
        if link['src'].find("1.bp.blogspot") and link['width'] =="175":
            imageLink = link['src']
            pass
    #===================================================================#
    #                          Getting Game Info

    alltables = soup.findAll( "table", {"border":"7"} )

    gameAttributes = []
    for t in alltables:
        if t.find('span'):
            allspan = t.find_all('span')
            for span in allspan:
                gameAttributes.append(span.text)

    spanIndex = 0
    lastText = ""
    for spanText in gameAttributes:
        spanIndex + 1
        if lastText == "GENRE":
            genre = spanText
        if lastText == "LANGUAGES" or lastText == "LANGUAGE":
            lang = spanText
        if lastText == "RELEASE":
            release = spanText
        lastText = spanText
    #===================================================================#
    #                        Getting Game Downloads

    gamedl1f, gamedlmega, gamedlmed, gamedlarch, gamedlcrypt = ["None"]*5
    updl1f, updlmega, updlmed, updlarch, updlcrypt = ["None"]*5
    dlc1f, dlcmega, dlcmed, dlcarch, dlccrypt = ["None"]*5

    results = soup.find("div", class_="su-spoiler-content su-u-clearfix su-u-trim")
    if results == "None": #results will return 'None' if nothing found
        print(f"{c.RED}[ERROR] --> Content search returned NONE (Cloudflare Flagged?)")

    posts = results.find_all("p")
    
    for post in posts:
        if str(post).find("CUSA") != -1 or str(post).find("SLES") != -1 or str(post).find("SLUS") != -1:
            if str(post).find('https') == -1:
                GameCUSA = strip(post)
        #==================================#
        if str(post).find("Game") != -1 or str(post).find("Link Download:") != -1:
            links = post.find_all('a')
            for alink in links:
                if alink['href'].find("1fichier") != -1:
                    gamedl1f = str(alink['href'])
                if alink['href'].find("downloadgameps3") != -1:
                    glink = getDLfromArchive(str(alink['href']), "GAME")
                    gamedlarch = str(glink)
                if alink['href'].find("filecrypt") != -1:
                    gamedlcrypt = str(alink['href'])
                if alink['href'].find("mediafire") != -1:
                    gamedlmed = str(alink['href'])
                if alink['href'].find("mega") != -1:
                    gamedlmega = str(alink['href']) 
        #==================================#
        #==================================#
        if str(post).find("Update") != -1 or str(post).find("Link Download:") != -1:
            links = post.find_all('a')
            for alink in links:
                if alink['href'].find("1fichier") != -1:
                    updl1f = str(alink['href'])
                if alink['href'].find("downloadgameps3") != -1:
                    glink = getDLfromArchive(str(alink['href']), "GAME")
                    updlarch = str(glink)
                if alink['href'].find("filecrypt") != -1:
                    updlcrypt = str(alink['href'])
                if alink['href'].find("mediafire") != -1:
                    updlmed = str(alink['href'])
                if alink['href'].find("mega") != -1:
                    updlmega = str(alink['href']) 
        #==================================#
        #==================================#            
        if str(post).find("All DLC") != -1 or str(post).find("DLC:") != -1 or str(post).find("DLC : ") != -1:
            links = post.find_all('a')
            for alink in links:
                if alink['href'].find("1fichier") != -1:
                    glink = str(alink['href'])
                    dlc1f = str(glink)
                    dlcSize = GetSize(glink)
                if alink['href'].find("downloadgameps3") != -1:
                    glink = getDLfromArchive(str(alink['href']), "DLC")
                    dlcarch = str(glink)
                    dlcSize = GetSize(glink)
                if alink['href'].find("filecrypt") != -1:
                    dlccrypt = str(alink['href'])
                if alink['href'].find("mediafire") != -1:
                    dlcmed = str(alink['href'])
                if alink['href'].find("mega") != -1:
                    dlcmega = str(alink['href']) 
        #==================================#

    GotGame = False
    for a in [gamedl1f, gamedlarch, gamedlcrypt, gamedlmed, gamedlmega]:
        if a!="None":
            GotGame = True

    if GotGame == False:
        print(f"Couldn't Find Game Link, Re-Scraping Content...")
        for raw in results:
            if str(raw).find("CUSA") != -1 or str(raw).find("SLES") != -1 or str(raw).find("SLUS") != -1:
                if str(raw).find('https') == -1:
                    GameCUSA = strip(raw)

        posts = results.find_all("a")
        for post in posts:
            #==================================#
            if post['href'].find("1fichier") != -1:
                        glink = str(post['href'])
                        gamedl1f = str(glink)
                        gameSize = GetSize(glink)
            if post['href'].find("downloadgameps3") != -1:
                        glink = getDLfromArchive(str(post['href']), "GAME")
                        gamedlarch = str(glink)
                        gameSize = GetSize(glink)
            if post['href'].find("filecrypt") != -1:
                        gamedlcrypt = str(post['href'])
            if post['href'].find("mediafire") != -1:
                        gamedlmed = str(post['href'])
            if post['href'].find("mega") != -1:
                        gamedlmega = str(post['href']) 
            #==================================#

    layout = [
        [sg.Titlebar("PS4 Games")],
        [
            sg.Frame("Game Icon", [[sg.Image(data=getImageData(imageLink), key="-ff-")]]),
            sg.Frame("GAME",[
                            [sg.Text('Game: '+GameCUSA)],
                            [sg.Text('Release: '+release)],
                            [sg.Text('Genre: '+genre)],
                            [sg.Text('Language: '+lang)],
                            [sg.Text('Size: ')],
                           ], pad=(0, 5))
        ],
    ]
    layout.append(
        [sg.Column([
            [sg.Frame('Downloads:',[
                [sg.Frame('1File', [
                    [sg.Column([
                        [sg.Button('Copy Game Link', k='CGL1F'),
                        sg.Button('Copy Update Link', k='CUL1F'),
                        sg.Button('Copy DLC Link', k='CDLC1F'),
                        sg.Button("Download Game", k='DG1F'),
                        sg.Button("Download Update", k='DU1F'),
                        sg.Button("Download DLC", k='DDLC1F')
                        ]
                    ],pad=(0,0))]
                ], k='1FF')],
                [sg.Frame('dlpsarchive', [
                    [sg.Column([
                        [sg.Button('Copy Game Link', k='CGLARCH'),
                        sg.Button('Copy Update Link', k='CULARCH'),
                        sg.Button('Copy DLC Link', k='CDLCARCH'),
                        sg.Button("Download Game", k='DGARCH'),
                        sg.Button("Download Update", k='DUARCH'),
                        sg.Button("Download DLC", k='DDLCARCH')
                        ]
                    ],pad=(0,0))]
                ], k='DLPSF')],
                [sg.Frame('Filecrypt', [
                    [sg.Column([
                        [sg.Button('Copy Game Link', k='CGLFC'),
                        sg.Button('Copy Update Link', k='CULFC'),
                        sg.Button('Copy DLC Link', k='CDLCFC'),
                        sg.Button("Download Game", k='DGFC'),
                        sg.Button("Download Update", k='DUFC'),
                        sg.Button("Download DLC", k='DDLCFC')
                        ]
                    ],pad=(0,0))]
                ], k='FCF')],
                [sg.Frame('Mediafire', [
                    [sg.Column([
                        [sg.Button('Copy Game Link', k='CGLMED'),
                        sg.Button('Copy Update Link', k='CULMED'),
                        sg.Button('Copy DLC Link', k='CDLCMED'),
                        sg.Button("Download Game", k='DGMED'),
                        sg.Button("Download Update", k='DUMED'),
                        sg.Button("Download DLC", k='DDLCMED')
                        ]
                    ],pad=(0,0))]
                ], k='MEDF')],
                [sg.Frame('MEGA', [
                    [sg.Column([
                        [sg.Button('Copy Game Link', k='CGLMEGA'),
                        sg.Button('Copy Update Link', k='CULMEGA'),
                        sg.Button('Copy DLC Link', k='CDLCMEGA'),
                        sg.Button("Download Game", k='DGMEGA'),
                        sg.Button("Download Update", k='DUMEGA'),
                        sg.Button("Download DLC", k='DDLCMEGA')
                        ]
                    ],pad=(0,0))]
                ], k='MEGAF')],
            ])]
        ], pad=(0,0))]
    )



    window2 = sg.Window('PS4 Games List by zbombr115', layout, keep_on_top=True, finalize=True)

    pos=0
    for a in [gamedl1f, gamedlarch, gamedlcrypt, gamedlmed, gamedlmega]:
            pos=pos+1
            if a=="None":
                if pos == 1: window2['CGL1F'].update(visible=False); window2['DG1F'].update(visible=False)
                if pos == 2: window2['CGLARCH'].update(visible=False); window2['DGARCH'].update(visible=False)
                if pos == 3: window2['CGLFC'].update(visible=False); window2['DGFC'].update(visible=False)
                if pos == 4: window2['CGLMED'].update(visible=False); window2['DGMED'].update(visible=False)
                if pos == 5: window2['CGLMEGA'].update(visible=False); window2['DGMEGA'].update(visible=False)
    pos=0
    for a in [updl1f, updlarch, updlcrypt, updlmed, updlmega]:
            pos=pos+1
            if a=="None":
                if pos == 1: window2['CUL1F'].update(visible=False); window2['DU1F'].update(visible=False)
                if pos == 2: window2['CULARCH'].update(visible=False); window2['DUARCH'].update(visible=False)
                if pos == 3: window2['CULFC'].update(visible=False); window2['DUFC'].update(visible=False)
                if pos == 4: window2['CULMED'].update(visible=False); window2['DUMED'].update(visible=False)
                if pos == 5: window2['CULMEGA'].update(visible=False); window2['DUMEGA'].update(visible=False)
    pos=0
    for a in [dlc1f, dlcarch, dlccrypt, dlcmed, dlcmega]:
            pos=pos+1
            if a=="None":
                if pos == 1: window2['CDLC1F'].update(visible=False); window2['DDLC1F'].update(visible=False)
                if pos == 2: window2['CDLCARCH'].update(visible=False); window2['DDLCARCH'].update(visible=False)
                if pos == 3: window2['CDLCFC'].update(visible=False); window2['DDLCFC'].update(visible=False)
                if pos == 4: window2['CDLCMED'].update(visible=False); window2['DDLCMED'].update(visible=False)
                if pos == 5: window2['CDLCMEGA'].update(visible=False); window2['DDLCMEGA'].update(visible=False)
    #===================#
    am=0
    for a in [gamedl1f, updl1f, dlc1f]:
        if a == "None": am = am + 1
    if am==3: window2['1FF'].hide_row()
    #===================#
    am=0
    for a in [gamedlarch, updlarch, dlcarch]:
        if a == "None": am = am + 1
    if am==3: window2['DLPSF'].hide_row()
    #===================#
    am=0
    for a in [gamedlcrypt, updlcrypt, dlccrypt]:
         if a == "None": am = am + 1
    if am==3: window2['FCF'].hide_row()
    #===================#
    am=0
    for a in [gamedlmed, updlmed, dlcmed]:
        if a == "None": am = am + 1
    if am==3: window2['MEDF'].hide_row()
    #===================#
    am=0
    for a in [gamedlmega, updlmega, dlcmega]:
        if a == "None": am = am + 1
    if am==3: window2['MEGAF'].hide_row()
    #================================================================#
    window2.metadata = []
    window2.metadata.append(gamedl1f) #index pos is 0 lol wtf
    window2.metadata.append(gamedlarch)
    window2.metadata.append(gamedlcrypt)
    window2.metadata.append(gamedlmed)
    window2.metadata.append(gamedlmega)
    window2.metadata.append(updl1f)
    window2.metadata.append(updlarch)
    window2.metadata.append(updlcrypt)
    window2.metadata.append(updlmed)
    window2.metadata.append(updlmega)
    window2.metadata.append(dlc1f)
    window2.metadata.append(dlcarch)
    window2.metadata.append(dlccrypt)
    window2.metadata.append(dlcmed)
    window2.metadata.append(dlcmega)
    print("Got Content!", flush=True)

#                           ==================================== Main Window Layout ====================================

sg.theme('dark gray 13')
layout = [  
    [sg.Titlebar("PS4 PKG List")],

    [sg.MenubarCustom([['&Options', ['Update Games', 'View New Games', 'Backup Games List','File Download API']]], key = 'menu', bar_text_color = 'White', background_color = 'White')],
    [sg.Text(gameAmount, justification='center' )],
    [sg.Input(size=(40, 1), enable_events=True, default_text="Input Search...", key='-INPUT-'), sg.Button('Clear Search')],
    [sg.Listbox(my_item_list, key='-LB-', s=(51,10), select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED)],
    [sg.Column([[sg.Frame('Actions:',[[sg.Column([[sg.Button('Get Page Link'), sg.Button('Get Game Content'), sg.Button('Exit')]],size=(375,45), pad=(0,0))]])]], pad=(0,0))],
    [sg.StatusBar('Coded by zbombr115', key='-STAT-')],
]

window1 = sg.Window('PS4 Games List by zbombr115', layout, keep_on_top=True, finalize=True)

def notif(str, flush):
    sg.popup_quick_message(str, keep_on_top=True)
    if flush:
        print(str, flush=True)

#                           ==================================== Event (Button) Handling ====================================
foundDifferences = []
foundDifferences.append(Item("No new games have been dumped here yet!", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
foundDifferences.append(Item("Try Updating the games list!", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))

while True:

    window, event, values = sg.read_all_windows()
    if event == sg.WIN_CLOSED or event == 'Exit' and window != "None":
        window.close()
    if event == 'Update Games':
        URL = "https://dlpsgame.com/list-all-game-ps4/"
        print(f"-->    Requesting Content")
        page = requests.get(URL)

        print(f"-->    Scraping Page")
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find("ol", class_="display-posts-listing")
        if results == "None": #results will return 'None' if nothing found
            print(f"{c.RED}[ERROR] --> Listing search returned NONE (Cloudflare Flagged?)")

        posts = results.find_all("li", class_="listing-item")
                
        print(f"-->    Got "+str(len(posts))+" posts! - Dumping to file now.")

        data = {}
        maindata = {}
        numero = 1

        for post_element in posts:
        #notif("dumping game "+str(numero)+" of "+str(len(posts)))
            link_url = post_element.find_all("a")[0]["href"]
            gameName = post_element.text

            data[gameName.encode('utf-8')] = {
                        "link" : link_url.encode('utf-8'),
                        "CUSA" : "NONE",
                        "gamedl" : "NONE",
                        "updl" : "NONE",
                        "dlcdl" : "NONE",
                        "release" : "NONE",
                        "genre" : "NONE",
                        "lang" : "NONE",
                        "GameSize" : "NONE",
                        "ImageLink" : "NONE",
            }
            maindata.update(data)
            numero = numero + 1
        with open("GameOutput.json", "w") as write_file:
            json.dump(str(maindata), write_file)
        print(f"{c.GREEN}Successfully dumped games. Checking for new releases... {c.ENDC}")

        gamesListRaw, gameAmount = loadList()
        new_item_list = []
        foundDifferences = []

        for game in gamesListRaw: # Adding to item list
            gameInfo = gamesListRaw[game]
            gameName = game.decode()
            #print(gameInfo['link'])
            obj = Item(gameName, gameInfo['link'], gameInfo['CUSA'], gameInfo['gamedl'], gameInfo['updl'], gameInfo['dlcdl'], gameInfo['release'], gameInfo['genre'], gameInfo['lang'], gameInfo['GameSize'], gameInfo['ImageLink'])


            new_item_list.append(obj)

        s = set(my_item_list)

        foundDifferences.append(Item("New Games:", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))


        for newgame in new_item_list:
                    found = False
                    for gname in my_item_list:
                        if newgame.gameName in gname.gameName:
                            found = True
                    
                    if not found:
                        foundDifferences.append(Item(newgame.gameName, newgame.link, "NONE", "NONE", "NONE", "NONE", "NONE", "NONE", "NONE", "NONE", "NONE")) # Adding new games into list

        my_item_list = []
        gamesListRaw, gameAmount = loadList()

        for game in gamesListRaw: # Adding to item list
                gameInfo = gamesListRaw[game]
                gameName = game.decode()

                obj = Item(gameName, gameInfo['link'], gameInfo['CUSA'], gameInfo['gamedl'], gameInfo['updl'], gameInfo['dlcdl'], gameInfo['release'], gameInfo['genre'], gameInfo['lang'], gameInfo['GameSize'], gameInfo['ImageLink'])


                my_item_list.append(obj)
                pass
            
        window['-LB-'].update(my_item_list)
        my_item_list = new_item_list
        print(f"{c.GREEN}Checked for new releases... See them in 'View New Games' {c.ENDC}")

    if event == 'View New Games':
        col3 = sg.Column([[sg.Frame('Options:', [[sg.Button('Exit')]])]]),

        layout3 = [
                [sg.Titlebar("New Games")],
                [sg.Listbox(foundDifferences, key='-ListBox-', s=(40,10), select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED)],
                [col3]
        ]

        window3 = sg.Window('Gamelist', layout3, keep_on_top=True, finalize=True)

    if event == 'File Download API':
        inp = ""
        with open("apikey.txt", "r", encoding='utf-8-sig') as f: # grab text
            inp = f.read()
        layout3 = [
                [sg.Titlebar("API Key Input (alldebrid.com)")],
                [sg.Column([[sg.Frame('API Key:',[[sg.Column([[sg.Input(inp, key='-API-')]],pad=(0,0))]])]], pad=(0,0))],
        ]

        window4 = sg.Window('API', layout3, keep_on_top=True, finalize=True)
    if event == 'Backup Games List':
        with open("GameOutput.json") as list:
            with open("GameOutputBackup.json", "w") as write_file:
                write_file.write(list.read())
                print(f"{c.GREEN}Successfully Backed up games list. {c.ENDC}")

    #print(event, flush=True)

    if window != 'None':
        if window == window1:
            if event == sg.WIN_CLOSED or event == 'Exit':
                window.close()
            #==================================# 
            if event == 'Clear Search':
                window['-INPUT-'].Update("")
                values['-INPUT-']=''
                notif("Cleared Search!", False)
            if values['-INPUT-'] != '' and values['-INPUT-'] != 'Input Search...':
                searchElements = []
                search = values['-INPUT-']
                for a in my_item_list:
                    if a.gameName.lower().find(search.lower()) != -1:
                        searchElements.append(a)

                window['-LB-'].update(searchElements)
            elif values['-INPUT-'] == '':
                print()
                #window['-LB-'].update(my_item_list) #FIGURE OUT A ETTER WAY FOR THIS OTHERWISE EVERY BUTTON CLICK IT RESETS TO TOP OF LISTBOX
            #==================================#
            if event == 'Get Page Link':
                for item in values['-LB-']:
                    setclipboard(item.link.decode("ASCII"))
                    notif("Set Link To Clipboard!", False)
            elif event == 'Get Game Content':
                for item in values['-LB-']:
                    #print(gamesListRaw[item.shown.encode('ASCII')], flush=True)
                    GetContent(item.link, item.gameName)
                    notif("Got Content for "+str(item.gameName)+"!", False)
        else:
            #==================================# 
            if event == "CGL1F":
                lnk = str(window.metadata[0])#.replace("Download: ", "")
                setclipboard(lnk)
                notif("Set Link To Clipboard!", False)
            #==================================# 
            if event == "CGLARCH":
                lnk = str(window.metadata[1])
                setclipboard(lnk)
                notif("Set Link To Clipboard!", False)
            #==================================# 
            if event == "CGLFC":
                lnk = str(window.metadata[2])
                setclipboard(lnk)
                notif("Set Link To Clipboard!", False)
            #==================================# 
            if event == "CGLMED":
                lnk = str(window.metadata[3])
                setclipboard(lnk)
                notif("Set Link To Clipboard!", False)
            #==================================# 
            if event == "CGLMEGA":
                lnk = str(window.metadata[4])
                setclipboard(lnk)
                notif("Set Link To Clipboard!", False)
            #==================================# 
            if event == "CUL1F":
                lnk = str(window.metadata[5])
                setclipboard(lnk)
                notif("Set Link To Clipboard!", False)
            #==================================# 
            if event == "CULARCH":
                lnk = str(window.metadata[6])
                setclipboard(lnk)
                notif("Set Link To Clipboard!", False)
            #==================================# 
            if event == "CULFC":
                lnk = str(window.metadata[7])
                setclipboard(lnk)
                notif("Set Link To Clipboard!", False)
            #==================================# 
            if event == "CULMED":
                lnk = str(window.metadata[8])
                setclipboard(lnk)
                notif("Set Link To Clipboard!", False)
            #==================================# 
            if event == "CULMEGA":
                lnk = str(window.metadata[9])
                setclipboard(lnk)
                notif("Set Link To Clipboard!", False)
            #==================================# 
            if event == "CDLC1F":
                lnk = str(window.metadata[10])
                setclipboard(lnk)
                notif("Set Link To Clipboard!", False)
            #==================================# 
            if event == "CDLCARCH":
                lnk = str(window.metadata[11])
                setclipboard(lnk)
                notif("Set Link To Clipboard!", False)
            #==================================# 
            if event == "CDLCFC":
                lnk = str(window.metadata[12])
                setclipboard(lnk)
                notif("Set Link To Clipboard!", False)
            #==================================# 
            if event == "CDLCMED":
                lnk = str(window.metadata[13])
                setclipboard(lnk)
                notif("Set Link To Clipboard!", False)
            #==================================# 
            if event == "CDLCMEGA":
                lnk = str(window.metadata[14])
                setclipboard(lnk)
                notif("Set Link To Clipboard!", False)
            #==================================# 
            if event == "DG1F":
                download(window.metadata[0])
            #==================================# 
            if event == "DGARCH":
                download(window.metadata[1])
            #==================================# 
            if event == "DGFC":
                download(window.metadata[2])
            #==================================# 
            if event == "DGMED":
                download(window.metadata[3])
            #==================================# 
            if event == "DGMEGA":
                download(window.metadata[4])
            #==================================# 
            if event == "DU1F":
                download(window.metadata[5])
            #==================================# 
            if event == "DUARCH":
                download(window.metadata[6])
            #==================================# 
            if event == "DUFC":
                download(window.metadata[7])
            #==================================# 
            if event == "DUMED":
                download(window.metadata[8])
            #==================================# 
            if event == "DUMEGA":
                download(window.metadata[9])
            #==================================# 
            if event == "DDLC1F":
                download(window.metadata[10])
            #==================================# 
            if event == "DDLCARCH":
                download(window.metadata[11])
            #==================================# 
            if event == "DDLCFC":
                download(window.metadata[12])
            #==================================# 
            if event == "DDLCMED":
                download(window.metadata[13])
            #==================================# 
            if event == "DDLCMEGA":
                download(window.metadata[14])
            #==================================#

        if 'window4' in globals() and window == window4:
            if '-API-' in values and values['-API-'] != "":
                with open("apikey.txt", "w") as write_file:
                    write_file.write(values['-API-'])
    else:
        break

window1.close()

#req:
#python -m pip install --upgrade pip
#python -m pip install --upgrade pyperclip
#python -m pip install --upgrade bs4
#python -m pip install --upgrade PySimpleGUI
#python -m pip install --upgrade Pillow
#python -m pip install --upgrade PSG-Reskinner
#python -m pip install --upgrade cloudscraper



import json
import io
import re
import math
import os
import requests
from bs4 import BeautifulSoup
import PySimpleGUI as sg
from PySimpleGUI import Window, Text, Button, Push, Titlebar, theme_list, theme, LOOK_AND_FEEL_TABLE, TIMEOUT_KEY
import pyperclip as pc
from PIL import Image

import cloudscraper

unsanit = False
#                           ==================================== Does Game List Exist? ====================================

import os.path
check_file = os.path.isfile('./GameOutput.json')
if check_file == False:
    #Do game list download thing
                print("Games list not found! Making one now...", flush=True)
                URL = "https://dlpsgame.com/list-all-game-ps4/"
                print("Requesting Content", flush=True)
                page = requests.get(URL)


                print("Scraping Page", flush=True)
                soup = BeautifulSoup(page.content, "html.parser")
                results = soup.find("ol", class_="display-posts-listing")

                posts = results.find_all("li", class_="listing-item")
                
                print("Got "+str(len(posts))+" posts! - Dumping to file now.", flush=True)

                data = {}
                numero = 1

                for post_element in posts:
                    #notif("dumping game "+str(numero)+" of "+str(len(posts)))
                    link_url = post_element.find_all("a")[0]["href"]
                    gameName = post_element.text
                    data[gameName.encode('utf-8')] = link_url.encode('utf-8')

                    with open("GameOutput.json", "w") as write_file:
                        json.dump(str(data), write_file)

                    numero = numero + 1

                print("Successfully dumped games. Starting GUI now.", flush=True)

#                           ==================================== Sanitising Game List ====================================

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

class Item(): # Defining item for metatable
    def __init__(self, internal, shown):
        self.internal = internal
        self.shown = shown

    def __str__(self):
        return self.shown
    
my_item_list = []

gamesListRaw, gameAmount = loadList()

for game in gamesListRaw: # Adding to item list
    #print(game, a[game])
    gameLink = gamesListRaw[game].decode()
    gameName = game.decode()
    ob = Item(gameLink, gameName)

    my_item_list.append(ob)
    pass

#                           ==================================== Functions ====================================

def setclipboard(text):
    pc.copy(text)

def gb2mb(size):
    return(size * 1000)

def mb2gb(size):
    return(size / 1000)

def addFileSizes(fSize1, fSize2):
    if fSize1 != "?? GB" and fSize2 != "?? GB" and fSize1 != "0mb" and fSize2 != "0mb" and fSize1 != "?? MB" and fSize2 != "?? MB":
        sizeType1 = ""
        sizeType2 = ""

        finalMB = 0
        finalGB = 0

        for char in fSize1:
            if char.isalpha():
                sizeType1 += char
        for char in fSize2:
            if char.isalpha():
                sizeType2 += char
        


        if fSize1.count('.') >= 1:
            fSize1 = float(re.findall("\d+\.\d+", fSize1)[0])
            if fSize2.count('.') >= 1:
                fSize2 = float(re.findall("\d+\.\d+", fSize2)[0])
            else:
                fSize2 = int(re.findall("\d+", fSize2)[0])
        else:
            fSize1 = int(re.findall("\d+", fSize1)[0])
            if fSize2.count('.') >= 1:
                fSize2 = float(re.findall("\d+\.\d+", fSize2)[0])
            else:
                fSize2 = int(re.findall("\d+", fSize2)[0])

        if sizeType1.lower() == 'mb' and sizeType2.lower() == 'mb':
            finalMB = fSize1 + fSize2
        elif sizeType1.lower() == 'gb' and sizeType2.lower() == 'gb':
            finalGB = fSize1 + fSize2
            finalMB = gb2mb(finalGB)
        elif sizeType1.lower() == 'mb' and sizeType2.lower() == 'gb':
            finalMB = fSize1 + gb2mb(fSize2)
        elif sizeType1.lower() == 'gb' and sizeType2.lower() == 'mb':
            finalMB = gb2mb(fSize1) + fSize2

        return str(math.floor(finalMB))+"MB", str(mb2gb(math.floor(finalMB)))+"GB"
    return fSize1, fSize2

def getDLfromArchive(link, sector):
    glink = "N/A"
    URL = str(link)
    page = requests.get(URL)


    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("main", id="content")
    if not results:
        print(results)
        sg.popup('Cloudflare has flagged you (archive area), wait a while or use vpn', non_blocking=False, keep_on_top=True, no_titlebar=True)


    divs = results.find_all("div")
    for div in divs:
        posts = div.find_all("p")
        if posts:
            for post in posts:
                if str(post).find("Game") != -1 or str(post).find("Update") != -1 or str(post).find("DLC") != -1:
                    links = post.find_all('a')
                    for alink in links:
                        if alink['href'].find("1fichier") != -1:
                            #print("Haha gotcha 1fichier, from"+sector+" :"+str(alink['href']))
                            return str(alink['href'])

def GetContent(link, name):
    notif("Getting Content...")
    gcode = "???"
    greg = "???"
    gamedl = "None Available"
    updl = "None Available"
    dlcdl = "None Available"
    size = "0"

    gameSize = "0mb"
    updateSize = "0mb"
    dlcSize = "0mb"

    SizeGB = "?? GB"
    SizeMB = "?? GB"

    notif("Making Request...")
    URL = str(link)
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("div", class_="su-spoiler-content su-u-clearfix su-u-trim")
    if not results or results == "None": #results will return 'None' if nothing found
        sg.popup(str(page)+' | Cloudflare has possibly flagged you, wait a while or use proxy', non_blocking=False, keep_on_top=True, no_titlebar=True)
        setclipboard(str(soup))

    posts = results.find_all("p")
    notif("Scraping Content...")
    for post in posts:
        if str(post).find("CUSA") != -1 or str(post).find("SLES") != -1 or str(post).find("SLUS") != -1:
            gcode = str(post);greg = gcode[-7:];greg = greg[:3];gcode = gcode[:13];gcode = gcode[-10:] # Extracting the game's CUSA and Region
        #==================================#
        if str(post).find("Game") != -1 or str(post).find("Link Download:") != -1:
            links = post.find_all('a')
            for alink in links:
                if alink['href'].find("1fichier") != -1:
                    glink = str(alink['href'])
                    gamedl = str(glink)
                    gameSize = GetSize(glink)
                if alink['href'].find("downloadgameps3") != -1:
                    glink = getDLfromArchive(str(alink['href']), "GAME")
                    gamedl = str(glink)
                    gameSize = GetSize(glink)
                if alink['href'].find("filecrypt") != -1:
                    gamedl = str(alink['href'])
                if alink['href'].find("mediafire") != -1:
                    gamedl = str(alink['href'])
                if alink['href'].find("mega") != -1:
                    gamedl = str(alink['href']) 
        #==================================#
        if str(post).find("Update") != -1:
            links = post.find_all('a')
            for alink in links:
                if alink['href'].find("1fichier") != -1:
                    glink = str(alink['href'])
                    updl = str(glink)
                    updateSize = GetSize(glink)
                if alink['href'].find("downloadgameps3") != -1:
                    glink = getDLfromArchive(str(alink['href']), "UPD")
                    updl = str(glink)
                    updateSize = GetSize(glink)
                if alink['href'].find("filecrypt") != -1:
                    updl = str(alink['href'])
                if alink['href'].find("mediafire") != -1:
                    updl = str(alink['href'])
                if alink['href'].find("mega") != -1:
                    updl = str(alink['href']) 
        #==================================#            
        if str(post).find("All DLC") != -1 or str(post).find("DLC:") != -1 or str(post).find("DLC : ") != -1:
            links = post.find_all('a')
            for alink in links:
                if alink['href'].find("1fichier") != -1:
                    glink = str(alink['href'])
                    dlcdl = str(glink)
                    dlcSize = GetSize(dlcdl)
                if alink['href'].find("downloadgameps3") != -1:
                    glink = getDLfromArchive(str(alink['href']), "DLC")
                    dlcdl = str(glink)
                    dlcSize = GetSize(glink)
                if alink['href'].find("filecrypt") != -1:
                    dlcdl = str(alink['href'])
                if alink['href'].find("mediafire") != -1:
                    dlcdl = str(alink['href'])
                if alink['href'].find("mega") != -1:
                    dlcdl = str(alink['href']) 
        #==================================#
    #==================================# 
    if str(gameSize) == "0mb" and str(updateSize) == "0mb" and str(dlcSize) == "0mb" and gamedl == "None Available": #If initial scrape misses links
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find("div", class_="su-spoiler-content su-u-clearfix su-u-trim")
        if not results:
            sg.popup('Cloudflare has flagged you, wait a while or use vpn', non_blocking=True, keep_on_top=True, no_titlebar=True)

        posts = results.find_all("a")
        notif("Re-Scraping Content...")
        for post in posts:
            #==================================#
            if post['href'].find("1fichier") != -1:
                        glink = str(post['href'])
                        gamedl = str(glink)
                        gameSize = GetSize(glink)
            if post['href'].find("downloadgameps3") != -1:
                        glink = getDLfromArchive(str(post['href']), "GAME")
                        gamedl = str(glink)
                        gameSize = GetSize(glink)
            if post['href'].find("filecrypt") != -1:
                        gamedl = str(post['href'])
            if post['href'].find("mediafire") != -1:
                        gamedl = str(post['href'])
            if post['href'].find("mega") != -1:
                        gamedl = str(post['href']) 
            #==================================#
    #==================================# 
    if str(gameSize) == "0":
        gameSize = "0mb"
    if str(updateSize) == "0":
        updateSize = "0mb"
    if str(dlcSize) == "0":
        dlcSize = "0mb"

    if gamedl == updl:
        updl = "[Included with Game]"
        if dlcdl != "None Available":
            SizeMB, SizeGB = addFileSizes(gameSize, dlcSize)
        else:
            SizeMB, SizeGB = addFileSizes(gameSize, "0mb")
    else:
        if updateSize != "0mb":
            SizeMB, SizeGB = addFileSizes(gameSize, updateSize)
        if dlcSize != "0mb":
            SizeMB, SizeGB = addFileSizes(gameSize, SizeMB)
        if updateSize == "0mb" and dlcSize == "0mb":
            SizeMB, SizeGB = addFileSizes(gameSize, "0mb")

    
    #==================================# 
    
    #==================================# 

    #==================================#                #Getting Game Icon :3
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("div", class_="post-body entry-content")
    if not results:
        sg.popup('Cloudflare has flagged you, wait a while or use vpn', non_blocking=True, keep_on_top=True, no_titlebar=True)
    posts = results.find_all("img", width=True, height=True)

    for link in posts:
        if link['src'].find("2.bp.blogspot") and link['width'] =="165":
            imageLink = link['src']
            pass
        if link['src'].find("1.bp.blogspot") and link['width'] =="175":
            imageLink = link['src']
            pass
    #==================================#
    # find game info in table border="7"
                            #tbody
                                #tr
    soup = BeautifulSoup(page.content, "html.parser")
    alltables = soup.findAll( "table", {"border":"7"} )

    gameAttributes = []
    for t in alltables:
        if t.find('span'):
            allspan = t.find_all('span')
            for span in allspan:
                gameAttributes.append(span.text)
    #t = [x for x in soup.findAll('span')]
    #print("Length of att table " + str(len(gameAttributes)))
    spanIndex = 0
    lastText = ""
    for spanText in gameAttributes:
        spanIndex = spanIndex + 1
        if lastText == "GENRE":
            genre = spanText
        if lastText == "LANGUAGES":
            lang = spanText
        if lastText == "LANGUAGE":
            lang = spanText
        if lastText == "RELEASE":
            release = spanText
        lastText = spanText

    #==================================# 

    col = sg.Column([[sg.Frame(name,
                                [[sg.Column([
                                                [sg.Text('Game: '+gcode+" | "+greg)],
                                                [sg.Text('Download: '+gamedl, k='gdl')],
                                                [sg.Text('Update: '+updl, k='udl'),],
                                                [sg.Text('DLC: '+dlcdl, k='ddl')],
                                                [sg.Text('Release: '+release)],
                                                [sg.Text('Genre: '+genre)],
                                                [sg.Text('Language: '+lang)],
                                                [sg.Text('Size: '+str(SizeGB)+" ("+str(SizeMB)+")")]
                                            ],
                                    pad=(0,0))
                                ]])
                    ]],pad=(0,0))
	
    col2 = sg.Column([[sg.Frame('Actions:',[[sg.Column([[sg.Button('Copy Game Link'), sg.Button('Copy Update Link'), sg.Button('Copy DLC Link'), ]],pad=(0,0))]])]], pad=(0,0)),

    layout2 = [
        [sg.Titlebar("PS4 Games")],
        [sg.Frame("Game Info", [[sg.Image(data=getImageData(imageLink), key="-ff-")]])],
        [col],
        [col2]
        ]

    window2 = sg.Window('Game Content', layout2, keep_on_top=True, finalize=True)

    #==================================# 

def GetSize(link):
    if link and link != 'None':
        URL = link
        if URL.find("&") != -1:
            URL = URL.rsplit('&',1)[0]
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")
        if soup.find("div", class_="center-container2"):
            return 0

        results = soup.find("table", class_="premium")
        if not results:
            print("Cloudflare is limiting you or something, wait a while")
        posts = results.find_all("td")

        for post in posts:
            if str(post).find('MB') != -1:
                newString = str(post)
                newString = newString.lstrip('<td class="normal">')
                newString = newString.rstrip('</td>')
                return newString
            elif str(post).find('GB') != -1:
                newString = str(post)
                newString = newString.lstrip('<td class="normal">')
                newString = newString.rstrip('</td>')
                return newString
        
    return 0

def getImageData(url):
    jpg_data = (
        cloudscraper.create_scraper(
            browser={"browser": "chrome", "platform": "windows", "mobile": False}
        )
        .get(url)
        .content
    )

    pil_image = Image.open(io.BytesIO(jpg_data))
    png_bio = io.BytesIO()
    pil_image.save(png_bio, format="PNG")
    png_data = png_bio.getvalue()

    return png_data

def refreshWindow(t):
    if t == 1:
        sg.theme('SystemDefaultForReal')
    elif t == 2:
        sg.theme('Dark')
    elif t == 3:
        sg.theme('DarkGrey12')

    layout = [  
        [sg.Titlebar("PS4 Games List")],
        [sg.Text(gameAmount, justification='center' )],
        [sg.Input(size=(40, 1), enable_events=True, default_text="Input Search...", key='-INPUT-'), sg.Button('Clear Search')],
        [sg.Listbox(my_item_list, key='-LB-', s=(51,20), select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED)],
        [sg.Column([[sg.Frame('Actions:',[[sg.Column([[sg.Button('Get Link'), sg.Button('Get Content'), sg.Button('Exit')]],size=(375,45), pad=(0,0))]])]], pad=(0,0))],
        [sg.Column([[sg.Frame('Settings:',[[sg.Column([[sg.Button('White Theme'), sg.Button('Green Theme'), sg.Button('Dark Theme'), sg.Button('Update')]],size=(375,45), pad=(0,0))]])]], pad=(0,0))],
        [sg.StatusBar('Coded by zbombr115', key='-STAT-')]
    ]

    window1 = sg.Window('PS4 Games List by zbombr115', layout, keep_on_top=True, finalize=True)
    return window1

#                           ==================================== Main Window Layout ====================================
sg.theme('SystemDefaultForReal')

layout = [  
    [sg.Titlebar("PS4 Games List")],
    [sg.Text(gameAmount, justification='center' )],
    [sg.Input(size=(40, 1), enable_events=True, default_text="Input Search...", key='-INPUT-'), sg.Button('Clear Search')],
    [sg.Listbox(my_item_list, key='-LB-', s=(51,20), select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED)],
    [sg.Column([[sg.Frame('Actions:',[[sg.Column([[sg.Button('Get Link'), sg.Button('Get Content'), sg.Button('Exit')]],size=(375,45), pad=(0,0))]])]], pad=(0,0))],
    [sg.Column([[sg.Frame('Settings:',[[sg.Column([[sg.Button('White Theme'), sg.Button('Green Theme'), sg.Button('Dark Theme'), sg.Button('Update')]],size=(375,45), pad=(0,0))]])]], pad=(0,0))],
    [sg.StatusBar('Coded by zbombr115', key='-STAT-')]
]

window1 = sg.Window('PS4 Games List by zbombr115', layout, keep_on_top=True, finalize=True)

def notif(strng):
    sg.popup_quick_message(strng, keep_on_top=True)

#                           ==================================== Event (Button) Handling ====================================

while True:

    window, event, values = sg.read_all_windows()
    if event == sg.WIN_CLOSED or event == 'Exit':
        window.close()
    if window != 'None':
        if window == window1:
            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            #==================================# 
            if event == 'Clear Search':
                window['-INPUT-'].Update("")
                values['-INPUT-']=''
                notif("Cleared Search!")
            if values['-INPUT-'] != '' and values['-INPUT-'] != 'Input Search...':
                searchElements = []
                search = values['-INPUT-']
                for a in my_item_list:
                    if a.shown.lower().find(search.lower()) != -1:
                        searchElements.append(a)

                window['-LB-'].update(searchElements)
            elif values['-INPUT-'] == '':
                window['-LB-'].update(my_item_list)
            #==================================#
            if event == 'Get Link':
                for item in values['-LB-']:
                    setclipboard(item.internal)
                    notif("Set Link To Clipboard!")
            elif event == 'Get Content':
                for item in values['-LB-']:
                    GetContent(item.internal, item.shown)
                    notif("Got Content for "+str(item.shown)+"!")
            elif event == 'Default Theme':
                window.close()
                sg.theme('SystemDefaultForReal')
                window1 = refreshWindow(1)
                notif("Set "+event)
            elif event == 'Green Theme':
                window.close()
                window1 = refreshWindow(2)
                notif("Set "+event)
            elif event == 'Dark Theme':
                window.close()
                window1 = refreshWindow(3)
                notif("Set "+event)
            elif event == 'Update':
                notif("parsing json...")

                col3 = sg.Column([[sg.Frame('Games:',[[sg.Column([[sg.Button('Update Games List'), sg.Button('Exit')]],pad=(0,0))]])]], pad=(0,0)),

                layout3 = [
                        [sg.Titlebar("Games")],
                        [col3],
                        [sg.Listbox(my_item_list, key='-ListBox-', s=(30,10), select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED)],
                ]

                window3 = sg.Window('Gamelist', layout3, keep_on_top=True, finalize=True)
        else:
            #==================================# 
            if event == "Copy Game Link":
                lnk = str(window['gdl'].get()).replace("Download: ", "")
                setclipboard(lnk)
                notif("Set Link To Clipboard!")
            #==================================# 
            if event == "Copy Update Link":
                lnk = str(window['udl'].get()).replace("Update: ", "")
                setclipboard(lnk)
                notif("Set Link To Clipboard!")
            #==================================# 
            if event == "Copy DLC Link":
                lnk = str(window['ddl'].get()).replace("DLC: ", "")
                setclipboard(lnk)
                notif("Set Link To Clipboard!")
            #==================================#
            if event == 'Update Games List':
                jfile = open('GameOutput.json', "w")

                URL = "https://dlpsgame.com/list-all-game-ps4/"
                notif("Requesting Content")
                page = requests.get(URL)


                notif("Scraping Page")
                soup = BeautifulSoup(page.content, "html.parser")
                results = soup.find("ol", class_="display-posts-listing")

                posts = results.find_all("li", class_="listing-item")
                
                notif("got "+str(len(posts))+" posts!")

                data = {}
                numero = 1

                for post_element in posts:
                    #notif("dumping game "+str(numero)+" of "+str(len(posts)))
                    link_url = post_element.find_all("a")[0]["href"]
                    gameName = post_element.text
                    data[gameName.encode('utf-8')] = link_url.encode('utf-8')

                    with open("GameOutput.json", "w") as write_file:
                        json.dump(str(data), write_file)

                    numero = numero + 1

                notif("Successfully dumped games, checking for new releases.")

                gamesListRaw, gameAmount = loadList()
                new_item_list = []
                foundDifferences = []

                for game in gamesListRaw: # Adding to item list
                    #print(game, a[game])
                    gameLink = gamesListRaw[game].decode()
                    gameName = game.decode()
                    ob = Item(gameLink, gameName)

                    new_item_list.append(ob)
                    pass

                s = set(my_item_list)

                foundDifferences.append(Item("", "New Games:"))

                for newgame in new_item_list:
                    found = False
                    for gname in my_item_list:
                        if newgame.shown in gname.shown:
                            found = True
                    
                    if not found:
                        foundDifferences.append(Item(newgame.internal, newgame.shown)) # Adding new games into list

                window3['-ListBox-'].update(foundDifferences)
                window1['-LB-'].update(new_item_list)
                my_item_list = new_item_list

    else:
        break

window.close()
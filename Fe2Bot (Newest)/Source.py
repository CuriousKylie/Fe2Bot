import discord
from typing import Literal
from discord import app_commands
from discord.ext import commands
import asyncio
import threading
import pathlib
import sys
import requests
import os
import json
import datetime
import srcomapi, srcomapi.datatypes as dt
import time
import ctypes
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager


ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

Prefix = '+'
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
Client = discord.Client(intents=intents)

tree = app_commands.CommandTree(Client)
Devs = set()

Load_Done = False
LeaderboardLength = 20
TestingPath = r'D:\User\desktop\New Folder\Fe2Bot (Newest)' # change path to where folder is
EmojiServer = 1096429917840887828

UserApi = 'https://users.roblox.com/'
thumbnailsApi = 'https://thumbnails.roblox.com/'
PresenceApi = 'https://presence.roblox.com/'
Profile = 'https://www.roblox.com/users/'
AuthApi = 'https://auth.roblox.com/'
CheckToken = 'https://accountsettings.roblox.com/v1/email'
MapInfoAPI = 'https://flood-escape-2.fandom.com/api.php?action=query&prop=revisions&titles=MAP&rvslots=*&rvprop=content&format=json'
GetImageFromWiki = 'https://flood-escape-2.fandom.com/wikia.php?controller=CuratedContent&method=getImage&title=FILE:'
DiscordJump = 'https://discord.com/channels/'


Emotes = dict()
BlackListed = {'1blindy'}
Status = 'josepeter1 is gone...'
MinAgeForSubmit = 5 # in days
HighestXPShow = 10
PFPSize = 180
idLength = 7
Width = 21
HardRunsCap = 10
HardSubmitCap = 3 # per day
CDTime = 4.5 
UpdateTime = 350
NameLimit = 50
SpeedrunUpdateTime = 1 #24 # in hours
Fe2PlaceId = 738339342
SRcomName = 'ROBLOX: Flood Escape 2'
PrivateServersFile = 'PrivateServers.txt'
Numbers = set('123456789')

SRcom_Loading_Done = False
LBXP_Calculation_Done = False
KillThreads = False
AccountToken = ''
Runs = dict()
RemoveSRWait = False
LastCheckTime = 0
Finished = 0
ValidPS = dict()
CheckQueue = dict()
CheckedNames = dict()
LoggedInCookies = list()
SubmitLimitUser = dict()
Total_Rank = dict()
SearchCache = dict()
OnCD = dict()
Maps = list()
MapsInfoCache = dict()
MapAcronyms = dict()
GuildSongInfos = dict()
CDMessageSent = set()
EdgeOptions = Options()
EdgeOptions.add_argument('--headless')
CheckDriver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=EdgeOptions)
CurrentlyRunning = False

DevOnly = {
    'ShutDown': {'shutdown', 'sd', 'off', 'goodbye', 'bye', 'shutoff', 'kill', 'turnoff'}, 
    'Talk': {'talk', 'say'},
    'ReloadCache': {'reloadcache', 'clearcache'}
    }

Commands = {
    'Universal': {'leaderboard', 'lb', 'board', 'lboard', 'leaderb'},
    'PlayerLB': {'playerlb', 'plrlb', 'lbplr', 'plrboard', 'playerboard', 'lbplayer'},
    'LBMonth': {'monthlb', 'lbmonth', 'boardmonth', 'monthboard'},
    # 'ResetTime': {'resettime', 'timeleft', 'lbreset', 'lbtime', 'timelft'},
    'Speedruns': {'speedruns', 'runs'},
    'MapInfo': {'mapinfo', 'map', 'infomap'},
    'ServerLinks': {'servers', 'serverlinks'},
    'HighestTotalXP': {'totalrank', 'totalxps', 'totalxp', 'totalranks'},
    'GetMaps': {'maps', 'mapnames', 'mapname', 'getmaps'},
    'MonthXPRankings': {'highestxps', 'monthxps', 'highmonthxp'},
    'Help': {'help', 'cmds', 'commands'}
    }

CommandInfo = {
    'PlayerLB': {'Args': '<Roblox name>', 'Info': 'Search for the specified player\'s Leaderboards!'},
    'LBMonth': {'Args': '<Month> <Year>', 'Info': "Search for Leaderboard months!"},
    'Speedruns': {'Args': '<Category (solo/duo)> <Sub-category (current/legacy)> <Map name (e.g: dark sci facility)>', 'Info': "Search for speedruns!"},
    'SubmitPS': {'Args': '<Private server link>', 'Info': "Submit private servers to be displayed at +GetPS!"},
    'MapInfo': {'Args': '<Map name>', 'Info': 'Get info of a certain map!'},
    'Play': {'Args': '<FE2 ost song name>', 'Info': 'Play a certain song (should be in a vc)'}
}

SpecialCommands = {
    'GetPS': {'privateservers', 'ps', 'privates', 'getps', 'displayservers', 'displayps'},
    'SubmitPS': {'submitps', 'privatesubmit', 'addserver', 'serveradd'},
    'Play': {'play'},
    'Skip': {'skip'}
}

MonthAlias = {
    'january': 'jan',
    'february': 'feb',
    'march': 'mar',
    'april': 'apr',
    'may': 'may',
    'june': 'un',
    'july': 'jul',
    'august': 'aug',
    'september': 'sept',
    'october': 'oct',
    'november': 'nov',
    'december': 'dec'
}

Categories = {
        'Glitchless Duos': 'duo',
        'Glitchless Solos': 'solo'
        }

SubCategories = ['legacy', 'current']



RobloxPSKeywords = [f'https://www.roblox.com/games/{str(Fe2PlaceId)}?', 'privateServerLinkCode=']

def CheckTest():
    if pathlib.Path(sys.executable).name == 'python.exe':
        os.chdir(TestingPath)
    else:
        coolpath = sys.executable
        os.chdir(os.path.dirname(coolpath))

CheckTest()

RobloxAccInfo = r'RobloxInfo.txt'

async def ReloadCache(args: list):
    ClearedCache = set()
    Message = args[1]
    if SRcom_Loading_Done == True:
        threading.Thread(target=SpeedrunAPI).start()
        ClearedCache.add('Speedruns')
    elif LBXP_Calculation_Done == True:
        file = open('TotalRank.txt', 'w')
        file.seek(0)
        file.truncate(0)
        file.close()
        threading.Thread(target=CalculateXP).start()
        ClearedCache.add('Total XP Rank')
    await Message.reply(f'Cleared cache for: {ClearedCache}')

def KillProcess():
    sys.exit()

async def DiscordShutdown(Msg):
    await Msg.reply("Bot is shutting off, goodbye!")
    try:
        await Client.close()
    except:
        print('Discord client has been turned off.')
        KillProcess()

def ShutDown(args):
    Msg, event = args[1], args[2]
    event.create_task(DiscordShutdown(Msg))
    print('he')
    try:
        global KillThreads
        KillThreads = True
        sys.exit()
    except SystemExit:
        print('Program successfully turned off! Program might take a while to stop!')
    except:
        print(sys.exc_info()[0])
        

def Check(Message: discord.Message):
    if not Message.author.bot and Message.content and Message.content[0] in Prefix:
        return Load_Done
    else:
        return None
    
def Format(text: str, middle: bool):
    TextStuff = text.split(' ')
    Placement, Name, XPEarned = TextStuff[0], TextStuff[1], TextStuff[2]
    SpacingPlacement = round(Width / 4) - len(Placement)
    SpacingName = Width - len(Name)

    SpacingName = ' ' * SpacingName
    SpacingPlacement = ' ' * SpacingPlacement
    text = f'{Placement}{SpacingPlacement}{Name}{SpacingName}{XPEarned}'

    return text

def EmbedFormat(Embed: discord.Embed, Type: str):
    Embed.color = discord.Color.blue()
    Embed.set_footer(text=Type, icon_url=Client.user.avatar.url)
    Embed.set_author(name='Flood Escape 2', icon_url='https://cdn.discordapp.com/attachments/1086796189875327136/1095700916604248074/Png.png')
    return Embed

def Capitalizer(StrToCapitalize: list):
    MapToUse = ''
    for word in StrToCapitalize:
        DashPlace = word.find('-')
        e = 0
        while True:
            if not str.isalpha(word[e]):
                e += 1
                continue
            break
        capitalize = e > 0 and f'{word[0:e]}{word[e].capitalize()}' or word[e].capitalize()
        e += 1
        if DashPlace != -1:
            MapToUse = f'{MapToUse == "" and "" or MapToUse}{capitalize + word[e:DashPlace + 1]}{word[DashPlace + 1].capitalize()}{word[DashPlace + 2:len(word)]} '
        else:
            MapToUse = f'{MapToUse == "" and "" or MapToUse}{capitalize + word[e:len(word)]} ' 

    return MapToUse.strip(' ')

def GetAcronymMaps(map: str):
    for acronym, fullname in MapAcronyms.items():
        if map.lower() == fullname.lower():
            return acronym
        
    return None

def GetMaps(args: list):
    Embed = discord.Embed(title='Maps and their acronyms:', description="")
    if SRcom_Loading_Done == True or RemoveSRWait == True:
        for mapname in Maps:
            mapname = Capitalizer(mapname.split(' '))
            acronym = GetAcronymMaps(mapname)
            Embed.description = f'{Embed.description == "" and "" or Embed.description}{mapname} ({acronym})\n'
    else:
        Embed.add_field(name='Fetching Maps!', value='Please wait, map fetching is still not done!')

    return EmbedFormat(Embed, 'Map List')

def GetNames(name: str):
    Names = set()
    NameHistory = None
    JsonTable = {
            'usernames': [
                name
            ],
            "excludeBannedUsers": False
        }
    while not NameHistory:
        try:
            PlayerInfo = json.loads(requests.post(url=UserApi + 'v1/usernames/users', json=JsonTable).content)['data']
            if len(PlayerInfo) >= 1:
                PlayerInfo = PlayerInfo[0]
                ActualName = PlayerInfo['name']
                DisplayName = PlayerInfo['displayName']
                UserId = PlayerInfo['id']
                IDJson = {
                            'userIds': [UserId]
                        }  
                NameHistory = json.loads(requests.get(url=UserApi + f'v1/users/{PlayerInfo["id"]}/username-history?limit={NameLimit}').content)
                if 'data' in NameHistory.keys(): 
                    for NameTable in NameHistory['data']:
                        Names.add(NameTable['name'].lower())
                else:
                    if name.lower() in CheckedNames.keys():
                        for username in CheckedNames[name.lower()]['Names']:
                            Names.add(username.lower())
                    else:
                        for info in CheckedNames.values():
                            if name.lower() in info['Names']:
                                for username in info['Names']:
                                    Names.add(username.lower())
                                break
                Names.add(ActualName.lower())
                Names.add(name.lower())
            else:
                return Names, None, None, None, None
        except:
            time.sleep(.5)
            continue


    return Names, DisplayName, ActualName, UserId, IDJson


def GetTotalRank(userid: int):
    if LBXP_Calculation_Done == True and userid:
        for place, info in Total_Rank.items():
            useridGiven = info['UserID']
            if useridGiven == userid:
                return place
        return 'No XP Rank!'
    elif not userid:
        return 'Player not found.'
    elif LBXP_Calculation_Done == False:
        return 'Still calculating XP, Please wait!!'
    
    return 'Player was blacklisted from Total XP Rank!!'

def FetchXPRanks():
    CheckedThisMonth = dict()
    htemp = list()
    placed = dict()
    with open('LB.txt', 'r') as LBFile:
        CurrentDate = None
        contents = LBFile.readlines()
        for text in contents:
            TempTable = {'XP': 0, 'Name': '', 'Date': ''}
            split = text.split(' ')
            if len(split) > 2:
                placement, name, xpamount = split[0], split[1], int(split[2].replace(',', ''))
                if not name in CheckedThisMonth[CurrentDate] and not name.lower() in BlackListed:
                    TempTable['XP'] = xpamount
                    TempTable['Name'] = name
                    TempTable['Date'] = CurrentDate
                    TempTable['Placement'] = placement
                    CheckedThisMonth[CurrentDate].insert(len(CheckedThisMonth[CurrentDate]) + 1, TempTable['Name'])
                    htemp.insert(len(htemp) + 1, TempTable)
            else:
                CurrentDate = text
                placed[CurrentDate] = set()
                CheckedThisMonth[CurrentDate] = list()
    with open('XPRankings.txt', 'w') as XPRankingFile:
        for place in range(1, len(htemp) + 1):
            HighestInfo = {'XP': 0, 'Name': '', 'Date': '', 'Placement': ''}
            for info in htemp:
                xp, name, date, pm = info['XP'], info['Name'], info['Date'], info['Placement']
                if xp > HighestInfo['XP'] and not name in placed[date]:
                    HighestInfo['XP'] = xp
                    HighestInfo['Name'] = name
                    HighestInfo['Date'] = date
                    HighestInfo['Placement'] = pm
            xp, name, date, pm = HighestInfo['XP'], HighestInfo['Name'], HighestInfo['Date'], HighestInfo['Placement']
            placed[date].add(name)
            XPRankingFile.write(f'{str(place)},{name},{date}')
    print('Done fetching monthly xp ranks!!')


def XPFormat(XP: int):
    XPEmojis = {
            100_000: Emotes['100k_XP'],
            500_000: Emotes['500k_XP'],
            1_000_000: Emotes['1m_XP'],
            2_000_000: Emotes['2m_XP'],
            3_000_000: Emotes['3m_XP'],
            4_000_000: Emotes['4m_XP'],
            5_000_000: Emotes['5m_XP'],
            25_000_000: Emotes['25m_XP'],
            50_000_000: Emotes['50m_XP']
        }
    xpemoji = None
    highestxp = 0
    for req, emoji in XPEmojis.items():
        if XP >= req and XP >= highestxp:
            xpemoji = emoji

    return f'{xpemoji} {"{:,}".format(XP)} XP'

def GetLBXPInfo(Start: int, Lines: int):
    Date = Lines[Start]
    with open('MonthTotalXPRankings.txt', 'r') as Rankings:
        Contents = Rankings.readlines()
        for text in Contents:
            datetext = text.split(',')[1]
            if datetext.lower() == Date.lower():
                print(text)
                info = text.split(',')
                rank, totalxp = info[0], int(info[2])
                break
                
        return XPFormat(totalxp), f'**#{rank}**/{len(Contents)}'

def FetchLBXPTotalRank():
    h = dict()
    e = set()
    with open('LB.txt', 'r') as LBFile:
        date = None
        Contents = LBFile.readlines()
        for text in Contents:
            text = text.strip('\n')
            splitted = text.split(' ')
            if len(splitted) <= 2:
                date = text
                h[date] = 0
            else:
                h[date] += int(text.split(' ')[2].replace(',', ''))
    with open('MonthTotalXPRankings.txt', 'r+') as TextFile:
        TextFile.truncate(0)
        for place in range(1, len(h) + 1):
            HighestInfo = {'XP': 0, 'Date': ''}
            for date, xp in h.items():
                if xp > HighestInfo['XP'] and date.lower() not in e:
                    HighestInfo['XP'] = xp
                    HighestInfo['Date'] = date
            e.add(HighestInfo['Date'].lower())
            TextFile.write(f'{place},{HighestInfo["Date"]},{HighestInfo["XP"]},\n')
    h.clear()
    print('done')


            
def GetXPRank(FindName: str, FindDate: str):
    with open('XPRankings.txt', 'r') as XPRankingFile:
        Contents = XPRankingFile.readlines()
        for content in Contents:
            splitted = content.split(',')
            place, name, date = splitted[0], splitted[1], splitted[2]
            if FindDate == date and FindName == name:
                return place

    
    
def PlayerLB(args: list):
    Statuses = {
        -2: [Emotes['notfound'], 'Not Found'],
        -1: [Emotes['deleted'], 'Account Deleted'],
        0: [Emotes['offline'], 'Offline'],
        1: [Emotes['website'], 'Website'],
        2: [Emotes['playing'], 'Playing'],
        3: [Emotes['studio'], 'In Studio']
    }

    def GetInfo(Name: str):
        Names = set()
        PFPUrl = ''
        ProfileURL = ''
        PlayerStatus = None
        CorrectName = None
        PlayerStatus = None
        DisplayName = None
        UserId = None
        TotalRankPlace = None
        Banned = False

        try:
            Names, DisplayName, CorrectName, UserId, JsonTable = GetNames(Name)
            if UserId and CorrectName:
                TotalRankPlace = GetTotalRank(UserId)
                ProfileURL = f'{Profile}{UserId}'
                if UserId in SearchCache.keys():
                    print('got from cache')
                    Cached = SearchCache[UserId]
                    if Cached['Banned'] == False:
                        PlayerStatus = json.loads(requests.post(url=f'{PresenceApi}v1/presence/users', json=JsonTable).content)['userPresences'][0]['userPresenceType']
                    else:
                        PlayerStatus = -1
                        return Cached['CorrectName'], Cached['DisplayName'], Cached['Names'], Cached['PFPUrl'], Cached['ProfileURL'], PlayerStatus, UserId, Cached['Banned'], TotalRankPlace
                ExtraPlayerInfo = json.loads(requests.get(url=f"{UserApi}/v1/users/{UserId}").content)
                if ExtraPlayerInfo['isBanned'] == False:
                    PlayerStatus = json.loads(requests.post(url=f'{PresenceApi}v1/presence/users', json=JsonTable).content)['userPresences'][0]['userPresenceType']
                else:
                    Banned = True
                    PlayerStatus = -1
                PFPUrl = json.loads(requests.get(url=f'{thumbnailsApi}v1/users/avatar-headshot?userIds={UserId}&size={str(PFPSize)}x{str(PFPSize)}&format=Png&isCircular=false').content)['data'][0]['imageUrl'] # still put this in cuz sometimes banned users has a pfp
            else:
                PlayerStatus = -2
            

        except Exception as E:
            print(f'{str(E)} ({sys.exc_info()[-1].tb_lineno})')

        return CorrectName, DisplayName, Names, PFPUrl, ProfileURL, PlayerStatus, UserId, Banned, TotalRankPlace
    
    def Format2():
        ToChange = f'Leaderboard count: {str(LBCount)} | Podium count: {str(PODCount)}\nTotal XP: {"{:,}".format(TotalXP)} | Average XP: {"{:,}".format(round(TotalXP/LBCount))}'
        name = lbName
        Formatting = {
            1: Emotes['Gold'],
            2: Emotes['Silver'],
            3: Emotes['Bronze']
        }
        XPEmojis = {
            100_000: Emotes['100k_XP'],
            500_000: Emotes['500k_XP'],
            1_000_000: Emotes['1m_XP'],
            2_000_000: Emotes['2m_XP'],
            3_000_000: Emotes['3m_XP'],
            4_000_000: Emotes['4m_XP'],
            5_000_000: Emotes['5m_XP'],
            25_000_000: Emotes['25m_XP'],
            50_000_000: Emotes['50m_XP']
        }
        monthyear = Content[linenum-placement]
        rawxp = split_text[2]
        XPToSend = XPFormat(xp)
        MonthlyXPRank = GetXPRank(name, monthyear)
        MonthlyXPRank = MonthlyXPRank and f'(#{MonthlyXPRank})' or ''
        if placement <= 3:
            Embed.add_field(name=monthyear, value=f'{Formatting[placement]} {name}\n{XPToSend} {MonthlyXPRank}')
        else:
            Embed.add_field(name=monthyear, value=f'#{placement} {name}\n{XPToSend} {MonthlyXPRank}')
        Embed.description = PlayerInfo + ToChange

    Name = args[1].lower()
    CorrectName, DisplayName, Names, PFPUrl, ProfileURL, PlayerStatus, UserID, Banned, TotalRankPlace = GetInfo(Name)
    Embed = discord.Embed(title=f'Leaderboards for {CorrectName} ({DisplayName}):')
    if PFPUrl != '':
        Embed.set_thumbnail(url=PFPUrl)
    if type(TotalRankPlace) == int:
        TotalRankPlace = f'#{TotalRankPlace}'
    TotalXP = 0
    LBCount = 0
    PODCount = 0
    PlayerInfo = f'Status: {Statuses[PlayerStatus][0]} ({Statuses[PlayerStatus][1]})\n Global Total XP Rank: {TotalRankPlace}\n'
    Embed.url = ProfileURL
    Embed.description = PlayerInfo
    with open('LB.txt') as LBFile:
        Content = LBFile.readlines()
        for linenum, text in enumerate(Content):
            lbName = text.split(' ')[1]
            for name in Names:
                if name.lower() == lbName.lower():
                    placement, split_text = int(str.replace(text.split(' ')[0], '#', '')), text.split(' ')
                    xp = int(str.replace(split_text[2], ',', ''))
                    TotalXP += xp
                    LBCount += 1
                    if placement <= 3:
                        PODCount += 1
                    Format2()
    if LBCount < 1:
        if LBXP_Calculation_Done == False and Banned:
            Embed.add_field(name='No Leaderboards', value=f"{CorrectName} might have leaderboards but cannot be fetched as of right now since calculations are still being done, please wait until calculations are done to get accurate results.")
        else:
            Embed.add_field(name='No Leaderboards', value=f'{CorrectName} doesn\'t have any leaderboards!')
    EmbedFormat(Embed, 'Leaderboard Search')
    if UserID and not UserID in SearchCache.keys() and LBXP_Calculation_Done == True:
        print(f'Saved to cache!! ({UserID})')
        SearchCache[UserID] = {'CorrectName': CorrectName, 'DisplayName': DisplayName, 'Names': Names, 'PFPUrl': PFPUrl, 'ProfileURL': ProfileURL, 'Banned': Banned}
    return Embed
    

def LBMonth(args: list):

    def AddNames(StartingLine: int, lines: list):
        count = 0
        LBText = Format(f'# User XP', True) + '\n'
        while count < LeaderboardLength:
            count += 1
            linetoadd = Format(lines[count + StartingLine], False)
            LBText = LBText + linetoadd + '\n'
        return LBText

    if not len(args) >= 3:
        return EmbedFormat(discord.Embed(title="If you're searching for a player, use ```+lb``` or ```+playerlb``` instead!"), 'Monthly Leaderboard')
    Month, Year = args[1].lower(), args[2]
    if not Month in MonthAlias.keys():
        for monthname, alias in MonthAlias.items():
            if alias in Month:
                Month = monthname.lower()
    MonthYear = f'{Month} {Year}'
    StartingLine = 0
    lines = list()
    with open('LB.txt') as LBFile:
        content = LBFile.read()
        FindLB = content.lower().find(MonthYear)
        if FindLB != -1:
            lines = content.splitlines()
            for linenum, text in enumerate(lines):
                if MonthYear in text.lower():
                    StartingLine = linenum
                    break
            LB_XP_Total, TotalRank = GetLBXPInfo(StartingLine, lines)
            LeaderboardText = f'```{AddNames(StartingLine, lines)}```'
            Embed = discord.Embed(title=f'Leaderboard Month: {lines[StartingLine]}', description=LeaderboardText)
            Embed.add_field(name='Total XP:', value=LB_XP_Total)
            Embed.add_field(name='Placement:', value=TotalRank)
        else:
            LeaderboardText = "Couldn't find any leaderboard history for the month!"
            Embed = discord.Embed(title=f'Leaderboard Month: {str.capitalize(MonthYear[0]) + MonthYear[1:len(MonthYear)]}', description=LeaderboardText)
    EmbedFormat(Embed, 'Monthly Leaderboard')
    return Embed

def MapInfo(Args: list):
    badsymbols = set("}{[],.`'|()</\>")
    NotsendSymbols = set("}{[]`'|")
    ImportantInfo = {
        'Difficulty:': 'difficulty = ',
        'Creator/s:': 'creator = ',
        'Buttons:': 'buttons = ',
        'Map_IDS:': 'id =',
        'In-game music:': 'bgm = ',
        'Image': 'image1 = ',
        'Lost Page:': 'lost page map event',
        'Rescue:': 'rescue mission'
        }
    DontInclude = {
        'location = ', 'status =', 'title1 = '
    }
    def RemoveHyperLink(text: str):
        HyperLinkSymbols = {
            '[[': '|'
                            }
        textToSend = text
        for start, end in HyperLinkSymbols.items():
            if start and end in text:
                StartRemove = 1
                EndRemove = 1
                StartRemove = textToSend.find(start)
                EndRemove = textToSend.find(end)
                textToSend = f'{textToSend[0:StartRemove]}{textToSend[EndRemove:len(textToSend)]}'
        return textToSend
    def check(text):
        for symbol in badsymbols:
            if symbol in text:
                text = text.replace(symbol, '') 
        for info in ImportantInfo.values():
            if info in text:
                return False
        for no in DontInclude:
            if no in text:
                return False
        h = text.split(' ')
        ToFind = {'fe2cm', ': '}
        lastword = ''
        for thing in ToFind:
            if thing in text:
                Location = text.find(thing) + len(thing)
                word = text[Location:Location + idLength + 1]
                if (len(word) > 5 and len(word) < 8) and (str.islower(word)) and not str.isalpha(word.replace(' ', '')):
                    return True
            else:
                continue
        if len(text) < 45 and len(h) < 6:
            wordsfile = open('words.txt', 'r')
            for word in h:
                if (len(word) > 5 and len(word) < 8) and (str.islower(word)) and not str.isalpha(word) and not word in wordsfile.readlines():
                    print(word, str.islower(word), str.isalpha(word))
                    return True

        return False
            
    def GetContent():
        ChangeChars = {'<br>': '\n', '*': '\*'}
        MapInformation = json.loads(requests.get(url=MapInfoAPI.replace('MAP', MapStr)).content)['query']['pages']
        PageNumber = list(MapInformation.keys())[0]
        ObtainedInfo = dict()
        for text in MapInformation[PageNumber]['revisions'][0]['slots']['main']['*'].split('\n'):
            for key, getinfo in ImportantInfo.items():
                if 'buttons' in key.lower() and getinfo in text:
                    if 'group' in text:
                        ObtainedInfo[key] = f'{key in ObtainedInfo.keys() and ObtainedInfo[key] or ""}{Emotes["GroupButtons"]} {text.replace(getinfo, "").strip("| ").replace("group", "Group: ")}\n'
                    else:
                        ObtainedInfo[key] = f'{key in ObtainedInfo.keys() and ObtainedInfo[key] or ""}{Emotes["Buttons"]} Normal: {text.replace(getinfo, "").strip("| ")}\n'
                elif 'ids' in key.lower() and (getinfo in text or check(text)):
                    for tochange, char in ChangeChars.items():
                        if tochange in text:
                            text = text.replace(tochange, char)
                    ObtainedInfo[key] = f'{key in ObtainedInfo.keys() and ObtainedInfo[key] or ""}{text.replace(getinfo, "").strip("| ")}\n'
                elif ('lost page' in key.lower() or 'rescue' in key.lower()) and getinfo in text.lower():
                    ObtainedInfo[key] = f'{key in ObtainedInfo.keys() and ObtainedInfo[key] or ""}{RemoveHyperLink(text)}\n'
                elif getinfo in text and text.strip('| ')[0:len(getinfo)].lower() == getinfo:
                    ObtainedInfo[key] = text.replace(getinfo, "").strip("| ")
                if len(ObtainedInfo) >= len(ImportantInfo):
                    break
        for name, info in ObtainedInfo.items():
            if 'creator' not in key.lower():
                text = RemoveHyperLink(text)
            for symbol in NotsendSymbols:
                if symbol != '.': 
                    info = info.replace(symbol, '')
            if 'difficulty' in name.lower():
                Embed.add_field(name=name, value=f'{Emotes[info.lower()]}{info}')
            elif 'image' in name.lower():
                try:
                    info = 'file:' in info.lower() and info[5:len(info)] or info
                    print(info)
                    ImageUrl = requests.get(url=f'{GetImageFromWiki}{info}').json()
                    if 'url' != None:
                        Embed.set_thumbnail(url=ImageUrl['url'].replace('50', '800'))
                except Exception as E:
                    print(str(E))
                    continue
            else:
                Embed.add_field(name=name, value=info)
        

    def Formatter(MapStr):
        MapToUse = ''
        MapToUse = Capitalizer(MapStr.split(' '))
        Embed.title = f'Map Info: {MapToUse}'
        MapToUse = MapToUse.strip(' ').replace(' ', '_')
        print(MapToUse)
        return MapToUse
        
    Embed = discord.Embed(title='Map Info:')
    Map = Args[1:len(Args)]
    MapStr = ' '.join(Map)
    if SRcom_Loading_Done == True or RemoveSRWait == True:
        if len(Args) > 2:
            if MapStr.lower() in Maps:
                MapStr = Formatter(MapStr)
                GetContent()
        elif len(Args) < 3 and MapStr.lower() in MapAcronyms.keys():
            MapStr = MapAcronyms[MapStr.lower()]
            MapStr = Formatter(MapStr)
            GetContent()
        elif len(Args) < 3 and MapStr.lower() in Maps:
            MapStr = Formatter(MapStr)
            GetContent()

    elif SRcom_Loading_Done == False or RemoveSRWait == False:
        Embed.description = "Fetching maps, please wait!"

    return EmbedFormat(Embed, 'Map Information')
        

def CheckPS(PrivateLink: str):
    DriverUsed = None
    DriverUsed = CheckDriver
    CheckDriver.get(PrivateLink)
    Found = None
    while not Found:
        time.sleep(2)
        try:
            Found = DriverUsed.find_element(By.XPATH, '//*[@id="modal-dialog"]/div/div[2]/div[1]/div[1]')
        except:
            continue
    if Found and 'no longer valid' in Found.text.lower():
        return False
    else:
        return True
    
def Help(args: list): 
    Embed = discord.Embed(title='Commands:', description='To get more info about the command, just send the command you want more info in without any arguments!')
    for name, aliases in Commands.items():
        if name != 'Universal':
            name = f'{Prefix}{name}'
        else:
            name = f'{name} (can be used for playerlb or lbmonth)'
        Embed.add_field(name=name, value=str(aliases))
    for name, aliases in SpecialCommands.items():
        Embed.add_field(name=f'{Prefix}{name}', value=str(aliases))
    return EmbedFormat(Embed, 'Help')

        

def CalculateXP():
    global LBXP_Calculation_Done
    CheckedNames.clear()
    with open('TotalRank.txt', 'r+') as RankFile:
        Contents = RankFile.readlines()
        if len(Contents) > 1 and not str.isalpha(Contents[0]) and float(Contents[0]) == os.path.getmtime('LB.txt'):
            print('LB file wasn\'t modified when this was last used, using cache')
            for info in Contents[1:len(Contents)]:
                info = info.split(' ')
                Placement, Name, XPEarned, UserID, Names = info[0], info[1], info[2], info[3], info[4].replace("'", '').split(',')
                DaInfo = {'UserID': UserID, 'Names': Names, 'ActualName': Name}
                CheckedNames[Name.lower()] = DaInfo
                CheckedNames[UserID] = DaInfo
                Total_Rank[int(Placement)] = {'Name': Name, 'XP': int(XPEarned), 'UserID': int(UserID)}
            print('Done applying cache to dictionary, calculation done')
            LBXP_Calculation_Done = True
            return
        else:
            RankFile.seek(0)
            RankFile.truncate(0)
            RankFile.write(f'{str(os.path.getmtime("LB.txt"))}\n')
            RankFile.close()
    TempRanks = dict() 
    def AlreadyChecked(userid):
        for info in Total_Rank.values():
            if info['UserID'] == userid:
                return True
        return False
    def NameAlreadyChecked(name: str):
        if len(CheckedNames) > 0:
            for info in CheckedNames.values():
                Names = info['Names']
                if name.lower() in Names:
                    return True
        return False
    def GetUserIDByName(name: str):
        for info in CheckedNames.values():
            UserID = info['UserID']
            if name.lower() in info['Names']:
                return UserID
        return None
    def Main(text: str, place: int):
        spacesplit = text.split(' ')
        if len(spacesplit) > 2:
            name, xp = spacesplit[1], spacesplit[2]
            if not NameAlreadyChecked(name):
                Names, DisplayName, ActualName, UserId, IDJson = GetNames(name)
                for blacklistedname in BlackListed:
                    if blacklistedname.lower() in Names:
                        print(f'{name} is blacklisted in highestxp, skipping')
                        return
                if UserId and ActualName:
                    TempRanks[UserId] = 0
                    DaInfo = {'UserID': UserId, 'Names': Names, 'ActualName': ActualName}
                    CheckedNames[ActualName.lower()] = DaInfo
                    CheckedNames[UserId] = DaInfo
                else:
                    print(f"Couldn't find USERID for player {name}!")
                    return
            UserId = GetUserIDByName(name)
            if UserId:
                TempRanks[UserId] += int(xp.replace(',', ''))
            else:
                print("UserID was made, but wasn't found.")
    with open('lb.txt', 'r') as File:
        contents = File.readlines()
        for linenum, text in enumerate(contents):
            linenum += 1
            Main(text, linenum)
            print(f'{linenum} lines out of {len(contents)} lines!')
    Placement = 0
    with open('TotalRank.txt', 'a') as RankFile:
        for _, _ in TempRanks.items():
            Placement += 1 
            HighestINFO = {'XP': 0, 'UserID': 0}
            for userid, xp in TempRanks.items():
                if xp > HighestINFO['XP'] and not AlreadyChecked(userid):
                    HighestINFO['XP'] = xp
                    HighestINFO['UserID'] = userid
            Total_Rank[Placement] = {'Name': CheckedNames[HighestINFO['UserID']]['ActualName'], 'XP': HighestINFO['XP'], 'UserID': HighestINFO['UserID'], 'Names': CheckedNames[HighestINFO['UserID']]['Names']}
            Info = Total_Rank[Placement]
            RankFile.write(f'{Placement} {Info["Name"]} {Info["XP"]} {Info["UserID"]} {str(Info["Names"]).replace("{", "").replace("}", "").replace(" ", "")} \n')
            if 'UserID' == 0:
                break
    CheckedNamesCopy = CheckedNames.copy()
    for key in CheckedNamesCopy.keys():
        if type(key) == int:
            del CheckedNames[key]
    print('Calculation of TotalXP is done!!!')
    LBXP_Calculation_Done = True
                    
def HighestTotalXP(args: list):
    Embed = discord.Embed(title=f'Top {HighestXPShow} highest total XP! (In leaderboard)')
    if LBXP_Calculation_Done == True:
        for place, info in Total_Rank.items():
            if place <= 10:
                Embed.add_field(name=place, value=f'Name: {info["Name"]}\nTotal XP: {"{:,}".format(info["XP"])}')
    else:
        Embed.description = 'Currently calculating XP, please wait!!'
    return EmbedFormat(Embed, 'Total XP')

def MonthXPRankings(args: list):
    Embed = discord.Embed(title=f'')
                                

async def SubmitPS(args: list):
    def CheckUser():
        timestamp = datetime.datetime.today().timestamp()
        if User.created_at.timestamp() < (timestamp - (MinAgeForSubmit * 86400)) and not User.id in SubmitLimitUser.keys():
            return True, None
        elif User.created_at.timestamp() > (timestamp - (MinAgeForSubmit * 86400)):
            return False, 'requirement'
        elif User.id in SubmitLimitUser.keys() and SubmitLimitUser[User.id] >= 3:
            return False, 'max'
        else:
            return True, None
        
    Embed = EmbedFormat(discord.Embed(title='Private Server Verification'), 'Private Servers')
    PrivateLink = args[1] 
    Message = args[len(args) - 1]
    if type(Message) == discord.Interaction:
        Messagecopy = Message
        User = Message.user
        class Message(object):
            pass
        Message.reply = Messagecopy.response.send_message
    else:
        User = Message.author
    UserCheck = CheckUser()
    if UserCheck[0]:
        checkcount = 0
        for item in CheckQueue.keys():
            if PrivateLink.lower() == item.lower():
                Embed.description = 'Link is already in queue! Please wait.'
                await Message.reply(embed=Embed)
                return
        for item in ValidPS.keys():
            if PrivateLink.lower() == item.lower():
                Embed.description = 'The link has already been accepted!'
                await Message.reply(embed=Embed)
                return
        for num, check in enumerate(RobloxPSKeywords):
            check = check.lower()
            if num == 0 and PrivateLink.lower().startswith(check):
                checkcount += 1
                continue
            elif check in PrivateLink.lower():
                checkcount += 1
            else:
                break
        if checkcount == len(RobloxPSKeywords):
            if not User.id in SubmitLimitUser.keys():
                SubmitLimitUser[User.id] = 0
            SubmitLimitUser[User.id] += 1
            CheckQueue[PrivateLink] = User.id
            Embed.description = f'Private server added in queue, will notify you here when the link is added/declined.'
            Embed.add_field(name='Estimated wait time:', value=f'{round(((LastCheckTime + UpdateTime) - datetime.datetime.today().timestamp() + (len(CheckQueue) * 3)) / 60, 2)} minutes') # made it a bit higher than usual
            await Message.reply(embed=Embed)
            Embed.remove_field(index=0)
            while True:
                await asyncio.sleep(3.5)
                if PrivateLink not in CheckQueue.keys():
                    if PrivateLink in ValidPS.keys():
                        Embed.description = 'Private server has successfully been added, Hooray!!'
                        Embed.add_field(name='Server:', value=f'Submitter: @{User.name}#{User.discriminator} (ID: {User.id})\nLink: {PrivateLink}')
                        await Message.reply(embed=Embed)
                        break
                    else:
                        Embed.description = 'Private server has expired or is not valid!!'
                        await Message.reply(embed=Embed)
                        break
        else:
            Embed.description = 'Private server link is invalid!!'
            await Message.reply(embed=Embed)
    elif UserCheck[1] == 'requirement':
        Embed.description = f"You don't meet the requirements to submit a private server ({MinAgeForSubmit} days account age)"
        await Message.reply(embed=Embed)
    elif UserCheck[1] == 'max':
        Embed.description = f"You can only submit {HardSubmitCap} private servers per day!!"
        await Message.reply(embed=Embed)

async def Talk(args: list):
    msg = args[len(args) - 2]
    tosend = msg.content[msg.content.find(' '):len(msg.content)]
    for h in msg.content.split(' '):
        if type(h) == str and not str.isalpha(h):
            #print(h)
            try:
                id = int(h)
                Channel = await Client.fetch_channel(id)
                await Channel.send(tosend.replace(h, ''))
                await msg.delete()
                return
            except (discord.NotFound, ValueError):
                continue
            except:
                break
    await msg.delete()
    await msg.channel.send(tosend)


async def GetPS(args: list):
    Embed = EmbedFormat(discord.Embed(title='Available Private Servers for FE2:'), 'Private Servers')
    Count = 0
    Message = args[len(args) - 1]
    if type(Message) == discord.Interaction:
        Messagecopy = Message
        class Message(object):
            pass
        Message.reply = Messagecopy.response.send_message
    for link, userid in ValidPS.items():
        ServerOwner = await Client.fetch_user(userid)
        Count += 1
        Embed.add_field(name=f'#{str(Count)}', value=f'Submitter: @{ServerOwner.name}#{ServerOwner.discriminator} | {ServerOwner.id}\nLink: {link}')
    await Message.reply(embed=Embed)

def CacheSpeedrun(Current: dict, Legacy: dict, map: str, type: str):
    for place, run in enumerate(Current.runs):
        place += 1
        run = run['run']
        players = None
        while not players:
            try:
                players = run.players
            except:
                time.sleep(.8)
        if place >= HardRunsCap:
            break

    for place, run in enumerate(Legacy.runs):
        place += 1
        run = run['run']
        players = None
        while not players:
            try:
                players = run.players
            except:
                time.sleep(.8)
        if place >= HardRunsCap:
            break
    global Finished
    Finished += 1

def GetAcronym(map: str):
    mapsplitted = map.split(' ')
    if len(mapsplitted) > 1:
        Acronym = ''
        h = 0
        for word in mapsplitted:
            if str.isalpha(word[h]):
                Acronym = f'{Acronym == "" and "" or Acronym}{word[h]}'
            else:
                h += 1
                while True:
                    Acronym = f'{Acronym == "" and "" or Acronym}{word[h]}'
                    if str.isalpha(word[h]):
                        break
        if Acronym in MapAcronyms.keys():
            count = 0
            while Acronym in MapAcronyms.keys():
                count += 1
                if count < len(word) and str.isalpha(word[count]):
                    Acronym = Acronym + word[count]
                elif count > len(word):
                    count = 1
                    Acronym = mapsplitted[0][count]
                else:
                    continue
                print(Acronym)
        return Acronym
    else:
        return None

def SpeedrunAPI():
    while True:
        if KillThreads:
            break
        global SRcom_Loading_Done
        SRcom_Loading_Done = False
        Runs.clear()
        Maps.clear()
        MapAcronyms.clear()
        try:
            api = srcomapi.SpeedrunCom(); api.debug = 1
            game = api.search(dt.Game, {'name': SRcomName})[0]
            for category in game.categories:
                if not category.name in Runs:
                    Runs[category.name] = {}
                for level in game.levels:
                    mapname = level.name.lower()
                    if not mapname in Runs[category.name].keys():
                        Runs[category.name][mapname] = {}
                    Current = None
                    Legacy = None
                    Variables = None
                    while not Variables:
                        try:
                            Variables = api.get(f'levels/{level.id}/variables')
                        except:
                            time.sleep(1.5)
                    VarID = Variables[0]['id']
                    for order, categid in enumerate(Variables[0]['values']['values']):
                        if order == 0:
                            Current = categid
                        else:
                            Legacy = categid
                    while (not SubCategories[0] in Runs[category.name][mapname].keys()) and (not SubCategories[1] in Runs[category.name][mapname].keys()):
                        try:
                            Runs[category.name][mapname][SubCategories[1]] = dt.Leaderboard(api, data=api.get(f"leaderboards/{game.id}/level/{level.id}/{category.id}?var-{VarID}={Current}"))
                            Runs[category.name][mapname][SubCategories[0]] = dt.Leaderboard(api, data=api.get(f"leaderboards/{game.id}/level/{level.id}/{category.id}?var-{VarID}={Legacy}")) # this causes an error, probably because some maps doesnt have any legacy records
                        except:
                            time.sleep(2)
                            continue
            print('Done loading all speedruns, now caching every speedrun.')
            for category in game.categories:
                for level in game.levels:
                    mapname = level.name.lower()
                    if not mapname in Maps:
                        Maps.insert(len(Maps), mapname)
                    if not mapname in MapAcronyms.values():
                        Acronym = GetAcronym(mapname.replace('-', ' '))
                        print(Acronym)
                        if Acronym:
                            MapAcronyms[Acronym] = mapname
                    while not Variables:
                        try:
                            Variables = api.get(f'levels/{level.id}/variables')
                        except:
                            time.sleep(1.5)
                    threading.Thread(target=CacheSpeedrun, args=(Runs[category.name][mapname][SubCategories[1]], Runs[category.name][mapname][SubCategories[0]], mapname, category.name)).start()
                while Finished < len(Maps):
                    time.sleep(1)
            SRcom_Loading_Done = True
            print('Fully loaded the speedruns.')
        except Exception:
             ex_type, ex_value, ex_traceback = sys.exc_info()
             print(f'{ex_type.__name__}: {ex_value} Line: {sys.exc_info()[-1].tb_lineno}')
        time.sleep(SpeedrunUpdateTime * 3600)
        #Runs = dict()

async def Play(args: list):
    Message = args[len(args) - 1]
    removesymb = "()[]"
    song_title = ""
    split = Message.content.split(' ')
    for e in split[1:len(split)]:
        song_title = f"{song_title} {e}"
    song_title = song_title.lower().strip(' ')
    Songs = os.listdir(f"{os.getcwd()}\\Songs")
    for e in Songs:
        if str.find(e.lower().strip('.mp3'), song_title) == 0:
            SongInfo = Message.guild.id in GuildSongInfos.keys() and GuildSongInfos[Message.guild.id] or False
            chan = Message.author.voice.channel
            if not chan:
                await Message.reply('You should be in a voice channel to use this!')
                break
            a = Message.guild.voice_client
            if not a or not a.is_connected():
                SongNumber = 0
                GuildSongInfos[Message.guild.id] = dict()
                SongInfo = GuildSongInfos[Message.guild.id]
                SongInfo['Queue'] = list()
                SongInfo['SongNumber'] = SongNumber
                SongQueue = SongInfo['Queue']
                SongQueue.insert(1, song_title)
                while True:
                    if not a or not a.is_connected(): # Checks again just in case someone disconnects the bot
                        a = await chan.connect()
                    if not a.is_playing() and SongNumber <= len(SongQueue) - 1:
                        SongNumber = GuildSongInfos[Message.guild.id]['SongNumber']
                        a.play(discord.FFmpegPCMAudio(executable='ffmpeg', source=f"{os.getcwd()}\\Songs\\{SongQueue[SongNumber]}.mp3"))
                        await Message.channel.send(f'Playing Song: {SongQueue[SongNumber]}')
                        SongNumber += 1
                        GuildSongInfos[Message.guild.id]['SongNumber'] = SongNumber
                    elif SongNumber >= len(SongQueue) - 1:
                        SongNumber = GuildSongInfos[Message.guild.id]['SongNumber']
                        SongNumber = 0
                        GuildSongInfos[Message.guild.id]['SongNumber'] = SongNumber
                        SongQueue.clear()
                    await asyncio.sleep(4)
            else:
                SongQueue = SongInfo['Queue']
                SongQueue.insert(999999, song_title)
                print(SongQueue)
                await Message.reply(f'Added in queue #{len(SongQueue)}: {song_title}')
            return
        else:
            continue

async def Skip(args: list):
    Message = args[len(args) - 1]
    SongNumber = Message.guild.id in GuildSongInfos.keys() and GuildSongInfos[Message.guild.id]['SongNumber'] or False
    VoiceClient = Message.guild.voice_client
    if VoiceClient and SongNumber:
        VoiceClient.stop()
        SongQueue = GuildSongInfos['Queue']
        GuildSongInfos[Message.guild.id]['SongNumber'] += 1
        if SongNumber <= len(SongQueue - 1): 
            VoiceClient.play(discord.FFmpegPCMAudio(executable='ffmpeg', source=f'{os.getcwd()}\\Songs\\{SongQueue[SongNumber + 1]}.mp3'))
        else:
            SongQueue.clear()
            GuildSongInfos[Message.guild.id]['SongNumber'] = 0

        





def Speedruns(Args: list):
    Embed = discord.Embed(title='Speedrun.com runs')
    if len(Args) >= 4 and SRcom_Loading_Done == True or RemoveSRWait == True:
        Type, subcateg, Map = Args[1], Args[2].lower(), Args[3:len(Args)]
        MapToShow = ""
        if len(Args) < 5 and not ' '.join(Map).lower() in Maps and Args[3].lower() in MapAcronyms.keys():
            Map = MapAcronyms[Args[3].lower()].split(' ')
        MapToShow = Capitalizer(Map)
        Map = MapToShow.lower()
        for key, value in Categories.items():
            if value in Type and Map in Runs[key].keys() and subcateg in SubCategories:
                Embed.title = f'Speedruns for map: {MapToShow}'
                Embed.description = f'{key}: {subcateg}'
                if len(Runs[key][Map][subcateg].runs) > 0:
                    for place, run in enumerate(Runs[key][Map][subcateg].runs):
                        run = run['run']
                        place += 1
                        players = ''
                        if len(run.players) >= 2:
                            for plr in run.players:
                                players = players == '' and plr.name or players + f', {plr.name}'
                        else:
                            players = run.players[0].name
                        thetime = run.times["realtime_t"] #/ 60
                        min = thetime / 60
                        sec = float("0." + str(min).split('.')[1]) * 60/1
                        millisec = float("0." + str(sec).split('.')[1]) * 1000/1
                        min = int(str(min).split('.')[0])
                        sec = int(str(sec).split('.')[0])
                        millisec = int(str(millisec).split('.')[0])
                        Embed.add_field(name= place <= 3 and Emotes[f'{place}sr'] or f'#{str(place)}', value=f'Player(s): {players}\nTime: {min}m {sec}s {millisec}ms \nDate: {run.date}' + '\n' + f'[Speedrun.com Link]({run.weblink})')
                        if place >= 10:
                            break
                    break
                else:
                    Embed.add_field(name='No records found', value=f'```No record was found for {Type} {subcateg}```')
    elif len(Args) < 4:
        Embed.description = "Missing arguments!"
    elif SRcom_Loading_Done == False or RemoveSRWait == False:
        Embed.description = "I'm still collecting data from speedrun.com, please try again later!!"
        Embed.set_thumbnail(url='https://media.discordapp.net/attachments/920310468051095634/1096952586856312862/yes.png')
    elif not Map in Runs[key].keys():
        Embed.description = "Map not found!!" 

    return EmbedFormat(Embed, 'Speedrun Search')

# def ResetTime():
#     Embed = discord.Embed(title='Reset Times')
    
#     return Embed

def PeriodicCheck():

    def SaveLink():
        with open(PrivateServersFile, 'a+') as File:
                h = File.read()
                if not serverlink in h:
                    File.write(f'{serverlink} {ownerid} \n')
    while True:
        if KillThreads:
            break
        global LastCheckTime
        LastCheckTime = datetime.datetime.today().timestamp()
        Removed = set()
        ValidPSCopy = ValidPS.copy()
        for serverlink, userid in ValidPSCopy.items():
            Valid = CheckPS(serverlink)
            if Valid:
                ValidPS[serverlink] = userid
            else: 
                Removed.add(serverlink)
                del ValidPS[serverlink]
        if len(Removed) > 0:
            print(f'Removed {str(len(Removed))} vip server links!!')
            with open(PrivateServersFile, 'r+') as File:
                Lines = File.readlines()
                File.seek(0)
                File.truncate()
                for text in Lines:
                    if not text.split(' ')[0] in Removed:
                        File.write(text)
        print(CheckQueue)
        CheckQueueCopy = CheckQueue.copy()
        for serverlink, ownerid in CheckQueueCopy.items():
            Valid = CheckPS(serverlink)
            if Valid:
                ValidPS[serverlink] = ownerid
                SaveLink()
            del CheckQueue[serverlink]
        time.sleep(UpdateTime)
        SearchCache.clear()

@Client.event
async def on_ready():
    for name in BlackListed.copy():
        Names = GetNames(name)
        for name in Names[0]:
            BlackListed.add(name.lower())
    Client.info = await Client.application_info()
    Devs.add(Client.info.owner.id)
    Emojis = await Client.fetch_guild(EmojiServer)   
    Emojis = await Emojis.fetch_emojis()
    for emoji in Emojis:
        EmoteName = emoji.name
        Emotes[EmoteName] = str(emoji)
    threading.Thread(target=SpeedrunAPI).start()
    threading.Thread(target=CalculateXP).start()
    with open('PrivateServers.txt', 'r') as PrivateServers:
        Servers = PrivateServers.readlines()
        for ServerInfo in Servers:
            ServerInfo = ServerInfo.split(' ')
            Server, Owner = ServerInfo[0], ServerInfo[1]
            ValidPS[Server] = Owner
    threading.Thread(target=PeriodicCheck).start()
    global Load_Done
    Load_Done = True
    await tree.sync()
    await Client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.playing, name=Status))
    FetchXPRanks()
    FetchLBXPTotalRank()
    print(f'**The bot ({Client.user.name}#{Client.user.discriminator}) is up!**')

def Cooldown(Message: discord.Message):
    OnCD[Message.author.id] = Message.created_at.timestamp() + CDTime
    while datetime.datetime.today().timestamp() < OnCD[Message.author.id]:
        time.sleep(.1)
    del OnCD[Message.author.id]
    if Message.author.id in CDMessageSent:
        CDMessageSent.remove(Message.author.id)


def GetArguments(command: str):
    if command == 'Universal':
        Embed = discord.Embed(title=f'Arguments of {command}', description=f'{CommandInfo["PlayerLB"]["Args"]} or {CommandInfo["LBMonth"]["Args"]}')
        Embed.add_field(name='Info:', value=CommandInfo["PlayerLB"]["Info"])
        Embed.add_field(name='Info:', value=CommandInfo["LBMonth"]["Info"])
    else:
        Embed = discord.Embed(title=f'Arguments of {command}', description=f'+{command} {CommandInfo[command]["Args"]}')
        Embed.add_field(name='Info:', value=CommandInfo[command]['Info'])
    return EmbedFormat(Embed, 'Command info')


def HashableObj(obj: dict):
    ToReturn = list()
    if type(obj) == dict:
        for value in obj.values():
            ToReturn.insert(len(ToReturn), value)
    elif type(obj) == list:
        return obj
    return ToReturn

def CheckPermissions(Channel: discord.TextChannel, Server: discord.Guild):
    if (not Server) or Channel.permissions_for(Server.me).send_messages:
        return True
    return False

@tree.command(name='playerlb', description=CommandInfo['PlayerLB']['Info'])
async def playerlb(interaction: discord.Interaction, name: str):
    await interaction.response.send_message(embed=PlayerLB(['+playerlb', name]))

@tree.command(name='lbmonth', description=CommandInfo['LBMonth']['Info'])
async def lbmonth(interaction: discord.Interaction, month: str, year: int):
    await interaction.response.send_message(embed=LBMonth(['+lbmonth', month, str(year)]))

@tree.command(name='speedruns', description=CommandInfo['Speedruns']['Info'])
async def speedruns(interaction: discord.Interaction, category: Literal[HashableObj(Categories)[0], HashableObj(Categories)[1]], subcategory: Literal[SubCategories[0], SubCategories[1]], map: str): # thge errors here is not real
    await interaction.response.send_message(embed=Speedruns(['+speedruns', category, subcategory, *map.split(' ')]))

@tree.command(name='submitps', description=CommandInfo['SubmitPS']['Info'])
async def submitps(interaction: discord.Interaction, link: str):
    asyncio.get_event_loop().create_task(SubmitPS(['+submitps', link, interaction]))

@tree.command(name='help')
async def help(interaction: discord.Interaction):
    await interaction.response.send_message(embed=Help(['+help']))

@tree.command(name='getps')
async def getps(interaction: discord.Interaction):
    asyncio.get_event_loop().create_task(GetPS(['+getps', interaction]))

@tree.command(name='mapinfo', description=CommandInfo['MapInfo']['Info'])
async def mapinfo(interaction: discord.Interaction, map: str):
    await interaction.response.send_message(embed=MapInfo(['+mapinfo', *map.split(' ')]))

@tree.command(name='totalxp')
async def totalxp(interaction: discord.Interaction):
    await interaction.response.send_message(embed=HighestTotalXP(['+highestxp']))

@tree.command(name='getmaps')
async def getmaps(interaction: discord.Interaction):
    await interaction.response.send_message(embed=GetMaps(['+getmaps']))

@Client.event
async def on_message(Message: discord.Message):
    ValidCMD = Check(Message)
    if ValidCMD and not Message.author.id in OnCD.keys():
        Command = Message.content.lower().split(' ')[0].strip('+')
        Args = Message.content.split(' ')
        Found = False
        for aliases in Commands.values():
            if Command in aliases:
                Found = True
                break
        for aliases in DevOnly.values():
            if Found:
                break
            elif Command in aliases:
                Found = True
                break
        for aliases in SpecialCommands.values():
            if Found:
                break
            elif Command in aliases:
                Found = True
                break
        if Found == True:
            CanSend = CheckPermissions(Message.channel, Message.guild)
            threading.Thread(target=Cooldown, args=(Message,)).start()
            if (not Message.guild) or (CanSend == True):
                if Message.author.id in Devs:
                    for DevCmd, alias in DevOnly.items():
                        if Command in alias:
                            if len(Args) < 2 and DevCmd in CommandInfo.keys():
                                await Message.reply(embed=GetArguments(DevCmd))
                            else:
                                print('joe mama so fat')
                                Args.insert(len(Args), Message)
                                Args.insert(len(Args), asyncio.get_event_loop())
                                await globals()[DevCmd](Args)
                            return
                    
                for key, alias in SpecialCommands.items():
                    if Command in alias:
                        if len(Args) < 2 and key in CommandInfo.keys():
                            await Message.reply(embed=GetArguments(key))
                        else:
                            Args.insert(len(Args), Message)
                            asyncio.get_event_loop().create_task(globals()[key](Args))
                        return

                for key, alias in Commands.items():
                    if Command in alias:
                        if key == 'Universal':
                            if len(Args) < 2:
                                await Message.reply(embed=GetArguments(key))
                            elif len(Args) >= 3 and str.isalpha(Args[2]) == False:
                                await Message.reply(embed=LBMonth(Args))
                            elif len(Args) < 3 and len(Args[1]) > 2 and len(Args[1]) < 21:
                                await Message.reply(embed=PlayerLB(Args))
                            else:
                               await Message.reply('Invalid name/date was given!')
                        else:
                            if len(Args) < 2 and key in CommandInfo.keys():
                                await Message.reply(embed=GetArguments(key))
                            else:
                                await Message.reply(embed=globals()[key](Args))
                        break
            elif CanSend == False:
                try:
                    Embed = discord.Embed(title=f'Failed to use: {Prefix + Command}', description=f'Please inform the owner (@{Message.guild.owner.name}#{Message.guild.owner.discriminator}) to allow me to send messages!\nAlternatively, you can use the commands here instead!')
                    Embed.add_field(name='Server:', value=f'[{Message.guild.name.encode("UTF-8", "ignore").decode()}]({DiscordJump}{Message.guild.id})')
                    Embed.add_field(name='Channel:', value=f'[#{Message.channel.name.encode("UTF-8", "ignore").decode()}]({Message.channel.jump_url})')
                    Embed = EmbedFormat(Embed, 'Permissions')
                    await Message.author.send(embed=Embed)
                except:
                    print(f"Couldn't send message to inform {Message.author.name}#{Message.author.discriminator}!")
    elif ValidCMD and Message.author.id in OnCD.keys():
        if not Message.author.id in CDMessageSent:
                CanSend = CheckPermissions(Message.channel, Message.guild)
                Embed = discord.Embed(title='Too fast!', description=f'Please wait **{round((OnCD[Message.author.id]) - datetime.datetime.today().timestamp(), 2)} seconds** before sending another command!!')
                Embed.add_field(name="Why does this even exist?", value='This was added as a precaution to prevent any slowdowns from the bot.')
                CDMessageSent.add(Message.author.id)
                if CanSend == True:
                    await Message.reply(embed=EmbedFormat(Embed, 'Ratelimit'))
                else:
                    await Message.author.send(embed=EmbedFormat(Embed, 'Ratelimit'))


Client.run(os.environ["DISCORD_TOKEN"])
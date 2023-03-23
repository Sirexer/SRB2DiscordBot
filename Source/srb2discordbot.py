#Set title of a console
import os
consoletitle = "SRB2 DiscordBot Console"
os.system("title " + consoletitle)


#Import python modules
from colorama import init, Fore
from colorama import Back
from colorama import Style
from tkinter import messagebox
from sys import stderr
import transliterate
import subprocess
import datetime
import tkinter
import discord
import shutil
import psutil
import json
import time
import json
import sys
import re


#Reset color after a function print
init(autoreset=True)


#Hide extra window when the program gives errors
root = tkinter.Tk()
root.withdraw()


#Text output about script information
print("Compliled with auto-py-to-exe 2.26.1 and pyinstaller 5.7.0")
print("Python 3.11.1 (tags/v3.11.1:a7a450f, Dec  6 2022, 19:58:39)")
print("Python modules:")
print("Discord 1.7.3")
print("Tkinter 0.1.0")
print("Colorama 0.4.6")
print("C data types 1.1.0")
print("Transliterate 1.10.2")
print("Regular Expression Engine 2.2.1")
print("JavaScript Object Notation 2.0.9\n")
print(Fore.GREEN + Style.BRIGHT + "===============================================================================")
print(Fore.GREEN + Style.BRIGHT + "      srb2discordbot.exe - Link your SRB2 server to your discord server!       ")
print(Fore.GREEN + Style.BRIGHT + "         Starts server with previous map and restarts on fatal error           ")
print(Fore.GREEN + Style.BRIGHT + "            Communicate via Discord with players on the SRB2 Server            ")
print(Fore.GREEN + Style.BRIGHT + "               View statistics of SRB2 Server and command support              ")
print(Fore.GREEN + Style.BRIGHT + "                     Created by Sirexer (i suck at python)                     ")
print(Fore.GREEN + Style.BRIGHT + "                            Discord: Sirexer#2004                              ")
print(Fore.GREEN + Style.BRIGHT + "                      Youtube: https:youtube.com/sirexer                       ")
print(Fore.GREEN + Style.BRIGHT + "                Discord Server DreamUniverse: http://srb2du.org              ")
print(Fore.GREEN + Style.BRIGHT + "===============================================================================")
print("SRB2DiscordBot v1.0 (19.03.2023)")
print(Fore.YELLOW + "Warning: Don't forget to add lua script to SRB2, the bot won't work without it.")
print("Setting up...")


#Chech the folder of program, if it does not exist, create it
if os.path.exists("srb2discordbot") == False:
    os.mkdir("srb2discordbot")
if os.path.exists("srb2discordbot/message-logs") == False:
    os.mkdir("srb2discordbot/message-logs")
if os.path.exists("srb2discordbot/srb2-logs") == False:
    os.mkdir("srb2discordbot/srb2-logs")
if os.path.exists("srb2discordbot/data") == False:
    os.mkdir("srb2discordbot/data")
if os.path.exists("srb2discordbot/backups") == False:
    os.mkdir("srb2discordbot/backups")
if os.path.exists("srb2discordbot/serverparameters") == False:
    os.mkdir("srb2discordbot/serverparameters")

    
#Set the start date of the program for log
timestart = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
mlogpath = "srb2discordbot/message-logs/mlogs-"+timestart+".txt"
create_file = open(mlogpath, "w+")
create_file.write("")
create_file.close()
print("Message logs will be written to " + mlogpath)


#Check files for lua, if they are missing, then create them
#This is necessary to avoid errors
if os.path.exists("luafiles") == False:
    os.mkdir("luafiles")
if os.path.exists("luafiles/client") == False:
    os.mkdir("luafiles/client")
if os.path.exists("luafiles/client/DiscordBot") == False:
    os.mkdir("luafiles/client/DiscordBot")
if os.path.isfile("latest-log.txt") == False:
    create_file = open("latest-log.txt", "w+")
    create_file.close()
for luafiles in "discordmessage.txt", "logcom.txt", "Messages.txt", "Players.txt", "Stats.txt", "console.txt":
    if os.path.isfile("luafiles/client/DiscordBot/"+luafiles) == False:
        create_file = open("luafiles/client/DiscordBot/"+luafiles, "w+")
        create_file.write("")
        create_file.close()

        
#Current map in SRB2, it is necessary to return the level
if os.path.isfile("srb2discordbot/data/map.sdb") == False:
    create_file = open("srb2discordbot/data/map.sdb", "w+")
    create_file.write("")
    create_file.close()
#Embeb message of server stats to remove past stats
if os.path.isfile("srb2discordbot/data/stats.sdb") == False:
    create_file = open("srb2discordbot/data/stats.sdb", "w+")
    create_file.write("")
    create_file.close()
#Current other cfg parameters
if os.path.isfile("srb2discordbot/data/cpcfg.sdb") == False:
    create_file = open("srb2discordbot/data/cpcfg.sdb", "w+")
    create_file.write("1")
    create_file.close()


#inputs
inp_token = None
inp_channelpost = None
inp_channelstatus = None
inp_channellog = None
inp_botprex = None
inp_srb2app = None
inp_address = None
inp_url = None
inp_debug = None
#Create config.json
def json_config():
    reg_id = re.compile("[^0-9]")
    global inp_token
    global inp_channelpost
    global inp_channelstatus
    global inp_channellog
    global inp_botprex
    global inp_srb2app
    global inp_address
    global inp_url
    global inp_debug
    if not inp_token:
        inp_token = input("Token of your discord bot:")
    while inp_token == "":
        messagebox.showwarning("Warning: Empty value.", "Token is needed to work with discord.")
        inp_token = input("Token of your discord bot:")
    inp_token = "\n\"token\": \""+inp_token+"\","
    if not inp_channelpost:
        inp_channelpost = input("Message channel ID:")
    while inp_channelpost == "":
        messagebox.showwarning("Warning: Empty value.", "Need a channel ID where there will be messages from the game.")
        inp_channelpost = input("Message channel ID:")
    inp_channelpost = (reg_id.sub('', inp_channelpost))
    inp_channelpost = "\n\"post_id\": "+inp_channelpost+","
    if not inp_channelstatus:
        inp_channelstatus = input("Information Channel ID:")
    while inp_channelstatus == "":
         messagebox.showwarning("Warning: Empty value.", "Need a channel ID where there will be Information from the game.")
         inp_channelstatus = input("Information Channel ID:")
    inp_channelstatus = "\n\"status_id\": "+inp_channelstatus+","
    if not inp_channellog:
        inp_channellog = input("Log channel ID(not necessary):")
        if inp_channellog == "":
            inp_channellog = "\"None\""
    inp_channellog = (reg_id.sub('', inp_channellog))
    inp_channellog = "\n\"log_id\": "+inp_channellog+","
    if not inp_botprex:
        inp_botprex = input("Prefix for the discord bot. Default ~srbot:")
        if inp_botprex == "":
            inp_botprex = "~srbot"
        elif inp_botprex != "":
            inp_botprex = inp_botprex.lower()
    inp_botprex = inp_botprex.translate({ord(' '): ''})
    inp_botprex = "\n\"botprefix\": \""+inp_botprex+"\","
    if not inp_srb2app:
        print(Fore.YELLOW + "Warning: If you are hosting multiple SRB2 servers on this computer, enter a new name for the SRB2 .exe file. For example \"my_server1\". (This is to avoid conflicts with other servers)")
        inp_srb2app = input("The new name of the SRB2 EXE file:")
        if inp_srb2app == "":
            inp_srb2app = "srb2win.exe"
        elif inp_srb2app != "":
            inp_srb2app = inp_srb2app.replace(".exe", '')
            inp_srb2app = inp_srb2app+".exe"
            inp_srb2app = inp_srb2app.lower()
    inp_srb2app = "\n\"srb2exe\": \""+inp_srb2app+"\","
    if not inp_address:
        inp_address = input("IP address of SRB2 Server(not necessary):")
    inp_address = "\n\"ip\": \""+inp_address+"\","
    if not inp_url:
        inp_url = input("Address where the level pictures are located(not necessary):")
        if inp_url == "":
            inp_url = "None.lol"
    inp_url = "\n\"url\": \""+inp_url+"\","
    if not inp_debug:
        inp_debug = "\n\"debug\": false"
    create_file = open("srb2discordbot/config.json", "w+")
    create_file.write("{"+inp_token+inp_channelpost+inp_channelstatus+inp_channellog+inp_botprex+inp_srb2app+inp_address+inp_url+inp_debug+"\n}")
    create_file.close()
#Check the config file, if it does not exist, create it
if os.path.isfile("srb2discordbot/config.json") == False:
    print("Creating a new .json file...")
    json_config()
    print("Config srb2discordbot/config.json is created.")

#Execute srb2discordbot/config.json
try:
    print("Executing config file srb2discordbot/config.json...")
    file_json = open("srb2discordbot/config.json", "r")
    config = json.load(file_json)
#If the file is damaged, then delete it and close the program
except json.decoder.JSONDecodeError:
    file_json.close()
    if os.path.isfile("srb2discordbot/backups/config.json") == True:
        shutil.copy(r'srb2discordbot/backups/config.json', 'srb2discordbot/config.json')
        messagebox.showerror("Error: Trouble with a config file.", "Invalid .json file configuration, it will be replaced from backup.")
    else:
        messagebox.showerror("Error: Trouble with a config file.", "Invalid .json file configuration, it will be deleted.")
        os.remove("srb2discordbot/config.json")
    exit()
#Check if there are all values in the config, if they are not, then add
json_notenough = False
try:
    if config["token"]:
        inp_token = str(config["token"])
except KeyError:
    json_notenough = True
try:
    if config["post_id"]:
        inp_channelpost = str(config["post_id"])
except KeyError:
    json_notenough = True
try:
    if config["status_id"]:
        inp_channelstatus = str(config["status_id"])
except KeyError:
    json_notenough = True
try:
    if config["log_id"]:
        inp_channellog = str(config["log_id"])
except KeyError:
    json_notenough = True
try:
    if config["botprefix"]:
        inp_botprex = str(config["botprefix"])
except KeyError:
    json_notenough = True
try:
    if config["srb2exe"]:
        inp_srb2app = str(config["srb2exe"])
except KeyError:
    json_notenough = True
try:
    if config["ip"]:
        inp_address = str(config["ip"])
except KeyError:
    json_notenough = True
try:
    if config["url"]:
        inp_url = str(config["url"])
except KeyError:
    json_notenough = True
try:
    if config["debug"] != None:
        inp_debug = str(config["debug"])
        if inp_debug == "False":
            inp_debug = "\n\"debug\": false"
        if inp_debug == "True":
            inp_debug = "\n\"debug\": true"
except KeyError:
    json_notenough = True
if json_notenough == True:
    print("Not all variables in the file recreate")
    json_config()
    file_json = open("srb2discordbot/config.json", "r")
    config = json.load(file_json)
    file_json.close()
shutil.copy(r'srb2discordbot/config.json', 'srb2discordbot/backups/config.json')


#Check if there is an exe file of the game and if there is a custom exe
if os.path.isfile(config["srb2exe"]) == False:
    while os.path.isfile("srb2win.exe") == False:
         messagebox.showwarning("Warning", "srb2win.exe was not found.")
         if os.path.isfile(config["srb2exe"]) == True:
             break
    if config["srb2exe"] != "srb2win.exe" and os.path.isfile("srb2win.exe") == True:
        shutil.copy(r'srb2win.exe', config["srb2exe"])


#Parameters for .exe srb2 file
print("Reading parameters from cfg file...")
if os.path.isfile("srb2discordbot/serverparameters/parameters.cfg") == False:
    print("The parameters.cfg file was not found, creating a new one...")
    print("Enter the parameters of the .exe file. For example \"-dedicated -server -room 33 -file...\"")
    inp_parameters = input("Parameters:")
    create_file = open("srb2discordbot/serverparameters/parameters.cfg", "w+")
    if inp_parameters != "":
        create_file.write(inp_parameters)
    elif inp_parameters == "":
        create_file.write("-dedicated -server 1 -room 33 -gametype 0 -file SRB2DiscordBot.wad")
    create_file.close()


#Program variables, they are neaded to have good synchronization and not only
isstarted = True
processsrb2 = None
statusfile = None
srbmessages = None
srbm = None
srbstats = None
msgstats = None
srblogcom = None
srblc = None
channel = None
embedstats = None
statchannel = None
stateditcount = 0
isdiscordborwork = False
botname = None
botavatar = None
log_lens = 0
twoxsdavoid = 0 
discordcmdmsg = None
srblog = None
embed_id = None
guild = None
server_isplaying = False
client = None
roles = {}
gametype = None
avoidautorestart = True
restart_mv = False
mapvalues = []
tr_completecount = None
completecount = 0
currentmap = None
pastmap = None
restart_pcfg = None
currentpcfg = None
countpcfg = None
gamepaused = False
url_cfgs = {}
emotes = {}
bannedsavemaps = []
allowroles = []
allowmembers = []

#Create empty configuration file for autorestart
if os.path.isfile("srb2discordbot/autorestart.cfg") == False:
    create_file = open("srb2discordbot/autorestart.cfg", "w+")
    create_file.write("//Customize this configuration if you need an auto restart\n\n")
    create_file.write("//mapvalue - restarts the server if game reaches desired map, use A0 instead of 100\n")
    create_file.write("//Examples:\n")
    create_file.write("//mapvalue = 01 - makes a autorestart on the map MAP01\n")
    create_file.write("//mapvalue = 01,a0,b0 - makes a autorestart on the maps MAP01, MAPA0, MAPB0\n")
    create_file.write("//mapvalue = none - does not autorestart due map, use \"none\" if you don't need it\n")
    create_file.write("mapvalue = none\n\n")
    create_file.write("//countvalue - restarts the server if so many maps have passed\n")
    create_file.write("//Examples:\n")
    create_file.write("//countvalue = 32 - if players have completed 32 levels no matter what, the server restarts\n")
    create_file.write("//countvalue = none - doing nothing\n")
    create_file.write("countvalue = none\n\n")
    create_file.write("//parameter_cfgs - how many parameters and they will change, this will not work if the server has been rebooted and due to errors or has been closed by the user\n")
    create_file.write("//Examples:\n")
    create_file.write("//parameter_cfgs = 3 - creates three parameter files and will change them after autorestart\n")
    create_file.write("//parameter_cfgs = 1 - doesn't create or change parameters, \"none\" can also be used\n")
    create_file.write("parameter_cfgs = none\n\n")
    create_file.write("//url_cfgX - changes link to images, if parameter_cfgs is greater than 3, make them larger\n")
    create_file.write("//Examples:\n")
    create_file.write("//url_cfg1 = srb2picturemap.org - Link will be changed for parameter number 1\n")
    create_file.write("//url_cfg2 = default - uses link from config.cfg\n")
    create_file.write("//url_cfg3 = none - removes the link\n")
    create_file.write("url_cfg1 = default\n")
    create_file.write("url_cfg2 = default\n")
    create_file.write("url_cfg3 = default\n")
    create_file.write("//url_cfg4 = default\n")
    create_file.close()
#Read autorestart.cfg
if os.path.isfile("srb2discordbot/autorestart.cfg") == True:
    file_autorestart = open("srb2discordbot/autorestart.cfg", "r")
    while True:
        #Current time
        now = datetime.datetime.now()
        line = file_autorestart.readline()
        if not line:
            break
        if line.find('=') == -1:
            continue
        if line.startswith("//"):
            continue
        line = line.translate({ord(' '): ''})
        line = line.translate({ord('\n'): ''})
        line = line.translate({ord(','): ' '})
        equals = line.find('=')
        if len(line) == equals+1:
            continue
        if line[equals+1:].lower().find("none") != -1 and not line.startswith("url_cfg"):
            continue
        if line[:equals].lower() == "mapvalue":
            restart_mv = True
            mapvalues = line[equals+1:].split()
            str_mapvalues = str(mapvalues)
            str_mapvalues = str_mapvalues.translate({ord(' '): ''})
            str_mapvalues = str_mapvalues.translate({ord('['): ''})
            str_mapvalues = str_mapvalues.translate({ord(']'): ''})
            str_mapvalues = str_mapvalues.translate({ord("'"): ''})
            print("Autorestart will turn on when the game reaches: "+str_mapvalues.upper())
            str_mapvalues = None
        elif line[:equals].lower() == "countvalue":
            try:
                tr_completecount = int(line[equals+1:])
            except ValueError:
                print("[" + now.strftime("%H:%M") + "]" + Fore.RED + 'Error:' + Style.RESET_ALL + ' ValueError in countvalue (expected intriger, got a letter)')
                continue
            print("Autorestart when "+str(tr_completecount)+" maps are completed")
        elif line[:equals].lower() == "parameter_cfgs":
            try:
               restart_pcfg = int(line[equals+1:]) 
            except ValueError:
                print("[" + now.strftime("%H:%M") + "]" + Fore.RED + 'Error:' + Style.RESET_ALL + ' ValueError in parameter_cfgs (expected intriger, got a letter)')
                continue
            if restart_pcfg <= 1:
                restart_pcfg = None
                continue
            if os.path.isfile("srb2discordbot/serverparameters/pcfg1.cfg") == False:
                print("Such parameters with a number will be reloaded after autorestart(which is specified in autorestart.cfg), the parameters.cfg file will always be used")
                print("Sequence: pcfg(count).cfg before parameters.cfg")
            for i in range(restart_pcfg):
                if os.path.isfile("srb2discordbot/serverparameters/pcfg"+str(i+1)+".cfg") == False:
                    int_pcfg = input("parameters for "+"pcfg"+str(i+1)+".cfg:")
                    create_file = open("srb2discordbot/serverparameters/pcfg"+str(i+1)+".cfg", "w+")
                    create_file.write(int_pcfg)
                    create_file.close()
        if restart_pcfg:
            if restart_pcfg >= 2:
                for i in range(restart_pcfg):
                    if line[:equals].lower() == "url_cfg"+str(i+1):
                        line = line.translate({ord(' '): ''})
                        line
                        line = line.translate({ord(','): ''})
                        if line[equals+1:].lower() == "none":
                            url_cfgs[str(i+1)] = "none"
                            print("url - removed for pcfg"+str(i+1)+".cfg")
                        elif line[equals+1:].lower() == "default":
                            url_cfgs[str(i+1)] = "default"
                            print("url - default for pcfg"+str(i+1)+".cfg")
                        elif line[equals+1:].find(".") == -1:
                            url_cfgs[str(i+1)] = "default"
                            print("Invalid link, no generic top-level domain for pcfg"+str(i+1)+".cfg")
                        else:
                            url_cfgs[str(i+1)] = line[equals+1:]
                            print("url - "+line[equals+1:]+" for pcfg"+str(i+1)+".cfg")
        now = None


#Create empty configuration file for emotes
if os.path.isfile("srb2discordbot/emotes.cfg") == False:
    create_file = open("srb2discordbot/emotes.cfg", "w+")
    create_file.write("//Emotes work on player skins, emeralds, ping, admin and completed\n")
    create_file.write("//Make sure it doesn't exceed 1024 characters in a single playerlist, otherwise there will be an error/n")
    create_file.write("//character emote example: \"sonic = :cyclone:\"\n\n")
    create_file.write("ping_red = :red_circle:\n")
    create_file.write("ping_yellow = :yellow_circle:\n")
    create_file.write("ping_green = :green_circle:\n")
    create_file.write("ping_blue = :blue_circle:\n")
    create_file.write("remote_admin = :star:\n")
    create_file.write("completed = :checkered_flag:\n")
    create_file.write("unknown = :grey_question:\n")
    create_file.write("spectator = :eye:\n")
    create_file.write("dead = :skull:\n")
    create_file.close()
totalemotes = 0
#Read emotes.cfg
if os.path.isfile("srb2discordbot/emotes.cfg") == True:
    file_emotes = open("srb2discordbot/emotes.cfg", "r")
    while True:
        line = file_emotes.readline()
        if not line:
            break
        if line.find('=') == -1:
            continue
        if line.startswith("//"):
            continue
        line = line.translate({ord(' '): ''})
        line = line.translate({ord('\n'): ''})
        equals = line.find('=')
        if len(line) == equals+1:
            continue
        emote_type = ":"+line[:equals].lower()+":"
        emote_value = line[equals+1:]
        emotes[emote_type] = emote_value
        totalemotes = totalemotes + 1
    if totalemotes > 0:
        if totalemotes == 1:
            print("Added "+str(totalemotes)+" emote")
        else:
            print("Added "+str(totalemotes)+" emotes")
        totalemotes = None
        

#Create empty configuration for dontsavemaps
#Which means that after the restart there will be a map before it
if os.path.isfile("srb2discordbot/dontsavemap.cfg") == False:
    create_file = open("srb2discordbot/dontsavemap.cfg", "w+")
    create_file.write("//These maps will not be saved\n")
    create_file.write("//it is useful that special stages are not included after the restart\n\n")
    create_file.write("//Single Special Stages\n")
    create_file.write("50,51,52,53,54,55,56,57\n")
    create_file.write("//Multiplayer Special Stages\n")
    create_file.write("60,61,62,63,64,65,66,67")
    create_file.close()
#Read dontsavemap.cfg
if os.path.isfile("srb2discordbot/dontsavemap.cfg") == True:
    file_maps = open("srb2discordbot/dontsavemap.cfg", "r")
    while True:
        line = file_maps.readline()
        if not line:
            break
        if line.startswith("//"):
            continue
        line = line.translate({ord(','): ' '})
        line = line.translate({ord('\n'): ''})
        if line == "":
            continue
        line = line.lower()
        bannedsavemaps = bannedsavemaps + line.split()
    str_bsm = str(bannedsavemaps)
    str_bsm = str_bsm.translate({ord(' '): ''})
    str_bsm = str_bsm.translate({ord('['): ''})
    str_bsm = str_bsm.translate({ord(']'): ''})
    str_bsm = str_bsm.translate({ord("'"): ''})
    print("list of maps that will not save: "+str_bsm.upper())


if os.path.isfile("srb2discordbot/commandperms.cfg") == False:
    create_file = open("srb2discordbot/commandperms.cfg", "w+")
    create_file.write("//Access to administrative command for members and roles\n\n")
    create_file.write("//Roles ID\n")
    create_file.write("roles = none\n")
    create_file.write("//Members ID\n")
    create_file.write("members = none")
    create_file.close()
if os.path.isfile("srb2discordbot/commandperms.cfg") == True:
    file_commandperms = open("srb2discordbot/commandperms.cfg", "r")
    while True:
        #Current time
        now = datetime.datetime.now()
        line = file_commandperms.readline()
        if not line:
            break
        if line.find('=') == -1:
            continue
        if line.startswith("//"):
            continue
        line = line.translate({ord(' '): ''})
        line = line.translate({ord('\n'): ''})
        line = line.translate({ord(','): ' '})
        equals = line.find('=')
        if len(line) == equals+1:
            continue
        if line[equals+1:].lower().find("none") != -1:
            continue
        if line[:equals].lower() == "roles":
            restart_mv = True
            allowroles = line[equals+1:].split()
            str_allowroles = str(allowroles)
            str_allowroles = str_allowroles.translate({ord(' '): ''})
            str_allowroles = str_allowroles.translate({ord('['): ''})
            str_allowroles = str_allowroles.translate({ord(']'): ''})
            str_allowroles = str_allowroles.translate({ord("'"): ''})
            print("Allowed roles for using commands: "+str_allowroles.upper())
            str_allowroles = None
        if line[:equals].lower() == "members":
            restart_mv = True
            allowmembers = line[equals+1:].split()
            str_allowmembers = str(allowmembers)
            str_allowmembers = str_allowmembers.translate({ord(' '): ''})
            str_allowmembers = str_allowmembers.translate({ord('['): ''})
            str_allowmembers = str_allowmembers.translate({ord(']'): ''})
            str_allowmembers = str_allowmembers.translate({ord("'"): ''})
            print("Allowed members for using commands: "+str_allowmembers.upper())
            str_allowmembers = None

#Change advenced parameters
def changeparameters():
    global restart_pcfg
    global currentpcfg
    global countpcfg
    if restart_pcfg:
        #Don't change it, if advenced parameters is empty
        if countpcfg == None:
            countpcfg_file = open("srb2discordbot/data/cpcfg.sdb", "r")
            try:
                countpcfg = int(countpcfg_file.read())
            except ValueError:
                if config["debug"] == True:
                    #Current time
                    now = datetime.datetime.now()
                    print("[" + now.strftime("%H:%M") + "]" + Fore.RED + 'Error:' + Style.RESET_ALL + ' ValueError in cpcfg.sdb (expected intriger, got string)')
                countpcfg = 1
            countpcfg_file.close()
            if countpcfg == "":
                countpcfg = 1
            if countpcfg > restart_pcfg:
                countpcfg = 1
                countpcfg_file = open("srb2discordbot/data/cpcfg.sdb", "w")
                countpcfg_file.write(str(countpcfg))
                countpcfg_file.close()
            currentpcfg_file = open("srb2discordbot/serverparameters/pcfg"+str(countpcfg)+".cfg", "r")
            currentpcfg = currentpcfg_file.read()
            currentpcfg_file.close()
        #Change it, if advenced parameters is not empty
        elif countpcfg != None:
            if countpcfg != restart_pcfg:
                countpcfg = countpcfg + 1
            else:
                countpcfg = 1
            currentpcfg_file = open("srb2discordbot/serverparameters/pcfg"+str(countpcfg)+".cfg", "r")
            currentpcfg = currentpcfg_file.read()
            currentpcfg_file.close()
            countpcfg_file = open("srb2discordbot/data/cpcfg.sdb", "w")
            countpcfg_file.write(str(countpcfg))
            countpcfg_file.close()


#Starting SRB2 Server
def startserver():
    global isstarted
    global srblog
    global server_isplaying
    global currentpcfg
    print("Starting server...")
    if currentpcfg == None:
        changeparameters()
    isstarted = False
    for proc in psutil.process_iter():
        name = proc.name()
        #Check if the server is running
        if name == config["srb2exe"]:
            #If the server is running, then wait for an answer
            isstarted = True
            restartsrb2 = input("Server already running, restart? (Y/n):")
            if restartsrb2.lower() == "yes" or restartsrb2.lower() == "y" or restartsrb2.lower() == "of course" or restartsrb2.lower() == "yeah":
                #Close the server if the answer is yes
                isstarted = False
                shutil.copy(r'latest-log.txt', "srb2discordbot/srb2-logs/log-" + timestart + ".txt")
                os.system("taskkill /f /im " + config["srb2exe"])
                log_file = open("latest-log.txt", "w")
                log_file.write("")
                log_file.close()
            else:
                server_isplaying = True
                #Get Gametype
                file_concole = open('luafiles/client/DiscordBot/console.txt', 'a')
                file_concole.write('gametype\n')
                file_concole.close
            break
    if isstarted == False:
        #Read parameters for the server
        file_parameters = open("srb2discordbot/serverparameters/parameters.cfg", "r")
        parameters = file_parameters.read()
        file_parameters.close()
        #Return the level that was the last time
        file_mapsrb2 = open("srb2discordbot/data/map.sdb", "r")
        mapsrb2 = file_mapsrb2.read()
        file_mapsrb2.close()
        #Start the server
        log_file = open("latest-log.txt", "w")
        log_file.write("")
        log_file.close()
        if currentpcfg == None:
            processsrb2 = subprocess.Popen(config["srb2exe"] + " " + mapsrb2 + " " + parameters)
        else:
            processsrb2 = subprocess.Popen(config["srb2exe"] + " " + mapsrb2 + " " + currentpcfg + " " + parameters)
        isstarted = True


#Restarting the server if it is closed for any reason
def restartserver():
    global isstarted
    global srblog
    global server_isplaying
    global currentpcfg
    global countpcfg
    global avoidautorestart
    server_isplaying = False
    avoidautorestart = True
    if srblog != None:
        shutil.copy(r'latest-log.txt', "srb2discordbot/srb2-logs/" + srblog)
        log_file = open("latest-log.txt", "w")
        log_file.write("")
        log_file.close()
    print("Restarting server...             ")
    for proc in psutil.process_iter():
        name = proc.name()
        #Close the crashed server
        if name == config["srb2exe"]:
            os.system("taskkill /f /im " + config["srb2exe"])
            break
    #Read parameters for the server
    file_parameters = open("srb2discordbot/serverparameters/parameters.cfg", "r")
    parameters = file_parameters.read()
    file_parameters.close()
    #Return the level that was the last time
    file_mapsrb2 = open("srb2discordbot/data/map.sdb", "r")
    mapsrb2 = file_mapsrb2.read()
    file_mapsrb2.close()
    #restart the server
    if countpcfg:
        currentpcfg_file = open("srb2discordbot/serverparameters/pcfg"+str(countpcfg)+".cfg", "r")
        currentpcfg = currentpcfg_file.read()
        currentpcfg_file.close()
    if currentpcfg == None:
        processsrb2 = subprocess.Popen(config["srb2exe"] + " " + mapsrb2 + " " + parameters)
    else:
        processsrb2 = subprocess.Popen(config["srb2exe"] + " " + mapsrb2 + " " + currentpcfg + " " + parameters)
    isstarted = True


#This function creates an embed containing information about the SRB2 server
def getsrbstats():
    #Get global variables
    global embedstats
    global botname
    global botavatar
    global gametype
    global restart_pcfg
    global currentpcfg
    global countpcfg
    global url_cfgs
    #Each line in the embed is 1024 characters max
    #So the list of the players divided into parts
    players = {1: '', 2: '', 3: '', 4: '',5: '', 6: '', 7: '', 8: ''}
    try:
        cline = 0 #Number of rows in one list
        plist = 1 #Numbers of lists
        #Open statistics of SRB2 Server
        srbstats = open('luafiles/client/DiscordBot/Stats.txt', 'r')
        #Get server name
        reg = re.compile("[^a-zA-Z0-9 !@#$%^&*()-_=+{}[]|\/?<>.,`~]")
        servername = srbstats.readline()
        servername = (reg.sub('', servername))
        #Get level name and map number
        gamemap = srbstats.readline()
        #Get map number only
        iconmap = srbstats.readline()
        #Get nextmap and map number
        nextlevel = srbstats.readline()
        #Get info about emeralds
        emeralds = srbstats.readline()
        for element in emotes:
            emeralds = emeralds.replace(element, emotes[element])
        #Get all skins on the server
        skins = srbstats.readline()
        for element in emotes:
            skins = skins.replace(element, emotes[element])
        #Get how much time has passed on a level
        leveltime = srbstats.readline()
        #Get how much time has passed since the launch of SRB2 server
        servertime = srbstats.readline()
        #Get count of players
        countp = srbstats.readline()
        #Get link of level image
        linktb = "http://"+config["url"]+"/levelpictures/thumbnail/"+iconmap+".png"
        if restart_pcfg:
            try:
                if url_cfgs[str(countpcfg)].lower() == "default":
                    linktb = "http://"+config["url"]+"/levelpictures/thumbnail/"+iconmap+".png"
                elif url_cfgs[str(countpcfg)].lower() == "none":
                    linktb = "http://none.kek/levelpictures/thumbnail/"+iconmap+".png"
                else:
                    linktb = "http://"+url_cfgs[str(countpcfg)]+"/levelpictures/thumbnail/"+iconmap+".png"
            except KeyError:
                pass
        #Remove a line break in URL
        linktb = (linktb.translate({ord('\n'): ''}))
        #EMBEDS!
        embedstats=discord.Embed(title=servername+" Statistics", url="https://bit.ly/3APCzSQ", description="Server information", color=0x00feff)
        embedstats.set_author(name=botname, url="https://ms.srb2.org", icon_url=botavatar)
        embedstats.set_thumbnail(url=linktb)
        embedstats.add_field(name="Leveltime", value=leveltime, inline=True)
        embedstats.add_field(name="Servertime", value=servertime, inline=True)
        embedstats.add_field(name="Players", value=countp, inline=True)
        embedstats.add_field(name="Map", value=gamemap, inline=True)
        embedstats.add_field(name="Nextmap", value=nextlevel, inline=True)
        if gametype:
            embedstats.add_field(name="Gametype", value=gametype, inline=True)
        embedstats.add_field(name="Emeralds", value=emeralds, inline=True)
        embedstats.add_field(name="Skins", value=skins, inline=True)
        #Split player list
        while True:
            if cline != 6 or (cline == 6 and plist == 8):
                line = srbstats.readline()
                for element in emotes:
                    line = line.replace(element, emotes[element])
                players[plist] = players[plist]+line
                cline = cline + 1
                if not line:
                    break
            #If there are 8 lines, create a new list and save the first list
            else:
                embedstats.add_field(name="Players list#"+str(plist), value=(players[plist]), inline=False)
                plist = plist +1
                cline = 0
        #Last list
        if players[plist] != '':
            embedstats.add_field(name="Players list#"+str(plist), value=(players[plist]), inline=False)
        embedstats.set_footer(text=servername+" "+config["ip"])
        srbstats.close()
        #Change a title of console
        consoletitle = ("SRB2 DiscordBot Console: " + servername)
        os.system("title " + consoletitle)
    except:
        if config["debug"] == True:
            print("[" + now.strftime("%H:%M") + "]" + Fore.RED + 'Error:' + Style.RESET_ALL + ' trouble in embed')


class MyClient(discord.Client):
    async def on_ready(self):
        global client
        try:
            await client.change_presence(status=discord.Status.dnd,activity=discord.Game("Launching a bot..."))
        except ConnectionResetError:
            if config["debug"] == True: #Display where the error occurred if debug is enabled
                print("[" + now.strftime("%H:%M") + "]" + Fore.RED + 'Error:' + Style.RESET_ALL + ' failed to update status')
        
        
        #Get global variables
        global srbmessages
        global srbm
        global channel
        global srbstats
        global msgstats
        global statchannel
        global embedstats
        global stateditcount
        global srblogcom
        global srblc
        global embed_id
        global guild
        global statusfile
        global botname
        global botavatar
        global isdiscordborwork
        global isstarted
        global srblog
        global twoxsdavoid
        global log_lens
        global processsrb2
        global roles
        global restart_mv
        global mapvalues
        global tr_completecount
        global completecount
        global bannedsavemaps
        global gametype
        global avoidautorestart
        global server_isplaying
        global currentmap
        global pastmap
        global gamepaused


        #Print bot name to console on successful connection
        print(Style.BRIGHT + Back.GREEN + 'SUCCESS:' + Style.RESET_ALL + Fore.GREEN + ' logged on as {0}!'.format(self.user))
        config["botprefix"] = config["botprefix"].translate({ord(' '): ''})
        print("Prefix for bot is "+config["botprefix"])
        try:
            guild_id = client.get_channel(config["post_id"]).guild.id
            #print(guild_id)
            guild = client.get_guild(guild_id)
            #print(guild)
            #print(",".join([str(r.id) for r in guild.roles]))
        #If the channel ID is not correct, display an error window and close the program
        except AttributeError:
            if config["debug"] == True:
                print("[" + now.strftime("%H:%M") + "]" + Fore.RED + 'Error:' + Style.RESET_ALL + ' failed ti get a guild ID')
            messagebox.showerror("Error: Improper Message or Log Channel ID has been passed.", "Check the channel ID, change it in the discordbot.json file.")
            exit()

        
        #Get bot name and avatar for embed
        botname = self.user
        botavatar = self.user.avatar_url
        twoxsdavoid = 2


        startserver()
        #Program loop
        while True:
            try:
                #Current time
                now = datetime.datetime.now()
                #Opening the log file
                file_log = open("latest-log.txt", "r")
                log = [l.strip() for l in file_log.readlines()]
                if log_lens != 0:
                    #Don't read what was readed
                    for line in log[log_lens:]:
                        if line.startswith("Entering main game loop..."):
                            await client.get_channel(config["post_id"]).send("✅`Server has been started!`✅")
                            print("[" + now.strftime("%H:%M") + "]" + Fore.YELLOW + "SRB2 Status Message: " + Style.RESET_ALL + "Server has been started!")
                            mlogs_file = open(mlogpath, "a")
                            mlogs_file.write("[" + now.strftime("%Y-%m-%d %H:%M:%S") + "]SRB2 Status Message: Server has been started!\n")
                            mlogs_file.close()
                            server_isplaying = True
                        elif line.startswith("Current gametype is "):
                            gametype = line[20:]
                        elif line.startswith("Logfile:"):
                            srblog = line[16:]
                        elif line.startswith("Map is now"):
                            #Write the current map to a file
                            if pastmap == None:
                                pastmap = line[12:17]
                            dbm = False
                            for element in bannedsavemaps:
                                if line[12:17].lower() == ("map"+element):
                                    dbm = True
                                    continue
                            if dbm == False:
                                if currentmap != None:
                                    pastmap = currentmap
                                currentmap = line[12:17]
                                mapsrb2 = "+map " + line[12:17]
                                file_mapsrb2 = open("srb2discordbot/data/map.sdb", "w")
                                file_mapsrb2.write(mapsrb2)
                                file_mapsrb2.close()
                            dbm = None
                            if tr_completecount:
                                completecount = completecount + 1
                            if currentmap == pastmap:
                                avoidautorestart = True
                            if avoidautorestart == False:
                                if restart_mv == True:
                                    for element in mapvalues:
                                        if "map"+element.lower() == line[12:17].lower():
                                            print("[" + now.strftime("%H:%M") + "]" + Fore.YELLOW + "SRB2 Status Message: " + Style.RESET_ALL + "Autorestart!")
                                            await client.get_channel(config["post_id"]).send("🔄`Autorestart!`🔄")
                                            await client.change_presence(status=discord.Status.dnd,activity=discord.Game("Restarting server..."))
                                            mlogs_file = open(mlogpath, "a")
                                            mlogs_file.write("[" + now.strftime("%Y-%m-%d %H:%M:%S") + "]SRB2 Status Message: Autorestart!\n")
                                            mlogs_file.close()
                                            avoidautorestart = True
                                            if tr_completecount:
                                                if completecount > tr_completecount:
                                                    completecount = 0
                                            changeparameters()
                                            restartserver()
                                #tr_completecount completecount
                                if tr_completecount != None:
                                    if avoidautorestart == False:
                                        if tr_completecount+1 == completecount:
                                            print("[" + now.strftime("%H:%M") + "]" + Fore.YELLOW + "SRB2 Status Message: " + Style.RESET_ALL + "Autorestart!")
                                            await client.get_channel(config["post_id"]).send("🔄`Autorestart!`🔄")
                                            await client.change_presence(status=discord.Status.dnd,activity=discord.Game("Restarting server..."))
                                            mlogs_file = open(mlogpath, "a")
                                            mlogs_file.write("[" + now.strftime("%Y-%m-%d %H:%M:%S") + "]SRB2 Status Message: Autorestart!\n")
                                            mlogs_file.close()
                                            completecount = 0
                                            changeparameters()
                                            restartserver()
                            else:
                                avoidautorestart = False
                            if server_isplaying == True:
                                print("[" + now.strftime("%H:%M") + "]" + Fore.YELLOW + "SRB2 Status Message: " + Style.RESET_ALL + line)
                                await client.get_channel(config["post_id"]).send("➡️`" + line + "`➡️")
                                mlogs_file = open(mlogpath, "a")
                                mlogs_file.write("[" + now.strftime("%Y-%m-%d %H:%M:%S") + "]SRB2 Status Message: " + line + "\n")
                                mlogs_file.close()
                        elif line.startswith("ERROR: Can't open "):
                            twoxsdavoid = 2
                            messagebox.showerror(line[18:] + " was not found or not valid." , "Find the addon file or remove it from srb2discordbot/serverparameters/parameters.cfg file.")
                            print("[" + now.strftime("%H:%M") + "]" + Fore.YELLOW + "SRB2 Status Message: " + Style.RESET_ALL + line[18:] + " was not found or not valid.")
                            mlogs_file = open(mlogpath, "a")
                            mlogs_file.write("[" + now.strftime("%Y-%m-%d %H:%M:%S") + "]SRB2 Status Message: " + line[18:] + " was not found or not valid.\n")
                            mlogs_file.close()
                            if msgstats != None:
                                try:
                                    await msgstats.delete()
                                    msgstats = None
                                    file_embed = open("srb2discordbot/data/stats.sdb", "w")
                                    file_embed.write("")
                                    file_embed.close()
                                except:
                                    pass
                            for i in reversed(range(0, 6)):
                                stderr.write(f"Restart server in {i:1d} seconds\r")
                                time.sleep(1)
                            await client.change_presence(status=discord.Status.dnd,activity=discord.Game("Restarting server..."))
                            restartserver()

                        
                        #Restart after server crash
                        elif line.startswith("Process killed by signal") or line.startswith("I_Error():") and not line.endswith("was not found or not valid."):
                            twoxsdavoid = 2
                            print("[" + now.strftime("%H:%M") + "]" + Fore.YELLOW + "SRB2 Status Message: " + Style.RESET_ALL + line)
                            await client.get_channel(config["post_id"]).send("❌`Server has shutdown`❌")
                            mlogs_file = open(mlogpath, "a")
                            mlogs_file.write("[" + now.strftime("%Y-%m-%d %H:%M:%S") + "]SRB2 Status Message: " + line + "\n")
                            mlogs_file.close()
                            if msgstats != None:
                                try:
                                    await msgstats.delete()
                                    msgstats = None
                                    file_embed = open("srb2discordbot/data/stats.sdb", "w")
                                    file_embed.write("")
                                    file_embed.close()
                                except:
                                    pass
                            await client.change_presence(status=discord.Status.dnd,activity=discord.Game("Restarting server..."))
                            restartserver()
                        #Restart after server has shutdown
                        elif line.startswith("I_ShutdownSystem():"):
                            if twoxsdavoid == 0:
                                await client.get_channel(config["post_id"]).send("❌`Server has shutdown`❌")
                                await client.change_presence(status=discord.Status.dnd,activity=discord.Game("Server has shutdown"))
                                print("[" + now.strftime("%H:%M") + "]" + Fore.YELLOW + "SRB2 Status Message: " + Style.RESET_ALL + "Server has shutdown")
                                mlogs_file = open(mlogpath, "a")
                                mlogs_file.write("[" + now.strftime("%Y-%m-%d %H:%M:%S") + "]SRB2 Status Message: Server has shutdown\n")
                                mlogs_file.close()
                                if msgstats != None:
                                    try:
                                        await msgstats.delete()
                                        msgstats = None
                                        file_embed = open("srb2discordbot/data/stats.sdb", "w")
                                        file_embed.write("")
                                        file_embed.close()
                                    except:
                                        pass
                                for i in reversed(range(0, 6)):
                                    stderr.write(f"Restart server in {i:1d} seconds\r")
                                    time.sleep(1)
                                await client.change_presence(status=discord.Status.dnd,activity=discord.Game("Restarting server..."))
                                restartserver()
                        elif line.startswith("WARNING:"):
                            if server_isplaying == True:
                                if config["log_id"] != "None":
                                    await client.get_channel(config["log_id"]).send(line)
                log_lens = len(log)
                if twoxsdavoid == 0:
                    #Check if the program is closed
                    isstarted = False
                    for proc in psutil.process_iter():
                        name = proc.name()
                        if name == config["srb2exe"]:
                            isstarted = True
                            break
                    #Restart if it is closed
                    if isstarted == False:
                        if server_isplaying == True:
                            await client.get_channel(config["post_id"]).send("❌`Server has shutdown`❌")
                            await client.change_presence(status=discord.Status.dnd,activity=discord.Game("Server has shutdown"))
                        print("[" + now.strftime("%H:%M") + "]" + Fore.YELLOW + "SRB2 Status Message: " + Style.RESET_ALL + "Server has shutdown")
                        mlogs_file = open(mlogpath, "a")
                        mlogs_file.write("[" + now.strftime("%Y-%m-%d %H:%M:%S") + "]SRB2 Status Message: Server has shutdown\n")
                        mlogs_file.close()
                        if msgstats != None:
                            try:
                                await msgstats.delete()
                                msgstats = None
                                file_embed = open("srb2discordbot/data/stats.sdb", "w")
                                file_embed.write("")
                                file_embed.close()
                            except:
                                pass
                        for i in reversed(range(0, 6)):
                            stderr.write(f"Restart server in {i:1d} seconds\r")
                            time.sleep(1)
                        twoxsdavoid = 2
                        await client.change_presence(status=discord.Status.dnd,activity=discord.Game("Restarting server..."))
                        restartserver()
                if twoxsdavoid != 0:
                    twoxsdavoid = twoxsdavoid - 1
            #If the channel ID is not correct, display an error window and close the program
            except AttributeError:
                messagebox.showerror("Error: Improper Message or Log Channel ID has been passed.", "Check the channel ID, change it in the discordbot.json file.")
                exit()
                #Don't close the program on any error
            except discord.errors.Forbidden:
                 messagebox.showerror("Error: Missing Permissions", "No access to the channel, give access to read and send messages for bot.")
            except ConnectionResetError:
                if config["debug"] == True: #Display where the error occurred if debug is enabled
                    print("[" + now.strftime("%H:%M") + "]" + Fore.RED + 'Error:' + Style.RESET_ALL + ' failed to update status')
            except discord.errors.HTTPException:
                if config["debug"] == True:
                    print("[" + now.strftime("%H:%M") + "]" + Fore.RED + 'Error:' + Style.RESET_ALL + ' there was a problem sending a request to Discord')
            except:
                if config["debug"] == True:
                    print("[" + now.strftime("%H:%M") + "]" + Fore.RED + 'Error:' + Style.RESET_ALL + ' unknown error while reading latest-log.txt file')
            time.sleep(0.5) #Timer

            
            if server_isplaying == True:
                try:
                    #Open the file and find out how many players are on the server and send it to the status
                    statusfile = open('luafiles/client/DiscordBot/Players.txt', 'r')
                    text_game = statusfile.read()
                    if text_game.find("Game is paused") != -1:
                        dstatus=discord.Status.idle
                        gamepaused = True
                    else:
                        dstatus=discord.Status.online
                        gamepaused = False
                    game = discord.Game("("+config["botprefix"]+"). "+text_game)
                    statusfile.close
                    await client.change_presence(status=dstatus,activity=game)
                    dstatus = None
                #If the connection was interrupted for a second, don't close the program
                except ConnectionResetError:
                    if config["debug"] == True: #Display where the error occurred if debug is enabled
                        print("[" + now.strftime("%H:%M") + "]" + Fore.RED + 'Error:' + Style.RESET_ALL + ' failed to update status')
                except discord.errors.HTTPException:
                    if config["debug"] == True:
                        print("[" + now.strftime("%H:%M") + "]" + Fore.RED + 'Error:' + Style.RESET_ALL + ' failed to update status. discord.errors.HTTPException')

                
                if isdiscordborwork == True:
                    #Outputting messages from the game and passing them to the channel
                    try:
                        srbmessages = open('luafiles/client/DiscordBot/Messages.txt', 'r')
                        srbm = srbmessages.read()
                        srbmessages.close()
                    #If the file is busy, don't close the program
                    except PermissionError:
                        if config["debug"] == True:
                            print("[" + now.strftime("%H:%M") + "]" + Fore.RED + 'Error:' + Style.RESET_ALL + ' unable to read Messages.txt file because it is busy')
                    #Send a message to discord
                    if srbm != '':
                        try:
                            srbmessages = open('luafiles/client/DiscordBot/Messages.txt', 'w')
                            srbmessages.write('')
                            srbmessages.close()
                            await self.get_channel(config["post_id"]).send(srbm)
                            srbm = srbm.translate({ord('*'): ''})[:-1]
                            mlogs_file = open(mlogpath, "a")
                            mlogs_file.write(("[" + now.strftime("%Y-%m-%d %H:%M:%S") + "]SRB2 Message: " + srbm).translate({ord('\n'): "\n[" + now.strftime("%Y-%m-%d %H:%M:%S") + "]" +  'SRB2 Message: '})+"\n")
                            mlogs_file.close()
                            srbm = srbm.translate({ord('\n'): "\n[" + now.strftime("%H:%M") + "]" + Fore.BLUE + Style.BRIGHT + 'SRB2 Message: ' + Style.RESET_ALL})
                            for delemote in ":rocket:", ":boot:", ":red_square:", ":o:", ":hammer:", ":door:", ":pencil2:":
                                srbm = srbm.replace(delemote, '')
                            print("[" + now.strftime("%H:%M") + "]" + Fore.BLUE + Style.BRIGHT + 'SRB2 Message:' + Style.RESET_ALL + ' ' + srbm)
                        #If the channel ID is not correct, display an error window and close the program
                        except AttributeError:
                            messagebox.showerror("Error: Improper Message Channel ID has been passed.", "Check the channel ID, change it in the discordbot.json file.")
                            exit()
                        except PermissionError:
                            if config["debug"] == True:
                                print("[" + now.strftime("%H:%M") + "]" + Fore.RED + 'Error:' + Style.RESET_ALL + ' unable to edit Messages.txt file because it is busy.')
                        except discord.errors.Forbidden:
                             messagebox.showerror("Error: Missing Permissions", "No access to the channel, give access to read and send messages for bot.")
                        #Don't close the program on any error
                        except:
                                if config["debug"] == True:
                                    print("[" + now.strftime("%H:%M") + "]" + Fore.RED + 'Error:' + Style.RESET_ALL + ' unknown error while reading Messages.txt file')

                                    
                    #Outputting command logs from the game and passing them to the channel
                    if config["log_id"] != "None":
                        try:
                            srblogcom = open('luafiles/client/DiscordBot/logcom.txt', 'r')
                            srblc = srblogcom.read()
                            srblogcom.close()
                        #If the file is busy, don't close the program
                        except PermissionError:
                            if config["debug"] == True:
                               print("[" + now.strftime("%H:%M") + "]" + Fore.RED + 'Error:' + Style.RESET_ALL + ' unable to read logcom.txt file because it is busy.')
                        if srblc != '':
                            try:
                                srblogcom = open('luafiles/client/DiscordBot/logcom.txt', 'w')
                                srblogcom.write('')
                                srblogcom.close()
                                await self.get_channel(config["log_id"]).send(srblc)
                                srblc = srblc.translate({ord('`'): ''})[:-1]
                                mlogs_file = open(mlogpath, "a")
                                mlogs_file.write(("[" + now.strftime("%Y-%m-%d %H:%M:%S") + "]Commands logs: " + srblc).translate({ord('\n'): "\n[" + now.strftime("%Y-%m-%d %H:%M:%S") + "]" +  'Commands logs: '})+"\n")
                                mlogs_file.close()
                                srblc = srblc.translate({ord('\n'): "\n[" + now.strftime("%H:%M") + "]" + Fore.CYAN + Style.BRIGHT + 'Commands logs: ' + Style.RESET_ALL})
                                print("[" + now.strftime("%H:%M") + "]" + Fore.CYAN + Style.BRIGHT + 'Commands logs:' + Style.RESET_ALL + ' ' + srblc)
                            #If the channel ID is not correct, display an error window and close the program
                            except AttributeError:
                                messagebox.showerror("Error: Improper Log Channel ID has been passed.", "Check the channel ID, change it in the discordbot.json file.")
                                exit()
                            except PermissionError:
                                if config["debug"] == True:
                                    print("[" + now.strftime("%H:%M") + "]" + Fore.RED + 'Error:' + Style.RESET_ALL + ' unable to edit logcom.txt file because it is busy')
                            except discord.errors.Forbidden:
                                 messagebox.showerror("Error: Missing Permissions", "No access to the channel, give access to read and send messages for bot.")
                            #Don't close the program on any error
                            except:
                                if config["debug"] == True:
                                    print("[" + now.strftime("%H:%M") + "]" + Fore.RED + 'Error:' + Style.RESET_ALL + ' unknown error while reading logcom.txt file')

                                    
                    #Create a new embed
                    if msgstats == None or (stateditcount >= 100 and msgstats != None):
                        try:
                            getsrbstats()
                            statchannel = self.get_channel(config["status_id"])
                            file_embed = open("srb2discordbot/data/stats.sdb", "r")
                            embed_id = file_embed.read()
                            if embed_id != "":
                                embed_id = int(embed_id)
                                msgstats = await statchannel.fetch_message(embed_id)
                            file_embed.close()
                            if msgstats != None:
                                await msgstats.delete()
                            msgstats = await statchannel.send(embed=embedstats)
                            file_embed = open("srb2discordbot/data/stats.sdb", "w")
                            file_embed.write(str(msgstats.id))
                            file_embed.close()
                            stateditcount = 0

                            
                        #If the channel ID is not correct, display an error window and close the program
                        except AttributeError:
                            messagebox.showerror("Error: Improper Information Channel ID has been passed.", "Check the channel ID, change it in the discordbot.json file.")
                            exit()

                            
                        #if embed was removed from text file
                        except discord.errors.NotFound:
                            msgstats = await statchannel.send(embed=embedstats)
                            file_embed = open("srb2discordbot/data/stats.sdb", "w")
                            file_embed.write(str(msgstats.id))
                            file_embed.close()
                            stateditcount = 0
                        except discord.errors.Forbidden:
                             messagebox.showerror("Error: Missing Permissions", "No access to the channel, give access to read and send messages for bot.")
                        except discord.errors.HTTPException:
                            if config["debug"] == True:
                                print("[" + now.strftime("%H:%M") + "]" + Fore.RED + 'Error:' + Style.RESET_ALL + ' failed to create embed with information. discord.errors.HTTPException')
                        #Don't close the program on any error
                        except:
                            if config["debug"] == True:
                                print("[" + now.strftime("%H:%M") + "]" + Fore.RED + 'Error:' + Style.RESET_ALL + ' failed to create embed with information')

                                
                    #Editing an existing embed
                    if msgstats != None and stateditcount <= 100:
                        try:
                            getsrbstats()
                            await msgstats.edit(embed=embedstats)
                            stateditcount = stateditcount + 1
                        #If embed was deleted, create a new one
                        except discord.errors.NotFound:
                            if config["debug"] == True:
                                print(Style.BRIGHT + "[" + now.strftime("%H:%M") + "]" + Fore.YELLOW + 'Warning:' + Style.RESET_ALL + ' message was deleted, creating a new message...')
                            msgstats = await statchannel.send(embed=embedstats)
                            file_embed = open("srb2discordbot/data/stats.sdb", "w")
                            file_embed.write(str(msgstats.id))
                            file_embed.close()
                            stateditcount = 0
                        except discord.errors.Forbidden:
                             messagebox.showerror("Error: Missing Permissions", "No access to the channel, give access to read and send messages for bot.")
                        except discord.errors.HTTPException:
                            if config["debug"] == True:
                                print("[" + now.strftime("%H:%M") + "]" + Fore.RED + 'Error:' + Style.RESET_ALL + ' failed to update embed with information. discord.errors.HTTPException')
                        #Don't close the program on any error
                        except:
                            if config["debug"] == True:
                                print("[" + now.strftime("%H:%M") + "]" + Fore.RED + 'Error:' + Style.RESET_ALL + ' failed to update embed with information')

                                
    #Works when someone sends a message to discord
    async def on_message(self, message):
        global discordcmdmsg
        global server_isplaying
        global gamepaused
        #Current time
        now = datetime.datetime.now()
        #Create a list of allowed characters that will not be removed from the message
        reg = re.compile('[^a-zA-Zа-б0-9 !@#$%^&*()-_=+{}[]|\/?<>.,`~]\n')
        channel = self.get_channel(config["post_id"])
        #Ignore the message if it was sent by the bot
        if message.channel == channel and message.author != self.user and not message.content.startswith(config["botprefix"]) and gamepaused == False:
            #Change role ID to role name
            rolelens = 0
            while message.content[rolelens:].find('<@&') != -1:
                role_ValueError = False
                rolefind = message.content.find('<@&')
                roleend = message.content[rolelens+rolefind:].find('>')+rolefind
                role_code = (message.content[rolelens+rolefind:rolelens+roleend+1])
                try:
                    if role_code.startswith("<@&") and role_code.endswith(">"):
                        role_id = int(role_code[3:-1])
                    else:
                        rolelens = rolelens+rolefind+2
                        continue
                except ValueError:
                    role_ValueError = True
                    rolelens = rolelens+rolefind+2
                if role_ValueError == False:
                    try:
                        role_object = guild.get_role(role_id)
                    except discord.errors.NotFound:
                        role_object = None
                    if role_object != None:
                        message.content = message.content.replace(role_code, "@"+role_object.name)
                    else:
                       message.content = message.content.replace(role_code, "@invalid-role")
            #Change user ID to nickname on the server
            userlens = 0
            while message.content[userlens:].find('<@') != -1:
                user_ValueError = False
                userfind = message.content.find('<@')
                userend = message.content[userlens+userfind:].find('>')+userfind
                user_code = (message.content[userlens+userfind:userlens+userend+1])
                try:
                    if user_code.startswith("<@") and user_code.endswith(">"):
                        user_id = int(user_code[2:-1])
                    else:
                        userlens = userlens+userfind+2
                        continue
                except ValueError:
                    user_ValueError = True
                    userlens = userlens+userfind+2
                if user_ValueError == False:
                    try:
                        user_object = await guild.fetch_member(user_id)
                    except discord.errors.NotFound:
                        user_object = None
                    if user_object != None:
                        message.content = message.content.replace(user_code, "@"+user_object.display_name+'#'+user_object.discriminator)
                    else:
                        message.content = message.content.replace(user_code, "@invalid-user#0000")
            #Change channel ID to channel name
            channellens = 0
            while message.content[channellens:].find('<#') != -1:
                channel_ValueError = False
                channelfind = message.content.find('<#')
                channelend = message.content[channellens+channelfind:].find('>')+channelfind
                channel_code = (message.content[channellens+channelfind:channellens+channelend+1])
                try:
                    if channel_code.startswith("<#") and channel_code.endswith(">"):
                        channel_id = int(channel_code[2:-1])
                    else:
                        channellens = channellens+channelfind+2
                        continue
                except ValueError:
                    channel_ValueError = True
                    channellens = channellens+channelfind+2
                if channel_ValueError == False:
                    try:
                        channel_object = guild.get_channel(channel_id)
                    except discord.errors.NotFound:
                        channel_object = None
                    if channel_object != None:
                        message.content = message.content.replace(channel_code, "#"+channel_object.name)
                    else:
                        message.content = message.content.replace(channel_code, "#invalid-channel")
            #Output to console
            discordcmdmsg = Fore.MAGENTA + Style.BRIGHT +  'Discord Message: ' + Style.RESET_ALL + '<{0.author.display_name}#{0.author.discriminator}> {0.content}'.format(message)
            discordcmdmsg = (discordcmdmsg.translate({ord('\n'): ' '}))
            print("[" + now.strftime("%H:%M") + "]" + discordcmdmsg)
            mlogs_file = open(mlogpath, "a")
            mlogs_text = "[" + now.strftime("%Y-%m-%d %H:%M:%S") + "]Discord Message: <{0.author.display_name}#{0.author.discriminator}> {0.content}".format(message) + "\n"
            mlogs_text = (reg.sub('', mlogs_text))
            mlogs_file.write(mlogs_text)
            mlogs_file.close()
            #Format the message
            try:
                message.content = transliterate.translit(message.content, reversed=True)
            except transliterate.exceptions.LanguageDetectionError:
                pass
            content = ('\"{0.author.display_name}#{0.author.discriminator}: {0.content}\" '.format(message))
            content = (content.translate({ord('\n'): ' '}))
            content = (reg.sub('', content))
            #Open a file and write message
            dmsg = open('luafiles/client/DiscordBot/discordmessage.txt', 'a')
            dmsg.write('\"'+content+'\" ')
            dmsg.close
        elif message.channel == channel and message.author != self.user and gamepaused == True:
            await message.add_reaction("⏸")
            
            

        #Bot commands
        try:
            if config["botprefix"] != "None":
                if message.author != self.user:
                    if message.content.startswith(config["botprefix"]):
                        allowedformember = False
                        for element in allowmembers:
                            try:
                                memberid = int(element)
                            except ValueError:
                                pass
                            if message.author.id == memberid:
                                allowedformember = True
                                break
                        if allowedformember == False and message.guild != None:
                            for element in allowroles:
                                try:
                                    roleid = int(element)
                                except ValueError:
                                    pass
                                for roles in message.author.roles:
                                    if roles.id == roleid:
                                        allowedformember = True
                                        break

                                    
                        if message.content.startswith(config["botprefix"]+"help"):
                            command_embed=discord.Embed(title="List of commands", description=config["botprefix"]+"kick - Kicks a player off the server\n"+config["botprefix"]+"ban - Bans a player on the server\n"+config["botprefix"]+"map - Changes the map on the server\n"+config["botprefix"]+"csay - Sends a message to everyone within a netgame which is displayed in the center of the screen\n"+config["botprefix"]+"exitlevel - Skips the current server map\n"+config["botprefix"]+"restart - Restarts the server", color=0xffff00)
                            command_embed.set_author(name=botname, url="https://ms.srb2.org", icon_url=botavatar)
                            await message.channel.send(embed=command_embed, reference=message)
                            command_embed = None

                                    
                        if allowedformember == True:

                            
                            if message.content.startswith(config["botprefix"]+"kick"):
                                if message.content != config["botprefix"]+"kick" and message.content != config["botprefix"]+"kick " and message.content.startswith(config["botprefix"]+"kick "):
                                    if gamepaused == False and server_isplaying == True:
                                        content = ('{0.content}\n'.format(message))
                                        #Format the message
                                        spacefind = content.find(" ")
                                        content = (content.translate({ord('\n'): ' '}))
                                        content = (content.translate({ord('\"'): 'а'}))
                                        content = (content.translate({ord('\''): 'б'}))
                                        content = content[spacefind+1:]
                                        content = (reg.sub('', content))
                                        content = (content.translate({ord('а'): '\"'}))
                                        content = (content.translate({ord('б'): '\''}))
                                        #Open a file and write message
                                        dcon = open('luafiles/client/DiscordBot/console.txt', 'a')
                                        dcon.write("kick "+content+'\n')
                                        dcon.close
                                        await message.add_reaction("✅")
                                    elif server_isplaying == False:
                                        await message.add_reaction("❌")
                                        '''
                                        command_embed=discord.Embed(title="⛔Server has shutdown⛔", description="You cannot use this command while the server is down or restarting", color=0xff0000)
                                        await message.channel.send(embed=command_embed, reference=message)
                                        command_embed = None
                                        '''
                                    elif gamepaused == True:
                                        command_embed=discord.Embed(title="⏸Game is Paused⏸", description="You cannot use this command when the server is paused", color=0xffff00)
                                        await message.channel.send(embed=command_embed, reference=message)
                                        command_embed = None
                                else:
                                    command_embed=discord.Embed(title=config["botprefix"]+"kick command", description="Kicks a player off the server", color=0xffff00)
                                    command_embed.set_author(name=botname, url="https://ms.srb2.org", icon_url=botavatar)
                                    command_embed.add_field(name="Kick using a player's node", value=config["botprefix"]+"kick 01", inline=False)
                                    command_embed.add_field(name="Kick using a player's name", value=config["botprefix"]+"kick sonic", inline=False)
                                    command_embed.add_field(name="Kick a player's name with reason", value=config["botprefix"]+"kick \"Sonic The Hedgehog\" \"annoying me\"", inline=False)
                                    await message.channel.send(embed=command_embed, reference=message)
                                    command_embed = None


                            if message.content.startswith(config["botprefix"]+"ban"):
                                if message.content != config["botprefix"]+"ban" and message.content != config["botprefix"]+"ban " and message.content.startswith(config["botprefix"]+"ban "):
                                    if gamepaused == False and server_isplaying == True:
                                        content = ('{0.content}\n'.format(message))
                                        #Format the message
                                        spacefind = content.find(" ")
                                        content = (content.translate({ord('\n'): ' '}))
                                        content = (content.translate({ord('\"'): 'а'}))
                                        content = (content.translate({ord('\''): 'б'}))
                                        content = content[spacefind+1:]
                                        content = (reg.sub('', content))
                                        content = (content.translate({ord('а'): '\"'}))
                                        content = (content.translate({ord('б'): '\''}))
                                        #Open a file and write message
                                        dcon = open('luafiles/client/DiscordBot/console.txt', 'a')
                                        dcon.write("ban "+content+'\n')
                                        dcon.close
                                        await message.add_reaction("✅")
                                    elif server_isplaying == False:
                                        await message.add_reaction("❌")
                                    elif gamepaused == True:
                                        command_embed=discord.Embed(title="⏸Game is Paused⏸", description="You cannot use this command when the server is paused", color=0xffff00)
                                        await message.channel.send(embed=command_embed, reference=message)
                                        command_embed = None
                                else:
                                    command_embed=discord.Embed(title=config["botprefix"]+"ban command", description="Bans a player on the server", color=0xffff00)
                                    command_embed.set_author(name=botname, url="https://ms.srb2.org", icon_url=botavatar)
                                    command_embed.add_field(name="Ban using a player's node", value=config["botprefix"]+"ban 01", inline=False)
                                    command_embed.add_field(name="Ban using a player's name", value=config["botprefix"]+"ban sonic", inline=False)
                                    command_embed.add_field(name="Ban a player's name with reason", value=config["botprefix"]+"ban \"Sonic The Hedgehog\" \"annoying me\"", inline=False)
                                    await message.channel.send(embed=command_embed, reference=message)
                                    command_embed = None


                            if message.content.startswith(config["botprefix"]+"map"):
                                if message.content != config["botprefix"]+"map" and message.content != config["botprefix"]+"map " and message.content.startswith(config["botprefix"]+"map "):
                                    if gamepaused == False and server_isplaying == True:
                                        content = ('{0.content}\n'.format(message))
                                        #Format the message
                                        spacefind = content.find(" ")
                                        content = (content.translate({ord('\n'): ' '}))
                                        content = (content.translate({ord('\"'): 'а'}))
                                        content = (content.translate({ord('\''): 'б'}))
                                        content = content[spacefind+1:]
                                        content = (reg.sub('', content))
                                        content = (content.translate({ord('а'): '\"'}))
                                        content = (content.translate({ord('б'): '\''}))
                                        #Open a file and write message
                                        dcon = open('luafiles/client/DiscordBot/console.txt', 'a')
                                        dcon.write("map "+content+'\n')
                                        dcon.close
                                        await message.add_reaction("✅")
                                    elif server_isplaying == False:
                                        await message.add_reaction("❌")
                                    elif gamepaused == True:
                                        command_embed=discord.Embed(title="⏸Game is Paused⏸", description="You cannot use this command when the server is paused", color=0xffff00)
                                        await message.channel.send(embed=command_embed, reference=message)
                                        command_embed = None
                                else:
                                    command_embed=discord.Embed(title=config["botprefix"]+"map command", description="Changes the map on the server", color=0xffff00)
                                    command_embed.set_author(name=botname, url="https://ms.srb2.org", icon_url=botavatar)
                                    command_embed.add_field(name="Change using a map number", value=config["botprefix"]+"map a0\n"+config["botprefix"]+"map 100", inline=False)
                                    command_embed.add_field(name="Change using a map keyword", value=config["botprefix"]+"map thz1", inline=False)
                                    await message.channel.send(embed=command_embed, reference=message)
                                    command_embed = None


                            if message.content.startswith(config["botprefix"]+"csay"):
                                if message.content != config["botprefix"]+"csay" and message.content != config["botprefix"]+"csay " and message.content.startswith(config["botprefix"]+"csay "):
                                    if gamepaused == False and server_isplaying == True:
                                        content = ('{0.content}\n'.format(message))
                                        #Format the message
                                        spacefind = content.find(" ")
                                        content = (content.translate({ord('\n'): ' '}))
                                        content = (content.translate({ord('\"'): 'а'}))
                                        content = (content.translate({ord('\''): 'б'}))
                                        content = content[spacefind+1:]
                                        content = (reg.sub('', content))
                                        content = (content.translate({ord('а'): '\"'}))
                                        content = (content.translate({ord('б'): '\''}))
                                        #Open a file and write message
                                        dcon = open('luafiles/client/DiscordBot/console.txt', 'a')
                                        dcon.write("csay "+content+'\n')
                                        dcon.close
                                        '''
                                        try:
                                            await self.get_channel(config["post_id"]).send("CSAY: "+content)
                                        except AttributeError:
                                            messagebox.showerror("Error: Improper Message Channel ID has been passed.", "Check the channel ID, change it in the discordbot.json file.")
                                            exit()
                                        '''
                                        await message.add_reaction("✅")
                                    elif server_isplaying == False:
                                        await message.add_reaction("❌")
                                    elif gamepaused == True:
                                        command_embed=discord.Embed(title="⏸Game is Paused⏸", description="You cannot use this command when the server is paused", color=0xffff00)
                                        await message.channel.send(embed=command_embed, reference=message)
                                        command_embed = None
                                else:
                                    command_embed=discord.Embed(title=config["botprefix"]+"csay command", description="Sends a message to everyone within a netgame which is displayed in the center of the screen", color=0xffff00)
                                    command_embed.set_author(name=botname, url="https://ms.srb2.org", icon_url=botavatar)
                                    command_embed.add_field(name="Send csay message", value=config["botprefix"]+"csay Ball mania is real!", inline=False)
                                    await message.channel.send(embed=command_embed, reference=message)
                                    command_embed = None

                                    
                            if message.content.startswith(config["botprefix"]+"exitlevel"):
                                if gamepaused == False and server_isplaying == True:
                                    #Open a file and write message
                                    dcon = open('luafiles/client/DiscordBot/console.txt', 'a')
                                    dcon.write("exitlevel\n")
                                    dcon.close
                                    await message.add_reaction("✅")
                                elif server_isplaying == False:
                                    await message.add_reaction("❌")
                                elif gamepaused == True:
                                    command_embed=discord.Embed(title="⏸Game is Paused⏸", description="You cannot use this command when the server is paused", color=0xffff00)
                                    await message.channel.send(embed=command_embed, reference=message)
                                    command_embed = None

                                    
                            if message.content.startswith(config["botprefix"]+"restart") and not message.content.startswith(config["botprefix"]+"restartbot"):
                                    #if server_isplaying == True:
                                    '''
                                    command_embed=discord.Embed(title="✅SUCCESS!✅", description="Server is restarting...", color=0x00ff00)
                                    await message.channel.send(embed=command_embed, reference=message)
                                    command_embed = None
                                    '''
                                    await message.add_reaction("✅")
                                    await client.get_channel(config["post_id"]).send("❌`Server has shutdown`❌")
                                    await client.change_presence(status=discord.Status.dnd,activity=discord.Game("Restarting server..."))
                                    restartserver()

                        
                        elif not message.content.startswith(config["botprefix"]+"help") and message.content != config["botprefix"] and message.content != config["botprefix"]+" ":
                            command_embed=discord.Embed(title="⚠PermissionError⚠", description="You don't have permission to use this command", color=0xff0000)
                            await message.channel.send(embed=command_embed, reference=message)
                            command_embed = None
                        discordconsole = Fore.MAGENTA + Style.DIM +  'Discord command: ' + Style.RESET_ALL + '<{0.author.display_name}#{0.author.discriminator}> {0.content}'.format(message)
                        discordconsole = (discordconsole.translate({ord('\n'): ' '}))
                        print("[" + now.strftime("%H:%M") + "]" + discordconsole)
                        mcon_file = open(mlogpath, "a")
                        mcon_file.write("[" + now.strftime("%Y-%m-%d %H:%M:%S") + "]Discord command: <{0.author.display_name}#{0.author.discriminator}> {0.content}".format(message) + "\n")
                        mcon_file.close()
        except PermissionError:
            if config["debug"] == True:
                print("[" + now.strftime("%H:%M") + "]" + Fore.RED + 'Error:' + Style.RESET_ALL + ' unable to edit console.txt file because it is busy.')
        except discord.errors.Forbidden:
            messagebox.showerror("Error: Missing Permissions", "No access to the channel, give access to read and send messages and reactions for bot.")
                        

#intents = discord.Intents.default()
#intents.members = True
#Bot launch
#client = MyClient(intents=intents) discord.errors.PrivilegedIntentsRequired:
if isdiscordborwork == False:
    isdiscordborwork = True
    client = MyClient()
    try:
        #Get a token and connect to the bot
        print("Connecting to a discord bot...")
        client.run(config["token"])
        #If the token is not correct, display an error window and close the program
    except discord.errors.LoginFailure:
         messagebox.showerror("Error: Improper token has been passed.", "Get a new token and replace it in the discordbot.json file.")
         exit()
else:
    now = datetime.datetime.now()
    if config["debug"] == True:
        print("[" + now.strftime("%H:%M") + "]" + Fore.RED + 'Error:' + Style.RESET_ALL + ' program tries to start bot again')

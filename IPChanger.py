# IPChanger.py
# https://github.com/hevnsnt/IPChanger
# Released under GPL 3.0
import requests
import sys, os, socket
from time import sleep
from stem import Signal
from stem.control import Controller
from fake_useragent import UserAgent
from colorama import Fore, Back, Style, init
from random import randint, shuffle
from bs4 import BeautifulSoup
from signal import signal, SIGINT
import csv
import subprocess
import time
import getopt


###########################Basic Setup########################################
proxies = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
} # This is for the local TOR proxy
IPCheckURL = 'https://ifconfig.co' # URL to determine IP address
headers = { 'User-Agent': UserAgent().random }
torpassword = ""
###############################################################################

def banner():
	os.system('clear')
	data = '''


      ::::::::::: :::::::::           
         :+:     :+:    :+:        
        +:+     +:+    +:+        
       +#+     +#++:++#+         
      +#+     +#+               
     #+#     #+#               
########### ###                 
         ::::::::  :::    :::     :::     ::::    :::  ::::::::  :::::::::: :::::::::
       :+:    :+: :+:    :+:   :+: :+:   :+:+:   :+: :+:    :+: :+:        :+:    :+: 
      +:+        +:+    +:+  +:+   +:+  :+:+:+  +:+ +:+        +:+        +:+    +:+  
     +#+        +#++:++#++ +#++:++#++: +#+ +:+ +#+ :#:        +#++:++#   +#++:++#:  
    +#+        +#+    +#+ +#+     +#+ +#+  +#+#+# +#+   +#+# +#+        +#+    +#+  
   #+#    #+# #+#    #+# #+#     #+# #+#   #+#+# #+#    #+# #+#        #+#    #+# 
   ########  ###    ### ###     ### ###    ####  ########  ########## ###    ###          
                                                        ...use it for things...
'''
	print(data)


def validateEnv():
	#Lets make sure everything is safe before we start
	if sys.platform != 'linux':
		print('  [' + Fore.RED + '!' + Style.RESET_ALL + '] This script requires Linux')
		sys.exit(0)
	else:
		print(f'  [' + Fore.GREEN +'+' + Style.RESET_ALL + ']  OS Check:' + Fore.GREEN + f' {sys.platform}' + Style.RESET_ALL)
	try:
		doIPAddressStuff()
		print('  [' + Fore.GREEN +'+' + Style.RESET_ALL + '] TOR Proxy: ' + Fore.GREEN + 'Responding' + Style.RESET_ALL)
	except:
		sys.exit(0)


def doIPAddressStuff():
	# This connects to the local TOR proxy and requests a new TOR exit node
	# It only makes the request, often you will get the same exit node returned
	# as TOR assigns node based on "best" route
	try:
		with Controller.from_port(port = 9051) as c:
			c.authenticate(password = torpassword)
			c.signal(Signal.NEWNYM)
	except:
		print('  [' + Fore.RED + '!' + Style.RESET_ALL + '] Local TOR proxy not responding')
		print('  [+] See READ.ME for TOR Proxy Configuration Instructions')
		sys.exit(0)


def getNewIP():
	# This uses the 'IPCheckURL' to determine what our current IP address is
	# and then uses the getNewIP() function to get a new one
	headers = { 'User-Agent': UserAgent().random }
	count = 1
	while True:
		try:
			currentIP = requests.get(IPCheckURL, proxies=proxies, headers=headers, timeout=3).text
			oldIPaddy = currentIP
			while currentIP == oldIPaddy:
				print('\r  [' + Fore.GREEN +'+' + Style.RESET_ALL + f'] [Getting new IP: {count}]', end ='')
				count = count + 1
				doIPAddressStuff()
				currentIP = requests.get(IPCheckURL, proxies=proxies, headers=headers, timeout=3).text
			print(Style.BRIGHT + Fore.BLACK + f'\n  [+] Obtained new IP Address: {currentIP}' + Style.RESET_ALL)
		except KeyboardInterrupt:
			sys.exit(0)
		except:
			print('\r  [' + Fore.RED + '!' + Style.RESET_ALL + f'] Connection Error to {IPCheckURL}, retrying', end='')
			sleep(3)
			continue #quality code right here
		break
	return oldIPaddy, currentIP

def handler(signal_received, frame):
    # Catches CTRL-C  // Handle any cleanup here
	print('\n  [!] CTRL-C detected. Exiting gracefully\n')
	sys.exit(0)



if __name__ == "__main__":
	signal(SIGINT, handler)
	banner()
	validateEnv() # Make sure we have correct environment
	oldip, newip = getNewIP()
	print(f'\nOld IPaddress: {oldip}  || New Ipaddress: {newip}')
	
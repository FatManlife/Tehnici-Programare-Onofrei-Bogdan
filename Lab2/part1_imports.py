import requests
import time
#from requests import get
#import requests as rq
import urllib.request
# Laborator: funcții, metode și importuri pe web
# Student: <Onofrei Bogdan>
 
BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

#Ex1
#requests a avut nevoie de install iar urllib nu deoarece urllib se afala  in librarie care vin odata cu instalarea python default 
#print(requests.__version__)

#Ex2
#req = requests.get(BASE_URL timeout=TIMEOUT)
#req = get(BASE_URL)
#cand ai nevoie doar de o functie din librarie si nu vrei sa consumi spatiu e mai bine sa utilizezi from import dar daca ai nevoie mai mult de o librarie atunci faci simplu imoprt totodata facand asta elimini posibilitatea de a aparea conflicte de nume
#print(req))

#Ex3
#print(rq.get(BASE_URL, timeout=TIMEOUT))
#alisal il face mai suor de citit cand utilizezi abrevieri de 2+ litere dar mai greu daca scrii o litera sau cuvinte fara sens nerelatate librariei

#Ex4
# with urllib.request.urlopen(BASE_URL, timeout=TIMEOUT) as response:
#     print(response.status)
#     body = response.read()
#     print(body)

#Ex5
#print(dir(requests))  
# '__license__', '__loader__', '__name__', - toate sunt metadata

#Ex6
#print(help(requests.get))
#print(requests.get(BASE_URL, timeout=TIMEOUT))

#Ex 7
# start = time.perf_counter()
# response = requests.get(BASE_URL, timeout=TIMEOUT)
# end = time.perf_counter()
# print(f"{end-start:.6f}")
# print(response.elapsed)

#Ex8
# try:
#     import bs4
#     print("Modul instalat")
# except ImportError:
#     print("Instalați modulul cu: pip install beautifulsoup4")

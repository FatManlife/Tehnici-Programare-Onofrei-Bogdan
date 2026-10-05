import time
import json
import re
import urllib
import math
import ssl
import socket
import csv
import requests as rq
from bs4 import BeautifulSoup

DEFAULT_HEADERS = {"User-Agent": "WebLab-<numele vostru>"}

#Ex44
def fetch(url:str, timeout:int=10):
    """Trimite o cerere HTTP către URL-ul specificat și returnează răspunsul."""
    return rq.get(url, timeout=timeout,headers=DEFAULT_HEADERS)

def get_status(base_url, url:str, timeout) -> int:
    """Returnează codul de stare HTTP pentru URL-ul specificat."""
    time.sleep(1)
    res = rq.get(base_url + url, timeout=timeout) 
    return res.status_code

def get_title(html:str) -> str:
    """Extrage titlu din html text."""
    return html[html.find("<title>") + len("<title>") : html.find("</title>")].strip() 

def security_headers(url:str, timeout=10):
    """Verifică prezența headerelor HTTP de securitate și returnează rezultatele."""
    res = rq.get(url, timeout=timeout)
    d = {
        "Strict-Transport-Security" : True if res.headers.get("Strict-Transport-Security") else False,
        "Content-Security-Policy" : True if res.headers.get("Content-Security-Policy") else False,
        "X-Frame-Options" : True if res.headers.get("X-Frame-Options") else False,
        "X-Content-Type-Options" : True if res.headers.get("X-Content-Type-Options") else False,
        "Referrer-Policy" : True if res.headers.get("Referrer-Policy") else False
    }

    return d

#Ex49
def check_paths(base:str, paths: list[str], timeout = 10):
    """Verifică codul de stare și timpul de răspuns pentru fiecare cale specificată."""
    l = []

    for path in paths:
        l1 = []
        res = rq.get(base + path, timeout=timeout)
        l1.append(path) 
        l1.append(res.status_code)
        l1.append(res.elapsed.total_seconds())
        l.append(l1)

    return l 

def create_csv(base:str, path: list[str]):
   """Creează un fișier CSV cu informații despre căile verificate."""
   l = [["path"],["status"],["checked_at"]]
   for val in check_paths(base,path):
        l.append(val)

   with open("report.csv", "w") as file:
       writer = csv.writer(file)
       writer.writerows(l)

def resolve(hostname):
    """Rezolvă un nume de domeniu și returnează adresa sa IP."""
    return socket.gethostbyname(hostname)


#EX46-deoarece can interpretorul interpreteaza aceasta linie el verifica mai intai unde se afla(anume in cazul acesta el verifica daca se afla in modul) si ruleaza programul in dependenta de asta
if __name__ == "__main__":
    print("Autotest:", get_status("https://cybercor.org", "", 10))

def score_headers(results: dict):
    """Calculează și returnează scorul headerelor de securitate."""
    ctr = 0
    for _, val in results.items():
        if val: 
            ctr +=1
    return f"{ctr}/{len(results)}"

def cert_days_left(hostname):
    """Calculează și returnează numărul de zile rămase până la expirarea certificatului SSL."""
    context = ssl.create_default_context()
    sock = socket.create_connection((hostname, 443))
    sock = context.wrap_socket(sock, server_hostname=hostname)
    cert = sock.getpeercert()
    expiry = cert["notAfter"]
    seconds = ssl.cert_time_to_seconds(expiry)
    return str(math.ceil(seconds/86400)) + " de zile rămase"


def split_links(res, url):
    """Separă legăturile unei pagini în legături interne și externe."""
    domain = urllib.parse.urlparse(url).hostname

    links = re.findall(r'<a[^>]+href=["\']([^"\']+)["\']', res.text, re.I)

    internal = []
    external = []

    for link in links:
        full_link = urllib.parse.urljoin(url, link)
        hostname = urllib.parse.urlparse(full_link).hostname

        if hostname == domain:
            internal.append(full_link)
        else:
            external.append(full_link)

    return internal, external

def disallowed_paths(url):
    """Extrage și returnează căile interzise din fișierul robots.txt al unui site."""
    res = rq.get(url + "/robots.txt") 
    html  = res.text

    if html == None:
        return 

    paths = []

    for line in html.splitlines():
        if line.startswith("Dissalow:"):
            paths.append(line.split(":")[1])

    return paths

def get_redirects(response):
    """Extrage și returnează redirecționările efectuate de un răspuns HTTP."""
    redirects = []

    for r in response.history:
        redirects.append(f"{r.status_code} -> {r.headers["Location"]}")

    return redirects
    

#Ex50
def site_report(url):
    """Generează și salvează un raport JSON cu informații despre site-ul specificat."""
    res = fetch(url)

    internal, external = split_links(res, url)

    lie = [internal, external]

    dict = {
        "Cod de stare": res.status_code,
        "Titlu": get_title(res.text),
        "Adresă IP": resolve("cybercor.org"),
        "Redirecționări": get_redirects(res),
        "Scor securitate": score_headers(security_headers(url)),
        "Certificat": cert_days_left("cybercor.org"),
        "Legături": lie,
        "Căi interzise": disallowed_paths(url),
    }


    with open("report.json", "w") as file:
        file.write("=== Raport site: https://cybercor.org ===\n")
        json.dump(dict, file, indent=4) 
        file.write("\nSalvat în report.json")

    print(dict)

#bonus
def get_title_bs(url) -> str:
    """Extrage titlu din html text."""
    res = rq.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    return (soup.find("title").text)

def extract_links(url):
    """Extrage și returnează legăturile dintr-o pagină HTML folosind BeautifulSoup."""
    res = rq.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    links = soup.find_all(href=True)

    new_links = []

    for link in links:
       new_links.append(link.get("href"))
    
    return new_links




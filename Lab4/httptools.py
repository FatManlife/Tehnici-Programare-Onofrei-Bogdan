import requests
BASE = "https://httpbin.org"
PATHS = ["/get", "/redirect/2", "/delay/1", "/status/404", "/delay/5"]

# Partea 1: parametri în URL
def search(params):
    """GET pe /get cu parametri în URL; returnează parametrii primiți de
    server."""
    r = requests.get("https://httpbin.org/get", params=params)
    print(r.json()["args"]) # {'q': 'python', 'page': '2'
    

def search_url(params):
    # Exercițiu de pregătire: Trusa de unelte HTTP
    # Page 1 of 11
    """Returnează adresa completă construită de requests, cu tot cu
    parametri."""
    r = requests.get("https://httpbin.org/get", params={"q": "python", "page":
    "2"})
    print(r.url) # https://httpbin.org/get?q=python&page=2


# Partea 2: anteturi
def fetch_with_agent(agent):
    """GET pe /headers cu User-Agent=agent; returnează User-Agent-ul văzut de
    server."""
    r = requests.get("https://httpbin.org/headers", headers={"User-Agent": agent})
    print(r.json()["headers"]["User-Agent"]) # MyBot/1.


def default_agent():
    """Returnează User-Agent-ul trimis de requests când nu setezi nimic."""
    r = requests.get("https://httpbin.org/headers")
    print(r.json()["headers"]["User-Agent"]) # MyBot/1.


# Partea 3: trimiterea datelor
def post_json(data):
    """POST cu datele ca JSON pe /post; returnează JSON-ul primit de
    server."""
    r = requests.post("https://httpbin.org/post", json=data)
    print(r.json()["json"]) # {'name': 'Ana'}


def post_form(data):
    r = requests.post("https://httpbin.org/post", data=data)
    print(r.json()["form"])
    """POST cu datele ca formular pe /post; returnează formularul primit de
    server."""


# Partea 4: coduri de stare
def describe_status(code):
    """GET pe /status/<code>; returnează 'succes', 'eroare client' sau
    'eroare server'."""
    r = requests.get(f"https://httpbin.org/status/{code}")
    try:
        r.raise_for_status() 
        print(r.status_code, "succes") # 404
    except requests.HTTPError as e:
        if r.status_code in range (400,500):
            print("eroare client:", e)
        elif r.status_code in range (500,600): 
            print("eroare server:", e)
        else:
            print("a eșuat:", e)


def is_ok(code):
    """GET pe /status/<code>; returnează True dacă cererea a reușit, altfel
    False."""
    r = requests.get(f"https://httpbin.org/status/{code}")
    try:
        r.raise_for_status() 
        return True
    except requests.HTTPError as e:
        return False


# Partea 5: redirecționări
def count_redirects(n):
    """GET pe /redirect/<n>; returnează câte redirecționări au fost
    Exercițiu de pregătire: Trusa de unelte HTTP
    Page 2 of 11
    urmate."""
    r = requests.get(f"https://httpbin.org/redirect/{n}")
    print(len(r.history)) 


def final_url(n):
    """GET pe /redirect/<n>; returnează adresa la care ai ajuns."""
    r = requests.get(f"https://httpbin.org/redirect/{n}")
    print(r.status_code) # 302
    print(r.url) # 302


def first_hop(n):
    """GET pe /redirect/<n> FĂRĂ a urma redirecționarea; returnează antetul
    Location."""

    r = requests.get(f"https://httpbin.org/redirect/{n}", allow_redirects=False)
    print(r.status_code) # 302
    print(r.headers["location"]) # unde voia serverul să te trimită


# Partea 6: sesiuni și cookie-uri
def cookie_demo(name, value):
    """Setează un cookie, apoi citește cookie-urile înapoi folosind O SINGURĂ
    sesiune."""
    s = requests.Session()
    s.get(f"https://httpbin.org/cookies/set?{name}={value}")
    r = s.get("https://httpbin.org/cookies")
    print(r.json()["cookies"]) # {'theme': 'dark'}


#?
def no_session_demo(name, value):
    """Fă același lucru cu apeluri simple requests.get; returnează cookie-
    urile văzute de server."""
    r = requests.get(f"https://httpbin.org/cookies/set?{name}={value}")
    print(r.json()["cookies"]) # {'theme': 'dark'}
    r = requests.get(f"https://httpbin.org/cookies/set?{name}s={value}s")
    print(r.json()["cookies"]) # {'theme': 'dark'}

# Partea 7: raportul final

def report(path):
    """Returnează un dicționar care descrie pagina de la BASE + path."""
    d = {}

    try:
        r = requests.get(BASE + path, timeout=3)
        r.raise_for_status
        d = { "status": r.status_code,
        "final_url": r.url,
        "redirects": len(r.history),
        "seconds": r.elapsed,
        "content_type": "application/json",
        }

    except:
        d = {
            "status": None,
            "error": "Eroare de cod, url sau timeout"
        }
    return d

def main():
    l = []
    ctr_f = 0

    for path in PATHS:
        d = report(path)
        if d["status"] == 200:
            l.append(d)
        else:
            ctr_f += 1

    print([path['final_url'] for path in l])


    print("Failed: " + str(ctr_f) + "\n" + "Succeded: " + str(len(l)))

# Bonus: autentificare
def check_login(user, password):
    """Returnează True dacă serverul acceptă datele de autentificare, altfel
    False."""
    r = requests.get("https://httpbin.org/basic-auth/admin/secret", auth=(user, password))

    if r.status_code == 200:
        return True

    return False

    # Exercițiu de pregătire: Trusa de unelte HTTP
    # Page 3 of 11

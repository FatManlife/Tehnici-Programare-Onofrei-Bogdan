import requests
BASE = "https://httpbin.org"
PATHS = ["/get", "/redirect/2", "/delay/1", "/status/404", "/delay/5"]

# Partea 1: parametri în URL
def search(params):
    """GET pe /get cu parametri în URL; returnează parametrii primiți de
    server."""
    r = requests.get("https://httpbin.org/get", params=params)
    print(r.json()["args"]) # {'q': 'python', 'page': '2'
    
search({'q':'python', 'page':'2'})

def search_url(params):
    # Exercițiu de pregătire: Trusa de unelte HTTP
    # Page 1 of 11
    """Returnează adresa completă construită de requests, cu tot cu
    parametri."""
    r = requests.get("https://httpbin.org/get", params={"q": "python", "page":
    "2"})
    print(r.url) # https://httpbin.org/get?q=python&page=2

search_url({'q':'python', 'page':'2'})

# Partea 2: anteturi
def fetch_with_agent(agent):
    """GET pe /headers cu User-Agent=agent; returnează User-Agent-ul văzut de
    server."""
    r = requests.get("https://httpbin.org/headers", headers={"User-Agent": agent})
    print(r.json()["headers"]["User-Agent"]) # MyBot/1.

fetch_with_agent("agent")

def default_agent():
    """Returnează User-Agent-ul trimis de requests când nu setezi nimic."""
    r = requests.get("https://httpbin.org/headers")
    print(r.json()["headers"]["User-Agent"]) # MyBot/1.

default_agent()

# Partea 3: trimiterea datelor
def post_json(data):
    """POST cu datele ca JSON pe /post; returnează JSON-ul primit de
    server."""
    r = requests.post("https://httpbin.org/post", json=data)
    print(r.json()["json"]) # {'name': 'Ana'}

post_json("Ana")

def post_form(data):
    r = requests.post("https://httpbin.org/post", data=data)
    print(r.json()["form"])
    """POST cu datele ca formular pe /post; returnează formularul primit de
    server."""

post_json("Ana")

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

describe_status(503)

def is_ok(code):
    """GET pe /status/<code>; returnează True dacă cererea a reușit, altfel
    False."""
    r = requests.get(f"https://httpbin.org/status/{code}")
    try:
        r.raise_for_status() 
        return True
    except requests.HTTPError as e:
        return False

print(is_ok(209))

# Partea 5: redirecționări
def count_redirects(n):
    """GET pe /redirect/<n>; returnează câte redirecționări au fost
    Exercițiu de pregătire: Trusa de unelte HTTP
    Page 2 of 11
    urmate."""
    r = requests.get(f"https://httpbin.org/redirect/{n}")
    print(len(r.history)) 

count_redirects(5)

def final_url(n):
    """GET pe /redirect/<n>; returnează adresa la care ai ajuns."""
    r = requests.get(f"https://httpbin.org/redirect/{n}")
    print(r.status_code) # 302
    print(r.url) # 302

final_url(4)

def first_hop(n):
    """GET pe /redirect/<n> FĂRĂ a urma redirecționarea; returnează antetul
    Location."""

    r = requests.get(f"https://httpbin.org/redirect/{n}", allow_redirects=False)
    print(r.status_code) # 302
    print(r.headers["location"]) # unde voia serverul să te trimită

first_hop(4)

# Partea 6: sesiuni și cookie-uri
def cookie_demo(name, value):
    """Setează un cookie, apoi citește cookie-urile înapoi folosind O SINGURĂ
    sesiune."""
    s = requests.Session()
    s.get(f"https://httpbin.org/cookies/set?{name}={value}")
    r = s.get("https://httpbin.org/cookies")
    print(r.json()["cookies"]) # {'theme': 'dark'}

cookie_demo("theme", "dark")

#?
def no_session_demo(name, value):
    """Fă același lucru cu apeluri simple requests.get; returnează cookie-
    urile văzute de server."""
    s = requests.Session()
    s.get(f"https://httpbin.org/cookies/set?{name}={value}")
    s.get(f"https://httpbin.org/cookies/set?{name}s={value}s")
    r = s.get("https://httpbin.org/cookies")
    print(r.json()["cookies"]) # {'theme': 'dark'}

cookie_demo("theme", "dark")
# Partea 7: raportul final

def report(path):
    """Returnează un dicționar care descrie pagina de la BASE + path."""
    r = requests.get(BASE + path, timeout=3)

    d = {
        "status": describe_status(r.status_code) if is_ok else f"{None}, {describe_status(r.status_code)}",
        "final_url": final_url(r.url),
        "redirects": r.url,
        "seconds": r.elapsed,
        "content_type": "application/json",
    }

    return d

def main():
    # l = []
    # ctr_f = 0

    # for path in PATHS:
    #     d = report(path)
    #     if d["status"] == 200:
    #         l.append(path)
    #     else:
    #         ctr_f += 1

    # print(sorted(l, key=lambda x: x["seconds"]))


    # print("Failed: " + ctr_f + "\n" + "Succeded: " + len(l))
    pass

# Bonus: autentificare
def check_login(user, password):
    """Returnează True dacă serverul acceptă datele de autentificare, altfel
    False."""
    pass
    # Exercițiu de pregătire: Trusa de unelte HTTP
    # Page 3 of 11
if __name__ == "__main__":
    print("\n\n")
    main()
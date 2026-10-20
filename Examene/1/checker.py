import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    url = (host +  (path if path[0] == "/" else f"/{path}") )
    return url

def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    if "https" == url[:5]:
        return True

    return False

def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    r = requests.get(url)
    print(f"Status: {r.status_code}")
    print(f"Content-Type: {r.headers["Content-Type"]}")

def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    d = {}

    try:

        r = requests.get(url, timeout=5)
        r.raise_for_status()
        d = {
            "status" : r.status_code,
            "content_type" : r.headers["Content-Type"],
            "length": len(r.content),
            "server": r.headers["Server"] if r.headers["Server"] else "Unknown"
        }
    except:
        d = {
            "status" : None,
            "error": "Erorare de url sau tiemout"
        }
    
    return d


def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    l = []
    ctr = 0;

    for site in SITES:
        d = check_site(site)
        d["url"] = site
        if d["status"] == 200:
            l.append(d)
        else:
            ctr += 1

    sorted(l, key=lambda x: x["length"])

    for site in l:
        print(f"{site["url"]} -> {site["status"]}, {site["length"]} octeti")

    print(f"Reusite: {len(l)} | Esuate: {ctr}")


def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    d = {
        "present":[],
        "missing":[],
        "score": 0, 
    }

    try:
        r = requests.get(url, timeout=5)

        headers = r.headers

        if "Strict-Transport-Security" in headers:
            d["present"].append("Strict-Transport-Security")
        else:
            d["missing"].append("Strict-Transport-Security")

        if "Content-Security-Policy" in headers:
            d["present"].append("Content-Security-Policy")
        else:
            d["missing"].append("Content-Security-Policy")

        if "X-Frame-Options" in headers:
            d["present"].append("X-Frame-Options")
        else:
            d["missing"].append("X-Frame-Options")

        if "X-Content-Type-Options" in headers:
            d["present"].append("X-Content-Type-Options")
        else:
            d["missing"].append("X-Content-Type-Options")

        d["score"] = len(d["present"]) / 4 * 100
    except:

     d = {
            "status" : None,
            "error": "Erorare de url sau tiemout"
        }
    
    return d; 


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    for attempt in range(attempts):
        try:
            r = requests.get(url, timeout=5)
            r.raise_for_status()
            return {"attempt": attempt}
        except requests.HTTPError as re :
            return {"status": None, "error": "depasit limita de incercari", attempts: attempts}         
        except :
            pass

    return {"status": None, "error": "depasit limita de incercari", attempts: attempts} 


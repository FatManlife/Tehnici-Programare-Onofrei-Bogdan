import httptools as h
from httptools import BASE
from httptools import PATHS

if __name__ == "__main__":
    h.search({'q': 'python', 'page': '2'})
    h.search_url({'q':'python', 'page':'2'})
    h.fetch_with_agent("MyBot/1.0")
    h.default_agent()
    h.post_json({"name": "Ana", "age": 19,"tags": ["a", "b"]})
    h.post_form({"user": "ana", "city":"Bălți"})
    h.describe_status(200)
    h.describe_status(404)
    h.describe_status(503)
    h.is_ok(204)
    h.is_ok(500) 
    h.count_redirects(3)
    h.final_url(2)
    h.first_hop(3)
    h.cookie_demo("theme", "dark")
    h.no_session_demo("theme", "dark")
    print(h.report("/get"))
    print(h.report("/redirect/2"))
    print(h.report("/delay/1"))
    print(h.report("/delay/5"))
    print(h.check_login("admin", "secret"))
    print(h.check_login("admin", "gresit"))

    h.main()
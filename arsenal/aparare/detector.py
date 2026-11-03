from collections import Counter
import argparse, json
from .parse_auth import citeste_esecuri
 
def suspecti(counts, prag=10):
    if prag < 1:
        raise ValueError(f"prag invalid: {prag} (cel putin 1)")
    # TODO: intoarce lista de (ip, n) cu n >= prag,
    #       sortata descrescator dupa n
    return [(ip, n) for ip,n  in counts.most_common() if n >= prag]
 
c = Counter({"203.0.113.9": 13, "198.51.100.7": 2})

def main():
    p = argparse.ArgumentParser()
    p.add_argument("log")
    p.add_argument("--prag", type=int, default=10)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    esecuri = citeste_esecuri(a.log)
    counts = Counter(e["ip"] for e in esecuri)
    sus = suspecti(counts, a.prag)

    # TODO: cu --json, scoate json.dumps cu {esecuri, pe_ip, suspecti};
    #       fara, un rezumat cu "BRUTE FORCE" pe fiecare suspect
    ...

    ctr = 0 

    for ip,n in counts.most_common():
        ctr += n

    if not a.json:
        print(f"Esecuri de autentificare {ctr}")
        for ip, n in counts.most_common():
            print(f" {ip}: {n}")
        print(f"Suspecti (prga{a.prag}):")
        print(f"{sus[0][0]} ({sus[0][1]} incercari) BRUTE FORCE:")

    else:
        with open("raport.json", "w") as f:
            json.dump({"esecuri": counts, "pe_ip": ctr, "suspecti": sus},f)

if __name__ == '__main__':
    # print(suspecti(c))
    # print(suspecti(c, prag=2))

    main()
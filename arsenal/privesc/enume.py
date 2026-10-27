import argparse, json, os 

#A1
def citeste_linii(cale):
    with open(cale, encoding="utf-8") as f:
        # TODO: intoarce lista liniilor .strip(), fara cele goale si fara cele cu #
        return list(set([line.strip() for line in f.readlines()]))
 
cai = citeste_linii("start/suid.txt")
# print("linii SUID:", len(cai))

#A2
def nume(cale):
    # TODO: intoarce ce e dupa ultimul "/"  (vezi rsplit)
    cai = cale.split("/")
    return cai[len(cai) - 1]
 
nume_unice = {nume(c) for c in cai}    # set comprehension
# print("SUID distincte:", len(nume_unice))

#A3
GTFO = {"find", "vim.basic", "vim", "nmap", "cp", "bash",
        "less", "awk", "python3", "perl"}
 
def suid_constatari(cale):
    cai = citeste_linii(cale)
    # TODO: pentru fiecare cale UNICA, in ordine sortata, un dict:
    #   {"cale": c, "nume": nume(c),
    #    "risc": "mare" daca nume(c) in GTFO, altfel "normal"}

    cai = list(set(cai))

    l = []

    for c in cai:
        l.append(
            {
                "cale": c,
                "nume": nume(c),
                "risc": "mare" if nume(c) in GTFO else "normal"
            }
        )

    return l

 
suid = suid_constatari("start/suid.txt")
mari = [c for c in suid if c["risc"] == "mare"]
# print(len(suid), "SUID,", len(mari), "cu risc mare")
# print(sorted(c["nume"] for c in mari))

#A4
def sudo_constatari(cale):
    out = []
    for ln in citeste_linii(cale):
        user, drept = ln.split(" : ", 1)   # despachetare in tuplu
        # TODO: adauga {"user": user.strip(), "drept": drept.strip(),
        #   "risc": "mare" daca "NOPASSWD" in drept, altfel "normal"}
        out.append(
            {
                "user": user.strip(),
                "drept": drept.strip(),
                "risc": "mare" if "NOPASSWD" in drept else "normal"
            }
        )

    return out
 
def cron_constatari(cale):
    # TODO: campuri = ln.split(); user = campuri[5];
    #   comanda = " ".join(campuri[6:]); dict cu user si comanda
    l = []
    for ln in citeste_linii(cale)[1:]:
        campuri = ln.split()

        l.append(
            { 
                "user": campuri[5],
                "comanda": " ".join(campuri[6:])
            }
        )
    return l

def enumereaza(d):
    return {
        "suid": suid_constatari(os.path.join(d, "suid.txt")),
        "sudo": sudo_constatari(os.path.join(d, "sudo.txt")),
        "cron": cron_constatari(os.path.join(d, "crontab.txt")),
    }
# print(enumereaza("start"))

#A5
def main():
    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    users = []
    raport = enumereaza(a.capturi)
    if a.json:
        print(json.dumps(raport, indent=2, ensure_ascii=False)); return
    for categorie, lista in raport.items():
        mari = [c for c in lista if c.get("risc") == "mare"]
        print(f"{categorie}: {len(lista)} gasite, {len(mari)} cu risc mare")
        # TODO: utilizatorii implicati = multimea userilor din sudo REUNITA cu cei din cron
        if categorie in "sudocron":
            for c in lista:
                users.append(c.get("user"))

    users = list(set(users))

    print("utilizatori implicati: ", end="")

    for user in users:
        print(user, end=", ")

    print()

    with open("enum.json", "w", encoding="utf-8") as f:
        json.dump(raport, f, indent=2, ensure_ascii=False)
    print("Raport salvat in enum.json")
 
if __name__ == "__main__":
    main()
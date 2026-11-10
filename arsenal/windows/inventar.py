from dataclasses import dataclass, asdict
import argparse
import json
from dataclasses import asdict

CAI_SUSPECTE = ("\\Temp\\", "\\Roaming\\")

@dataclass
class Proces:
    pid: int
    nume: str
    user: str
    cale: str

    def e_suspect(self):
        for cale_suspect in CAI_SUSPECTE:
            if cale_suspect in self.cale:
                return True
        return False
 
p = Proces(3120, "update.exe", "ana", r"C:\Users\ana\AppData\Local\Temp\update.exe")
# print(p.pid, p.nume)
# print(p)
# print(p.e_suspect())   

SUSPECTE_ID = {4625, 1102, 7045}
 
@dataclass
class Eveniment:
    id: int; nivel: str; sursa: str; cont: str; mesaj: str
    def e_suspect(self):
        # TODO: True daca self.id in SUSPECTE_ID SAU self.nivel == "critical"
        if self.id in SUSPECTE_ID or self.nivel == "critical":
            return True
        return False;

def procese_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        # TODO: intoarce [Proces(**d) for d in json.load(f)]
        return [Proces(**d) for d in json.load(f)]

 
procese = procese_din_json("arsenal/windows/start/procese.json")
# print("procese:", len(procese))
# print("suspecte:", sum(1 for p in procese if p.e_suspect()))


@dataclass
class Inventar:
    procese: list
    @classmethod
    def din_json(cls, cale):
        with open(cale, encoding="utf-8") as f:
            return cls([Proces(**d) for d in json.load(f)])
            # TODO: return cls([Proces(**d) for d in json.load(f)])
            ...
    def __len__(self):
        return len(self.procese)

    def suspecte(self):
        # TODO: lista proceselor cu p.e_suspect()
        return [p for p in self.procese if p.e_suspect()]

        ...
    def pe_user(self):
        # TODO: dict user -> lista de nume (foloseste setdefault)
        rezultat = {}

        for p in self.procese:
            rezultat.setdefault(p.user, []).append(p.nume)

        return rezultat
 

inv = Inventar.din_json("arsenal/windows/start/procese.json")
# print("procese:", len(inv))

# for p in inv.suspecte():
    # print(f"  [{p.pid}] {p.nume}  {p.cale}")
    # print(inv.pe_user())

def evenimente_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        return [Eveniment(**d) for d in json.load(f)]

 
def main():
    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    inv = Inventar.din_json(a.capturi + "/procese.json")
    ev = evenimente_din_json(a.capturi + "/evenimente.json")

    alarma = [e for e in ev if e.e_suspect()]

    if a.json:
        rezultat = {
            "suspecte": [asdict(p) for p in inv.suspecte()],
            "alarma": [asdict(e) for e in alarma]
        }

        print(json.dumps(rezultat, indent=4, ensure_ascii=False))

    else:
        print(f"Procese: {len(inv)} | suspecte: {len(inv.suspecte())}\n")
        for p in inv.suspecte():
            print(f"  [{p.pid}] {p.nume}  ({p.user})  {p.cale}")

        print(f"\nEvenimente: {len(ev)} | alarma: {len(alarma)}\n")

        for e in alarma:
            print(f"  {e.id} [{e.nivel}] {e.cont}: {e.mesaj}")

if __name__ == "__main__":
    main()

 

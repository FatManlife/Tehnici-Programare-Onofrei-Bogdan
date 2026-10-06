import re
import hashlib
import base64
from urllib.parse import unquote

#A1

# s = "Salut"
# b = s.encode()          # bytes
# print(b, b[0])          # b"Salut" 83

# TODO: tipareste b.hex() si refa bytes din hex
#       cu bytes.fromhex(...)

# h = b.hex()
# h_reformed = bytes.fromhex(h)
# print(h, h_reformed)

#A2
def ghici_strat(s):
    # TODO: daca are %xx -> "url" 
    if re.findall(r"%[A-Fa-f0-9]{2}",s):
        return "url" 
    # TODO: daca doar 0-9 a-f si lungime para -> "hex"
    elif re.fullmatch(r"([0-9a-f]{2})+", s):
        return "hex"
    # TODO: daca doar A-Za-z0-9+/= -> "base64"
    elif re.fullmatch(r"[A-Za-z0-9+=/]+", s):
        return "base64"

    return "necunoscut"
# print(ghici_strat("%2Fetc"))   # url
# print(ghici_strat("48656c6c6f"))  # hex

#A3

def desfa(s):
    strat = ghici_strat(s)
    # TODO: pentru fiecare strat, decodeaza
    #   base64 -> base64.b64decode(s)
    if strat == "base64":
        s = base64.b64decode(s)
    #   hex    -> bytes.fromhex(s)
    elif strat == "hex":
        s = bytes.fromhex(s)
    #   url    -> unquote(s).encode()
    elif strat == "url":
        s = unquote(s).encode()

    s = s.decode()
    # intoarce (strat, rezultat_bytes)
    return strat, s.encode()

#A4
def citibil(b):
    # TODO: True daca toti octetii sunt 32..126
    return all(32 <= c < 127 for c in b)
 
# val = "NTM1OTU3NTk="
# for _ in range(8):
#     strat, b = desfa(val)
#     # TODO: daca citibil(b): opreste si tipareste
#     #       altfel val = b.decode(); continua
#     if citibil(b):
#         print(b)
#         break
#     else:
#         val = b.decode()
    
#A5
# date = open("../../probe/xor.bin", "rb").read()

# for k in range(256):
#     clar = bytes(b ^ k for b in date)
#     # TODO: daca citibil(clar):
#     # print("cheie:", k, clar.decode())
#     if citibil(clar):
#         print("cheie:", k, clar.decode())


#A6
# tinta = open("../../probe/hashuri.txt").readline().strip()
# print(len(tinta))   # 32 md5 / 40 sha1 / 64 sha256
# for cuv in open("../../probe/wordlist.txt", encoding="latin1"):    
#     cuv = cuv.strip()
#     # TODO: daca hashlib.md5(cuv.encode()).hexdigest()
#     #       == tinta: print("gasit:", cuv); break
#     if hashlib.md5(cuv.encode()).hexdigest() == tinta:
#         print("gasit:", cuv)
#         break

#A7
import argparse, json
p = argparse.ArgumentParser()
p.add_argument("intrare")          # sir sau cale
p.add_argument("--fisier", action="store_true")
a = p.parse_args()
# TODO: daca a.fisier, citeste octetii din cale;
#       altfel trateaza intrarea ca sir
# TODO: salveaza {strat, rezultat} in
#       arsenal/forensics/fisa.json
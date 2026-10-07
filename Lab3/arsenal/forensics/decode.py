import re
import hashlib
import argparse, json
import base64
from urllib.parse import unquote
from PIL import Image
from PIL.ExifTags import TAGS

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
# if __name__ == "__main__": 
#     p = argparse.ArgumentParser()
#     p.add_argument("intrare")          # sir sau cale
#     p.add_argument("--fisier", action="store_true")
#     a = p.parse_args()
#     # TODO: daca a.fisier, citeste octetii din cale;
#     #       altfel trateaza intrarea ca sir
#     data = None

#     if a.fisier:
#         with open(a.intrare, "rb") as f:
#             data = f.read().decode()
#     else:
#         data = a.intrare


#     strat, rez = desfa(data)


#     # TODO: salveaza {strat, rezultat} in
#     #       arsenal/forensics/fisa.json
#     with open("fisa.json", "w") as f:
#         json.dump({"strat": strat, "rezultat":rez.decode()}, f)

#B1
def tip_real(cale):
    cap = open(cale, "rb").read(8)


    print(cap)

    # TODO: daca cap incepe cu b"%PDF" -> "pdf"
    #       b"\x89PNG" -> "png" ; b"\xff\xd8" -> "jpeg"
    #       b"PK\x03\x04" -> "zip/docx"

    if cap.startswith(b"%PDF"):
        cap = "pdf"
    elif cap.startswith(b"\x89PNG"):
        cap = "jpeg"
    elif cap.startswith(b"\xff\xd8"):
        cap = "jpeg"
    elif cap.startswith(b"PK\x03\x04"):
        cap = "zip/docx"

    return cap.encode().hex()

# print(tip_real("../../probe/foto.jpg"))

#B2
# date = open("../../probe/ascuns.png", "rb").read()
# # TODO: for m in re.findall(rb"[ -~]{4,}", date):
# #           print(m.decode())
# # cauta un indiciu: o cale, un mesaj, un nume de fisier
# for m in re.findall(rb"[ -~]{4,}", date):
#     print(m.decode())

#B3

# exif = Image.open("../../probe/foto.jpg")._getexif() or {}

# for id, val in exif.items():
#     print(TAGS.get(id, id), "=", val)
# # TODO: ia blocul GPS (tag 34853) si tipareste
# #       latitudinea si longitudinea
#     if id == 34853:
#         print(f"\nLatitudinea este {val[1]} {float(val[2][0] + val[2][1]/60 + val[2][2]/3600)} iar Longitudinea este {val[3]} {float(val[4][0] + val[4][1]/60 + val[4][2]/3600)} ")

# date = open("../../probe/ascuns.png", "rb").read()
# i = date.find(b"PK\x03\x04")

# TODO: daca i != -1:
#   open("gasit.zip","wb").write(date[i:])
#   print("arhiva extrasa de la octetul", i)
# apoi dezarhiveaza si vezi ce era inauntru

# if i != -1:
#     open("gasit.zip","wb").write(date[i:])
#     print("arhiva extrasa de la octetul", i)

#B5

# img = Image.open("../../probe/foto.jpg").convert("RGB")
# px = img.get_flattened_data()
# mesaj = b"FLAG{ascuns_in_pixeli}\0"
# biti = "".join(f"{c:08b}" for c in mesaj)

# canale = [c for p in px for c in p]

# # TODO: pentru fiecare bit, ia un canal si pune
# #   canal = (canal & ~1) | int(bit)
# # TODO: img.putdata(px_nou); img.save("stego.png")

# for i,bit in enumerate(biti):
#     canale[i] = (canale[i] & ~1) | int(bit)

# px_nou = [tuple(canale[i:i+3]) for i in range(0, len(canale), 3)]

# img.putdata(px_nou)
# img.save("stego.png")

#B6
# px = list(Image.open("stego.png").convert("RGB").get_flattened_data())
# biti = ""

# for (r, g, b) in px:
#     # TODO: aduna ultimii biti (r&1, g&1, b&1)
#     biti += str(r & 1) + str(g & 1) + str(b & 1)
# # TODO: grupeaza cate 8 biti -> octeti -> text
# #       opreste-te la primul octet 0 (final de mesaj)

# l = []

# for i in range(0, len(biti) - 7, 8):
#     octet = int(biti[i:i+8],2)

#     if octet == 0:
#         break

#     l.append(octet)

# mesaj = bytes(l)
# print(mesaj)

# PENTRU VÂRFUL SĂLII (opțional).  Dacă termini devreme, în probe/ găsești challenge.bin: un fișier care combină tot ce
# ai făcut azi (un strat de encoding peste un XOR, cu un hash de verificat)
# . Despică-l singur, fără schelet, și pune pașii în raport. Este genul de problemă pe care o vei întâlni pe pwn.college și
# pe challenge-urile de forensics

data = None

with open("../../probe/challenge.bin", "rb") as f:
    data = f.read()

byte_data = base64.b64decode(data)

for i in range(256):
    decoded = bytes(b ^ i for b in byte_data)

    if all(32 <= b <= 127 for b in decoded):
        print(i, decoded)


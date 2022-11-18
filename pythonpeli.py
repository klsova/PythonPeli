#Importit

from tkinter import *
import random

#Kyseessä on siis klassinen matopeli

#Vakiot
PELIN_LEVEYS = 600
PELIN_KORKEUS = 600
KOKO = 50
NOPEUS = 100
KAARMEEN_KEHO_PITUUS = 3
KAARME_VARI = "#194fff"
RUOKA_VARI = "#ffec19"
TAUSTA_VARI = "#000000"

#Luokat
class Kaarme:
    
    def __init__(self):
        self.body_size = KAARMEEN_KEHO_PITUUS
        self.coordinates = []
        self.neliot =  []

        for i in range(0, KAARMEEN_KEHO_PITUUS):
            self.coordinates.append([0, 0])
            
        for x, y in self.coordinates:
            nelio = tausta.create_rectangle(x, y, x + KOKO, y + KOKO, fill=KAARME_VARI, tag="kaarme")
            self.neliot.append(nelio)


class Ruoka:
    
    def __init__(self):
        x = random.randint(0 , (PELIN_LEVEYS/KOKO)-1) * KOKO
        y = random.randint(0 , (PELIN_KORKEUS/KOKO)-1) * KOKO
        self.coordinates = [x, y]
        
        tausta.create_rectangle(x,y , x + KOKO, y + KOKO, fill=RUOKA_VARI, tag="ruoka")

#Liikkuminen ja yleiset pelinmekaniikat

def seur_kaannos(kaarme, ruoka):
    
    x, y = kaarme.coordinates[0]

    if suunta == "ylos":
        y -= KOKO
    elif suunta == "alas":
        y += KOKO
    elif suunta == "oikea":
        x += KOKO
    elif suunta == "vasen":
        x -= KOKO

    kaarme.coordinates.insert(0, (x, y))

    nelio = tausta.create_rectangle(x, y, x + KOKO, y + KOKO, fill=KAARME_VARI)

    kaarme.neliot.insert(0, nelio)

    if x == ruoka.coordinates[0] and y == ruoka.coordinates[1]:

        global pisteet

        pisteet += 1

        pistetaulu.config(text="Pisteet:{}".format(pisteet))

        tausta.delete("ruoka")

        ruoka = Ruoka()

    else:
        del kaarme.coordinates[-1]

        tausta.delete(kaarme.neliot[-1])

        del kaarme.neliot[-1]

    if tormaykset(kaarme):
        peli_ohi()

    else:
        nakyma.after(NOPEUS, seur_kaannos, kaarme, ruoka)

def vaihda_suunta(uusi_suunta):
    
    global suunta

    if uusi_suunta == 'vasen':
        if suunta != 'oikea':
            suunta = uusi_suunta
    elif uusi_suunta == 'oikea':
        if suunta != 'vasen':
            suunta = uusi_suunta
    elif uusi_suunta == 'ylos':
        if suunta != 'alas':
            suunta = uusi_suunta
    elif uusi_suunta == 'alas':
        if suunta != 'ylos':
            suunta = uusi_suunta
    

def tormaykset(kaarme):
    x, y = kaarme.coordinates[0]

    if x < 0 or x >= PELIN_LEVEYS:
        return True
    elif y < 0 or y >= PELIN_KORKEUS:
        return True

    for body_part in kaarme.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False

def peli_ohi():
    tausta.delete(ALL)
    tausta.create_text(tausta.winfo_width()/2, tausta.winfo_height()/2, font=('Comic Sans MS', 70), text="Hävisit Pelin!", fill="red", tag="peliohi")

#Pelin UI

nakyma = Tk()

nakyma.title("Python Peli")
nakyma.resizable(False, False)

pisteet = 0
suunta = 'alas'

pistetaulu = Label(nakyma, text= "Pisteet:{}".format(pisteet), font=('Comic Sans MS', 45))
pistetaulu.pack()

highscore= Label(nakyma, text= "Highscore: ")

tausta = Canvas(nakyma, bg=TAUSTA_VARI, height= PELIN_KORKEUS, width= PELIN_LEVEYS)
tausta.pack()

nakyma.update()

nakyma_leveys = nakyma.winfo_width()
nakyma_korkeus = nakyma.winfo_height()
naytto_leveys = nakyma.winfo_screenwidth()
naytto_korkeus = nakyma.winfo_screenheight()

x = int((naytto_leveys/2) - (nakyma_leveys/2))
y = int((naytto_korkeus/2) - (nakyma_korkeus/2))

nakyma.geometry(f'{nakyma_leveys}x{nakyma_korkeus}+{x}+{y}')

#Käärme ja ruoka generointi sekä aloitusnapin ja ohejeiden poisto
def aloitus():
    aloitusnappi.destroy()
    ohjeet.destroy()
    python = Kaarme()
    ruoka = Ruoka()
    seur_kaannos(python, ruoka) 

#Aloitusnappi

kuva = PhotoImage(file= 'thinking.png')

aloitusnappi = Button(nakyma, text="Aloita peli?", font=("Comic Sans MS", 50), bg="black", fg="#ffec19", highlightbackground="white", command=aloitus, image=kuva, compound= "bottom")
aloitusnappi.place(x= 100, y= 180)

#Ohjeet

ohjeet = Label(nakyma, text="Liiku käyttäen nuolinäppäimiä!", bg="black", fg="white", font=("Comic Sans MS", 30))
ohjeet.place(x=25, y= 100)



#Keybindit

nakyma.bind('<Left>', lambda event: vaihda_suunta('vasen'))
nakyma.bind('<Right>', lambda event: vaihda_suunta('oikea'))
nakyma.bind('<Down>', lambda event: vaihda_suunta('alas'))
nakyma.bind('<Up>', lambda event: vaihda_suunta('ylos'))

nakyma.mainloop()

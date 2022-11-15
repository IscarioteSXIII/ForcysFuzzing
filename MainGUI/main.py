"""
Contexte :      Projet Python Aforp - Fuzzing

Description :   Interface graphique regroupant :
                    - Network Scanner based on NMAP
                    - Crawler HTTP(S)
                    - Différent fuzzing (SQL, WEB, ...)

Auteurs :       Enzo PALASSIN :
                    - Integration GUI / Scanner / Crawler
                Adrien P :
                    - Documentation
                Guillaume DUJON :
                    - x
                Julien DEGRAVE :
                    - Fuzzing SQL / DDOS
                JEREMIE GUIBERT :
                    - x         
"""

from tkinter import *
from tkinter import ttk, messagebox
import threading
import os
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime

#Main GUI
root = Tk()
root.title("Network scanner - GUI")

#Variables
selected_profil = StringVar()
CommandEntry = StringVar()
Cible = StringVar()
NMAP_Command = StringVar()

URLEntry = StringVar()
pall = IntVar()
p404 = IntVar()
pformular = IntVar()
pext_url = IntVar()


#Functions
class Crawler():

    def __init__(self, url):
        self.primary_url = urlparse(url).netloc     # Récupère le nom de domaine
        self.urls_to_visit = [url]                  # URLs à crawler
        self.urls_visited = []                      # URLs checked
        self.urls_404 = []                          # URLs response code 404
        self.urls_external_domain = []              # URLs avec un nom de domaine différent de la cible
        self.urls_protected = []                    # Page protégé par un mot de passe
        self.urls_formulaire = []                   # Page contenant un formulaire


    def get_page(self, url):
        """
            Gestion des différentes page HTML
        """
        if urlparse(url).netloc == self.primary_url:
            page = requests.get(url)
            if page.status_code == "404": # Gestion des pages 404
                self.urls_404.append(url)
            else:
                return page.content # Gestion des pages normaux (pas de 404, formulaire etc...)
        else:
            self.urls_external_domain.append(url) # Gestion des domaines externes


    def get_links(self, url, html):
        """
            Gestion des liens
        """
        soup = BeautifulSoup(html, "html.parser")
        for link in soup.find_all("a"):
            chemin = link.get("href")
            if chemin and not chemin.startswith("#"):
                if chemin.startswith("/"): 
                    chemin = urljoin(url, chemin)
                elif chemin.startswith("https://") or chemin.startswith("http://"):
                    chemin = chemin
                else:
                    return
                if chemin not in self.urls_to_visit:
                    self.urls_to_visit.append(chemin)


    def find_special_page(self, url, page):
        """
            Trouver les pages contenant des formulaires, des mots de passe etc...
        """
        if url not in self.urls_formulaire and url not in self.urls_protected and url not in self.urls_external_domain:
            formulaire = BeautifulSoup(page, "html.parser").find_all("form")
            protected = BeautifulSoup(page, "html.parser").find_all("password")
            if formulaire:
                #print("{} Une page avec un formulaire ! URL: {}".format(time, url))
                self.urls_formulaire.append(url)
                

    def crawl(self, url):
        """
            Crawler
        """
        page = self.get_page(url)
        self.get_links(url, page)
        self.find_special_page(url, page)


    #Les différentes fonctions appelées selon les choix de l'utilisateurs
    def run(self):
        """
            Execute le programme normalement
        """
        CrawlerOutput.delete("0.0", END)

        for url in self.urls_to_visit:
            CrawlerOutput["state"] = "normal"
            CrawlerOutput.insert("end", "{} Crawling: {}\n".format(datetime.now().time(), url))
            CrawlerOutput["state"] = "disabled"            
            try:
                self.crawl(url)
            except:
                if url in self.urls_external_domain:
                    CrawlerOutput["state"] = "normal"
                    CrawlerOutput.insert("end", "{} Not the same domain. Don't crawl: {}\n".format(datetime.now().time(), url))
                    CrawlerOutput["state"] = "disabled"
                else:
                    CrawlerOutput["state"] = "normal"
                    CrawlerOutput.insert("end", "{} Failed to crawl: {}\n".format(datetime.now().time(), url))
                    CrawlerOutput["state"] = "disabled"
            finally:
                self.urls_visited.append(url)
        #print(self.urls_protected)
        


    def run404(self):
        """
            Execute le programme et n'affiche que les pages 404
        """
        CrawlerOutput.delete("0.0", END)
        CrawlerOutput["state"] = "normal"
        CrawlerOutput.insert("end", "{} Crawling {}.\n==> A la recherche des pages 404.\n".format(datetime.now().time(), self.primary_url))
        CrawlerOutput["state"] = "disabled"
        for url in self.urls_to_visit:
            try:
                self.crawl(url)
            except:
                url in self.urls_external_domain
            finally:
                self.urls_visited.append(url)
        if len(self.urls_404) > 0:
            CrawlerOutput["state"] = "normal"
            CrawlerOutput.insert("end", "{} Trouvé ! {}\n".format (datetime.now().time(), self.urls_404))
            CrawlerOutput["state"] = "disabled"
        else:
            CrawlerOutput["state"] = "normal"
            CrawlerOutput.insert("end", "{} Pas de page 404\n".format(datetime.now().time()))
            CrawlerOutput["state"] = "disabled"
            

    def run_external_url(self):
        """
            Execute le programme et n'affiche que les pages redirigeant vers un domaine externe.
        """
        CrawlerOutput.delete("0.0", END)
        CrawlerOutput["state"] = "normal"
        CrawlerOutput.insert("end", "{} Crawling {}.\n==> A la recherche des pages redirigeant vers un domaine externe.\n".format(datetime.now().time(), self.primary_url))
        CrawlerOutput["state"] = "disabled"
        for url in self.urls_to_visit:
            try:
                self.crawl(url)
            except:
                url in self.urls_external_domain
            finally:
                self.urls_visited.append(url)
        if len(self.urls_external_domain) > 0:
            CrawlerOutput["state"] = "normal"
            CrawlerOutput.insert("end", "{} Trouvé ! {}\n" .format(datetime.now().time(), self.urls_external_domain))
            CrawlerOutput["state"] = "disabled"
        else:
            CrawlerOutput["state"] = "normal"
            CrawlerOutput.insert("end", "{} Pas de page redirigeant vers un domaine externe.\n".format(datetime.now().time()))
            CrawlerOutput["state"] = "disabled"


    def run_formular(self):
        """
            Execute le programme et n'affiche que les pages contenant un formulaire
        """
        CrawlerOutput.delete("0.0", END)
        CrawlerOutput["state"] = "normal"
        CrawlerOutput.insert("end", "{} Crawling {}.\n==> A la recherche des pages contenant un quelconque formulaire.\n".format(datetime.now().time(), self.primary_url))
        CrawlerOutput["state"] = "disabled"
        for url in self.urls_to_visit:
            try:
                self.crawl(url)
            except:
                url in self.urls_external_domain
            finally:
                self.urls_visited.append(url)
        if len(self.urls_formulaire) > 0:
            CrawlerOutput["state"] = "normal"
            CrawlerOutput.insert("end", "{} Trouvé ! {}\n".format(datetime.now().time(), self.urls_formulaire))
            CrawlerOutput["state"] = "disabled"
        else:
            CrawlerOutput["state"] = "normal"
            CrawlerOutput.insert("end", "{}Pas de page contenant un formulaire.\n".format(datetime.now().time()))
            CrawlerOutput["state"] = "disabled"


def LaunchCrawl():
    CrawlerOutput.delete("0.0", END)
    url = URLEntry.get()
    if url:
        launch = threading.Thread(target=StartCrawl, args=(url,))
        launch.start()
    else:
        messagebox.showwarning(title="Warning!", message="No tagert URL found!")


def StartCrawl(url):
    if (pall.get() == 1):
        claunch = threading.Thread(target=Crawler(url).run())
        claunch.start()
    elif (p404.get() == 1):
        claunch = threading.Thread(target=Crawler(url).run404())
        claunch.start()
    elif (pformular.get() == 1):
        claunch = threading.Thread(target=Crawler(url).run_formular())
        claunch.start()
    elif (pext_url.get() == 1):
        claunch = threading.Thread(target=Crawler(url).run_external_url())
        claunch.start()


def LaunchScan():
    #global slaunch
    slaunch = threading.Thread(target=GoScan, args=('',))
    slaunch.start()
    

def SetCommandEntry(event):
    profil = selected_profil.get()
    if profil == "Intense Scan":
        CommandEntry.set("nmap -T4 -A -v")
    elif profil == "Intense Scan - All TCP Port":
        CommandEntry.set("nmap -p 1-65535 -T4 -A -v")
    elif profil == "Stealth":
        CommandEntry.set("nmap -sS -sV")


def GoScan(foo):
    entry_NmapOutput["state"] = "normal"
    entry_NmapOutput.delete("0.0", END)
    entry_NmapOutput.insert("0.0", "Scanning started - Please wait until finished, it might takes few minutes")
    entry_NmapOutput["state"] = "disabled"

    NMAP_Command.set(CommandEntry.get() + " " + Cible.get())
    response = os.popen(f"{CommandEntry.get()} {Cible.get()}").read()

    entry_NmapOutput["state"] = "normal"
    entry_NmapOutput.delete("0.0", END)
    entry_NmapOutput.insert("0.0", response)
    entry_NmapOutput["state"] = "disabled"


def NewCrawlWindow():
    #creation de la fenêtre crawler http
    global CrawlerOutput

    CrawlWindow = Toplevel(root)
    CrawlWindow.title("Crawler HTTP(S)")
    CrawlWindowWidth = 800
    CrawlWindowHeight = 550
    CrawlWindow.geometry("%dx%d+%d+%d" % (CrawlWindowWidth, CrawlWindowHeight, x, y))

    lbl_urlcible = Label(CrawlWindow, text="URL Cible: ", font=("calibri", 12)).place(x=10, y=10)
    lbl_option = Label(CrawlWindow, text="Options: ", font=("calibri", 12)).place(x=10, y=45)
    entry_urlcible = Entry(CrawlWindow, font=("calibri", 11), width=97, textvariable=URLEntry).place(x=95, y=12)

    chkb_404 = Checkbutton(CrawlWindow, text="Pages 404", font=("calibri", 11) ,variable=p404, onvalue=1, offvalue=0).place(x=95, y=63)
    chkb_formular = Checkbutton(CrawlWindow, text="Formulaires", font=("calibri", 11) ,variable=pformular, onvalue=1, offvalue=0).place(x=200, y=63)
    chkb_exturl = Checkbutton(CrawlWindow, text="URL externes", font=("calibri", 11) ,variable=pext_url, onvalue=1, offvalue=0).place(x=318, y=63)
    chkb_all = Checkbutton(CrawlWindow, text="Toutes les pages", font=("calibri", 11) ,variable=pall, onvalue=1, offvalue=0).place(x=95, y=40)

    scan_button = Button(CrawlWindow, text = "Start scanning", font=("calibri", 10), command =LaunchCrawl).place(x=685,y=40)


    CrawlerOutput = Text(CrawlWindow, width=94, height=27)
    CrawlerOutput["state"] = "disabled"
    CrawlerOutput.place(x=20, y=100)




#Taille de la fenêtre Root
width = 850
height = 600
#Taille de l'écran du PC
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
#Placement de la fenêtre sur l'écran
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)

#Labels
lbl_profil = Label(root, text="Profil: ", font=("calibri", 12)).place(x=470, y=10)
lbl_cible = Label(root, text="Cible: ", font=("calibri", 12)).place(x=10, y=10)
lbl_command = Label(root, text="Commande: ", font=("calibri", 12)).place(x=10, y=36)

#Combobox
profil_cb = ttk.Combobox(root, textvariable=selected_profil, font=("calibri", 10), width=23)
profil_cb["values"] = ["Intense Scan","Intense Scan - All TCP Port", "Stealth"]
profil_cb["state"] = "readonly"
profil_cb.place(x=520, y=12)
profil_cb.bind("<<ComboboxSelected>>", SetCommandEntry)

#Cible entry
entry_cible = Entry(root, font=("calibri", 11), width=50, textvariable=Cible).place(x=95, y=12)
entry_commande = Entry(root, font=("calibri", 12), width=76, textvariable=CommandEntry).place(x=95, y=38)

entry_NmapOutput = Text(root, width=100, height=30)
entry_NmapOutput["state"] = "disabled"
entry_NmapOutput.place(x=20, y=100)

#Buttons
scan_button = Button(root, text = "Start scanning", font=("calibri", 10), command = LaunchScan).place(x=730,y=20)

#Menu barre
menubar = Menu(root)
root.config(menu=menubar)

menucrawl = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Scan Web", menu=menucrawl)
menucrawl.add_command(label="Crawler HTTP(s)", command=NewCrawlWindow)

#Affichage GUI
root.mainloop()
os.kill(os.getpid(), 9)
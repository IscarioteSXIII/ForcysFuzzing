#!/usr/bin/env python3

import wfuzz

from simple_term_menu import TerminalMenu

option = ["URL","DICO","Fuzzing URL","Get payload","Get session","Interacting with the results","Exit"]
mainMenu = TerminalMenu(option, title = 'main menu')

quitting = False

while quitting == False:
    optionsIndex = mainMenu.show()
    optionsChoice = option[optionsIndex]

    if(optionsChoice == "URL"):
        print("Select URL")
        URLfuzz = input()

    if(optionsChoice == "DICO"):
        print("Select DICO")
        DICO = input()

    if(optionsChoice == "Exit"):
        quitting = True

    if(optionsChoice == "Fuzzing URL"):
        print("Fuzzing URL")
        for r in wfuzz.fuzz(url=f"{URLfuzz}", hc=[404], payloads=[("file",dict(fn=f"{DICO}"))]):
            print(r)

    if(optionsChoice == "Get payload"):
        print("Get payload")
        s = wfuzz.get_payload(range(5))
        for r in s.fuzz(url=f"{URLfuzz}"):
            print(r)

    if(optionsChoice == "Get session"):
        print("Get session")
        s = wfuzz.get_session(f"-z range,0-10 {URLfuzz}")
        for r in s.fuzz():
            print(r)

    if(optionsChoice == "Interacting with the results"):
        print("Interacting with the results")
        with wfuzz.get_session(f"-z list --zD test -u {URLfuzz} -d uname=FUZZ&pass=FUZZ") as s:
            for r in s.fuzz():
                print(r.history.cookies.response)
                print(r.history.params.all)
                print(r.history.params.post)
                print(r.history.params.post.uname)
                print(r.history.params.post['pass'])



#"http://testphp.vulnweb.com/FUZZ"
#

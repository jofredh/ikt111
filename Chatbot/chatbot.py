run = True
internett = ['internett','nettverk','wifi','inter nett']
epost = ['epost','email','e-post','e-mail','mail','gmail','g-mail']
while run:
    svar = input("Hei, hva kan jeg hjelpe deg med i dag?\n")
    if("hei" in svar):
        print("Hei på deg\n")
    if [i for i in internett if i in svar]:
        svar=input("Har du problemer med internettet?\n")
        if("ja" in svar):
            print("Skru ruteren din av og på!\n")
            svar = input("Virket det?")
            if("ja" in svar):
                print("Supert.\n")
                run = False
            else:
                print("Søren!\n")
                svar = input("Sjekk gjerne våre nettsider for å se om det er signalproblemer i ditt område")
                run = False
    elif [i for i in epost if i in svar]:
        svar=input("Har du problemer med eposten din?\n")
        if("ja" in svar):
            svar = input("Er du koblet til internett?")
            if("nei" in svar):
                print("Start hjelperen på nytt og be om internett hjelp")
                run = False
            if("ja" in svar):
                print("Vi tilbyr ikke epost-tjenester, og kan derfor ikke hjelpe deg. Sjekk med epost-provideren din.")
                run = False
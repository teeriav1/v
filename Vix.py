from datetime import datetime
import time
import http.client
import os
import socket
import urllib.request


#This is multiplier to show more or to show less. Basevalue is 1

class Lista():
    def __init__(self):
        self.expensive = []
        self.red = []
        self.yellow = []
        self.vixinkorjaustarve = False
        self.limitlista = []
        self.lenlist = []
    def lisaa_luku(self, luku):
        self.expensive.append(luku)
    def lukujenKeskiarvo(self):
        summa = 0
        for i in range(len(self.expensive)):
            summa += self.expensive[i]
        for i in range(len(self.red)):
            cheapinpalat = str(self.red[i]).split("+")
            cheaplisays = float(cheapinpalat[1])
            summa += cheaplisays
        print("Ylitysmaara (%) ",end="")
        amount = 0
        for i in range(len(self.limitlista)):
           muuttuja = str(self.limitlista[i]).strip("\n")
           muuttuja = float(muuttuja)
           amount += muuttuja
        printti = 1.0
        printti = summa/amount
        printti = printti * 100
        print("{:.3f} / {}".format(printti, len(self.limitlista)))
        self.expensive = []
    def hintaListaan(self, string):
        self.red.append(string)
    def searchRed(self):
        toinenLista = self.red
        self.red = []
        return(toinenLista)            
paskalista = Lista()  
rahalista = Lista()      

def getvix():
    try:
        link = "https://www.marketwatch.com/investing/index/vix/charts"
        file = urllib.request.urlopen(link)
        myfile = file.read()
        myfile = str(myfile)
        osat = []
        osat = myfile.split('class="value">')
        osa1 = str(osat[1])
        toinenjako = osa1.split("</span")
        stringtobereturned = str(toinenjako[0])
        link = "https://www.marketwatch.com/investing/index/vix/charts"
        file = urllib.request.urlopen(link)
        myfile = file.read()
        myfile = str(myfile)
        partsToSplitPercent = myfile.split('"priceChangePercent":"')
        wantedPart = str(partsToSplitPercent[1])
        partsToSplitPercent = wantedPart.split('"')
        perCent = partsToSplitPercent[0]
        perCent = str(perCent)
        print("Vix change", perCent)
        return(stringtobereturned)
    except IndexError:
            link = "https://finance.yahoo.com/quote/%5EVIX/?guccounter=1"
            limit = 9999
            Vixstring = (readlinkYahoo(link, limit))
            stringSplit = Vixstring.split("+")
            wantedPart = stringSplit[1]
            wantedPart = str(wantedPart)
            return(wantedPart)
    except IOError:
        return 0.00    
def addToThelist(Mahdollinenlisays, limit, ListaNimistäJaHinnoista, kerroin):
    limit = limit * kerroin
    limit = float(limit)
    splitOfReadPrice = Mahdollinenlisays.split("+")
    vertaushinta = splitOfReadPrice[1]
    vertaushinta = float(vertaushinta)
    printti = float(vertaushinta / limit) * 100
    printti = int(printti)
    paskalista.lisaa_luku(printti)
    if vertaushinta < limit:
        #return(Mahdollinenlisays)
        return( Mahdollinenlisays+"+"+str(limit))
    else:
        paskalista.hintaListaan(Mahdollinenlisays+"+"+str(limit))
        return("a")                
def tenToTwoSpread():
    link = "https://ycharts.com/indicators/10_2_year_treasury_yield_spread"
    file = urllib.request.urlopen(link)
    myfile = file.read()
    myfile = str(myfile)
    firstSplit = myfile.split('class="key-stat-title')
    wantedPart = firstSplit[1]
    secondSplit = wantedPart.split("%")
    wantedPart = secondSplit[0]
    wantedPart = str(wantedPart)
    printti = ""
    for i in range(5):
        if wantedPart[i-5] == " ":
            pass
        else:
            printti += wantedPart[i-5]
    return printti
def readlinkNorndet(link, limit):
    try:    
        file = urllib.request.urlopen(link)
        NameToBeSplitFromLink = str(link)
        LinkParts = NameToBeSplitFromLink.split('-')
        stockname = str("")
        for i in range(len(LinkParts) - 1):
            stockname = stockname + str(LinkParts[i + 1])
            if len(LinkParts) > (i + 2):
                stockname += "-"
        stockname = stockname.upper()
        if "VANGUARD-" in stockname:
            vanguardSplitParts = stockname.split("VANGUARD-")
            tempSAve = vanguardSplitParts[1]
            stockname = str(tempSAve)
        myfile = file.read()
        myfile = str(myfile)
        price = myfile.split('StatsBox__StyledPriceText')
        price2 = str(price[2])
        price3 = price2.split('>')
        price = str(price3[1])
        price = str(price)
        price2 = price.split('<')
        price3 = str(price2[0])
        price3.replace(",", ".",1)
        price = price3.split(',')
        price2 = str("")
        price2 = str(price[0]) + "." + str(price[1])


        stockprice = float(price2)
        limit = float(limit)
        kerroin = 1
        limit = limit * kerroin            
        #print("{:10s} now {:.2f}" .format(stockname,stockprice))            
        stockprice = str(stockprice)
        stockprice = stockprice.strip(",")
        StringPalautettavaksi = stockname + "+" + stockprice
        #print(StringPalautettavaksi)
        return(StringPalautettavaksi)
    except ValueError:
        print("ValueError: Readlink Nordnet: Reading link:", link)
    print(stockname)
def readlinkYahoo(link, limit):
    try:    
        file = urllib.request.urlopen(link)
    except socket.gaierror:
        print("gaierror: ReadLinkYahoo: URL READ \n" + link)
    NameToBeSplitFromLink = str(link)
    NameToBeSplitFromLink = NameToBeSplitFromLink.split('/quote/')
    stockname = str(NameToBeSplitFromLink[1])
    checkpoint = 0
    try:
        NameToBeSplitFromLink = stockname.split('.')
        stockname = str(NameToBeSplitFromLink[0])
    except ValueError:
        checkpoint = 0
    try:
        NameToBeSplitFromLink = stockname.split('?')
        stockname = str(NameToBeSplitFromLink[0])
    except ValueError:
        checkpoint = 0
    if checkpoint > 0:
        print("ValueError: Nimen halkaisu" + stockname)
        checkpoint = 0     
    myfile = file.read()
    myfile = str(myfile)
    myfile = myfile.split(' data-reactid="14">') 
    striptosplit = str(myfile[4])
    myfile = striptosplit.split('data-reactid="32">')
    striptosplit = str(myfile[1])
    myfile = striptosplit.split('</span>')    
    stockprice = myfile[0]
    stockprice = stockprice.strip(",")
    try:

        #This fixes valueErrors with prices above 1000
        if "," in stockprice:
            bufferi = ""
            for letteri in stockprice:
                if letteri == ",":
                    pass
                else:
                    bufferi += letteri
            stockprice = bufferi
        stockprice = float(stockprice)
    except ValueError:
        print("ValueError: Stockprice \n" + stockprice)
        print(" ")
        


    file = urllib.request.urlopen(link)    
    try:
        limit = float(limit)
        kerroin = 1
        limit = limit * kerroin
    except ValueError:
        print("ValuError: Limit " + limit)
    stockprice = float(stockprice)        
        #print("{:10s} now {:.2f}" .format(stockname,stockprice))        
    stockprice = str(stockprice)
    stockprice = stockprice.strip(",")
    stockname = stockname.upper()
    StringPalautettavaksi = stockname + "+" + stockprice
    print(StringPalautettavaksi)
    return(StringPalautettavaksi)
def readfile(kerroin):    
    file_to_be_read = open(r"C:\stocksites.txt", "r")
    rivi = file_to_be_read.readline()
    rivinjako = rivi.split(",")
    rivi = rivinjako[0]
    limit = rivinjako[1]
    MahdollinenLisays = "0"
    #readlinkYahoo(rivi, limit)
    ListaNimistäJaHinnoista = []
    LineCounter = 0
    while rivi != "":
        try:
            time.sleep(1)
            rivi = file_to_be_read.readline()
            rivinjako = rivi.split(",")
            rivi = rivinjako[0]
            limit = rivinjako[1] 
            paskalista.limitlista.append(limit)
            rivi = str(rivi)
            toADD = "a"
            try:
                limit = float(limit)
            except ValueError:
                print("ValueError: Readfile: Limit" + limit)
            #time.sleep(3)
            if "yahoo" in rivi:
                checkpoint = 0
                while checkpoint == 0:
                    try:
                        MahdollinenLisays = readlinkYahoo(rivi, limit)
                        
                        print(LineCounter, end ="") 
                        LineCounter += 1
                        checkpoint = 1

                    except IOError:
                        print(".", end ="") 
                        # delete next line, it is for debug
                        break

                    except http.client.IncompleteRead:
                        print(".", end="")                        

            elif "nordnet" in rivi:

                checkpoint = 0
                while checkpoint == 0:
                    try:                
                        MahdollinenLisays = readlinkNorndet(rivi, limit)
                        #print(LineCounter, end ="") 
                        print(MahdollinenLisays)
                        LineCounter += 1
                        checkpoint = 1                        
                    except IOError:
                        print(".", end="")
                    except http.client.IncompleteRead:
                        print(".", end="")
            else:
                break
            toADD = addToThelist(MahdollinenLisays, limit, ListaNimistäJaHinnoista,kerroin)
            toADD = str(toADD)    
            if len(toADD) > 1 :
                ListaNimistäJaHinnoista.append(toADD)
        except ValueError:
            print("ValueError: def_Readfile: Main\n")
            print(rivi)
            print(MahdollinenLisays)
            
        except IndexError:
            #print("\nIndexError: def Readfile: Main")
            if "nordnet" in rivi:
                rivi = rivi.strip("https://www.nordnet.fi/markkinakatsaus/")
            print(rivi)
    return(ListaNimistäJaHinnoista)    
def timeanddate():            
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time ", dt_string)	
def clean():
    time.sleep(10)
    #Old, worked on python 3.7
    print('cls')
    print("\033[H\033[J")

    print('\x1bc')
    print(chr(27) + '[2j')
    os.system('cls')
    os.system('cls' if os.name=='nt' else 'clear')
    #os.system("ls")
    print(u"{}[2J{}[;H".format(chr(27), chr(27)))
def vixinkorjaus():
    print("")
    VixinKorjaustarve = True
    while VixinKorjaustarve == True:
        try:
            vixValue = getvix()            
            print("VIX is now   " + vixValue)
            VixinKorjaustarve = False    
            break
        except IOError:
            print(".",end="")  
            break
def vixForFirstRound():
        paskalista.vixinkorjaustarve = True          
        try:                                        
            print("VIX is now   " + getvix())
            paskalista.vixinkorjaustarve = False                  
        except IOError:
                print("IOError: Getvix() inside VixForFirstRound")                
        except IndexError:
            print("IOError: Getvix() inside VixForFirstRound")
def bitcoin():
    rivi = "https://finance.yahoo.com/quote/BTC-USD?p=BTC-USD"
    def rivinhaku(rivi):
        file = urllib.request.urlopen(rivi)
        siteRead = file.read()
        siteRead = str(siteRead)
        siteReadFirstSplit = siteRead.split('data-reactid="33">')
        wantedPart = str(siteReadFirstSplit[3])
        siteReadSecondSplit = wantedPart.split("</span><div")
        printti = siteReadSecondSplit[0]
        splitToPercent1 = printti.split("(")
        wantedPart = str(splitToPercent1[1])
        splitToPercent2 = wantedPart.split("%")
        percentChange = splitToPercent2[0]
        percentChange = percentChange.strip("+")
        printti = float(percentChange)
        return printti
    # delete next #, it is for debug
    #print("BTC", rivinhaku(rivi), "%")
def goodmoney():    
    goodmoneyNet = []
    badmoneyList = ["https://finance.yahoo.com/quote/PHP%3DX?p=PHP%3DX","https://finance.yahoo.com/quote/CNY%3DX?p=CNY%3DX","https://finance.yahoo.com/quote/INR%3DX?p=INR%3DX","https://finance.yahoo.com/quote/MXN%3DX?p=MXN%3DX","https://finance.yahoo.com/quote/IDR%3DX?p=IDR%3DX","https://finance.yahoo.com/quote/THB%3DX?p=THB%3DX","https://finance.yahoo.com/quote/MYR%3DX?p=MYR%3DX","https://finance.yahoo.com/quote/ZAR%3DX?p=ZAR%3DX","https://finance.yahoo.com/quote/RUB%3DX?p=RUB%3DX"]
    goodmoneyList = ["https://finance.yahoo.com/quote/%5EEUI/","https://finance.yahoo.com/quote/DX-Y.NYB/","https://finance.yahoo.com/quote/%5ESFC/"]
    badmoneyNet = []
    for i in range(len(goodmoneyList)):
        file = urllib.request.urlopen(goodmoneyList[i])
        siteRead = file.read()
        siteRead = str(siteRead)
        siteReadFirstSplit = siteRead.split('data-reactid="33">')
        wantedPart = str(siteReadFirstSplit[3])
        siteReadSecondSplit = wantedPart.split("</span><div")
        printti = siteReadSecondSplit[0]    
        splitToPercent1 = printti.split("(")
        wantedPart = str(splitToPercent1[1])
        splitToPercent2 = wantedPart.split("%")
        percentChange = splitToPercent2[0]
        percentChange = percentChange.strip("+")
        percentChange = float(percentChange)
        goodmoneyNet.append(percentChange)    
    for i in range(len(badmoneyList)):
        file = urllib.request.urlopen(badmoneyList[i])
        siteRead = file.read()
        siteRead = str(siteRead)
        siteReadFirstSplit = siteRead.split('data-reactid="33">')
        wantedPart = str(siteReadFirstSplit[3])
        siteReadSecondSplit = wantedPart.split("</span><div")
        printti = siteReadSecondSplit[0]    
        splitToPercent1 = printti.split("(")
        wantedPart = str(splitToPercent1[1])
        splitToPercent2 = wantedPart.split("%")
        percentChange = splitToPercent2[0]
        percentChange = percentChange.strip("+")
        percentChange = float(percentChange)
        badmoneyNet.append(percentChange)   
    goodmoneyKeskiarvo = keskiarvo(goodmoneyNet)
    badmoneyKeskiarvo = keskiarvo(badmoneyNet)
    strongstring = "Strong currencies " + str(round(goodmoneyKeskiarvo,2))
    weakstring = " -- Weak ones " + str(round(badmoneyKeskiarvo,2))
    palautus = strongstring + weakstring
    return(palautus)
def keskiarvo(lista):
    summa = 0.0
    for i in range(len(lista)):
        summa += lista[i]
    keskiarvo = summa / (len(lista))
    return(keskiarvo)  
def macrolist(isFirstRoundDone, ListaNimistäJaHinnoista):
    if isFirstRoundDone == False:
        try:
            vixForFirstRound()
        except IOError:
            pass
    else:
        vixinkorjaus()
    #paskalista.lukujenKeskiarvo()
    try:
        bitcoin()
    except IOError:
        print("BTC IOError")
    try:
        print("USD 10-2 year spread = ",tenToTwoSpread())
    except IOError:
        print("10-2 spread IOError")
    laskuri = 0 #Laskuri goodmoney:lle, jos internet pätkii / tarkoitus antaa uusintayrityksiä
    while True:
        try:
            printListGoodmoney = goodmoney()
            print(printListGoodmoney)
            break
        except http.client.IncompleteRead:
            pass
        except IndexError:
            pass
        except IOError:
            if laskuri >= 10: #Laskuri goodmoney:lle, jos internet pätkii / tarkoitus antaa uusintayrityksiä
                laskuri += 1
            else:
                print("Goodmoney IOError")
                break
def printlist(ListaNimistäJaHinnoista):
    ListaNimistäJaHinnoista = cleanlist(ListaNimistäJaHinnoista)
    print("LEN# is " , len(ListaNimistäJaHinnoista),"\n")  
    for i in range(len(ListaNimistäJaHinnoista)):
        try:
            RaakaString = str(ListaNimistäJaHinnoista[i])
            RaakaStringPuolikkaat = RaakaString.split("+")
            stockname = RaakaStringPuolikkaat[0]                    
            stockprice = RaakaStringPuolikkaat[1]
            if len(RaakaStringPuolikkaat) > 2:
                limit = RaakaStringPuolikkaat[2]
                limit = float(limit)
            if "," in stockprice:
                stockprice = stockprice.strip(",")
            try:
                stockprice = float(stockprice)
                stockname = stockname.replace("-"," ")
                if "TREASURY BOND" in stockname:
                    stockname = "US TREASURY BOND"
                if len(RaakaStringPuolikkaat) == 2:
                    print("{:23s}  {:6.2f}" .format(stockname,stockprice))
                if len(RaakaStringPuolikkaat) == 3:
                    print("{:23s}  {:6.2f}   ( {:.2f} )" .format(stockname,stockprice,limit))                    
            except ValueError:
                print(stockname + "       " + stockprice)      
        except IndexError:
            print("IndexError: Second Print, rivi:\n", ListaNimistäJaHinnoista[i])    
    loop = False
def cleanlist(list):
    #This function cleans list
    #Cleansing list means removing duplicates
    #There was problem with with duplicates in lists due to Error http.client.IncompleteRead

    palautuslista = []
    for x in list:

        if x in palautuslista:
            pass
        else:
                #When market is open, there may come problems with multiple runs creating
                #multiple lines with different prices -> this is to solve that
            
                xcopy = x
                xtoparts = xcopy.split("+")
                stockname = xtoparts[0]
                stockname = str(stockname)
                viablename = True
                for name in palautuslista:
                    if stockname in name:
                        viablename = False                        
                        
                if viablename:
                    if stockname in palautuslista:
                        pass                    
                    else:
                        #x is the one to save and one to use
                        palautuslista.append(x)
    return(palautuslista)  
def testit():
    all_passed = True
    failed = []
    link = "https://www.nordnet.fi/markkinakatsaus/osakekurssit/16103263-kone-corporation"
    limit = 999
    try:
        readlinkNorndet(link, limit)
    except IOError:
        failed.append("Readlink Nordnet")
    try:        
        readlinkYahoo(link, limit)
    except IOError:
        failed.append("Readlink Yahoo")
    except IndexError:
        failed.append("Readlink Yahoo")
    try:
        goodmoney()
    except IOError:
        failed.append("Goodmoney")
    try:
        bitcoin()
    except IOError:
        failed.append("BTC")
    try:
        tenToTwoSpread()
    except IOError:
        failed.append("tenToTwoSpread")
    try:
        vixi = getvix()
        if vixi == 0.00:
            failed.append("Vix == 0")
    except IOError:
        failed.append("Vix, IO")
    except IndexError:
        failed.append("Vix, index")

    if len(failed) > 0:
        all_passed = False
    if all_passed:
        print("All tests passed")
    else:
        print("TEST FAILED: ",end="")
        for alkio in failed:
            print(alkio+", ",end="")
        print("---")

def main():
        testit()
        looppi = False
        kerroin = 1
        isFirstRoundDone = False
        ErrorTries = int(1)
        while ErrorTries > 0:
            try:
                if kerroin == 1:
                    print("Loading...\nplease wait...\n\n\n")
                #ErrorTries = int(0)
                ListaNimistäJaHinnoista = readfile(kerroin)
                clean()                
                if kerroin == 1:             
                    timeanddate()
                    print("Kerroin on " , kerroin)
                    print("\n")
                    try:
                        macrolist(isFirstRoundDone, ListaNimistäJaHinnoista)   
                    except IOError:
                        print("IOError: Macrolist")



                ListaNimistäJaHinnoista.sort()  
                ListaNimistäJaHinnoista = cleanlist(ListaNimistäJaHinnoista)   
                printlist(ListaNimistäJaHinnoista) 
                
                print("\n\n\nNow this prints the whole list\n\n\n")                          
                ListaNimistäJaHinnoista = paskalista.searchRed()   
                ListaNimistäJaHinnoista = sorted(ListaNimistäJaHinnoista)
                ListaNimistäJaHinnoista = cleanlist(ListaNimistäJaHinnoista)
                printlist(ListaNimistäJaHinnoista)      
                #looppi = False                
            except ValueError:
                ErrorTries = 1
                print("ValueError: Main function")
                
            except IOError:
                ErrorTries = 1
                print("\nIOError: Main function\nProbably Internet 11001")
                print(r"This program expects file to be at C:\Users\stocksites.txt")
                print("Site can be either yahoo.finance or Nordnet -link")
                print("The lines in file are expected to be in format:\n")
                print(r"https://finance.yahoo.com/quote/NOKIA.HE/,3")



            except http.client.IncompleteRead:
                ErrorTries = 1
                print("Incomplete Read")
                looppi = True
            print("\n\n")      
            
            #delete this
            ErrorTries = 1
            if looppi == True:
                pass
            else:
                print("Program  ends now.")
                #inputToExit = input("Press X to exit")
                break
        
    
main()

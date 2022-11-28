# Author: Daan
# Date: 28.11.2022

import imaplib
import pandas as pd

def get_creds():
    # Funtion to retrieve the credits from json file:
    creds = pd.read_json("creds.json")
    return creds

def login(creds):
    # Funtion to login to the email server:
    imap  = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(creds["user1"]["user"], creds["user1"]["16pass"])
    return imap

def filter_inbox(imap, sender):
    # Funtion to search for mails from sender:
    imap.select("Inbox")
    status, messages = imap.search(None, "X-GM-RAW", "from:%s" % sender)
    print("We found %s mails from %s." % (get_len(messages), sender))
    imap.close()
       
def add_label(imap, search):
    imap.select("Inbox")
    result, data = imap.search(None, "X-GM-RAW", "from:%s" % search)
    print("We found %s mails from %s." % (get_len(data), search))
    new_label = input("What label would you like to assign to them? {Enter 'x' to cancel}\n>").replace(" ", "")
    if new_label != "x":
        for id in data[0].split():
            imap.store(id, "+X-GM-LABELS", new_label)
        print("Labels were succesfully assigned.")
    else:
        print("No labels were assigned.")    
    
    imap.close()
     
def get_len(data):
    # Function to get n of searched mail:
    x = str(data).split(" ")
    if x == ["[b'']"]:
        n = 0
    else:      
        n = len(x)
    return n

def main():
    # Funtion to run main loop of the script:
    creds = get_creds()
    mImap = login(creds)
    
    running = True
    while running:
        mode = input("\nWhat would you like to do?: \n1. Count all mail from a sender.\n2. Add labels to mail.\n3. Quit.\n> ")
        if str(mode) == "1":
            sender = input("\nFrom what sender would you like to count email?\n> ").replace(" ", "")
            filter_inbox(mImap, sender)
        elif str(mode) == "2":
            search = input("\nFrom what sender would you like to label email?\n>").replace(" ", "")
            add_label(mImap, search)                
        elif str(mode) == "3":
            running = False
        else:
            print("That is not a valid option...")
    
    mImap.logout()
       
main()
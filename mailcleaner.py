import imaplib
import pandas as pd

def get_creds():
    
    creds = pd.read_json("creds.json")
    return creds

def login(creds):
    imap  = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(creds["user1"]["user"], creds["user1"]["16pass"])
    return imap

def filter_inbox(imap, sender):
    imap.select("Inbox")
    status, messages = imap.search(None, "X-GM-RAW", "from:%s" % sender)
    n = len(str(messages).split(" "))
    print("We found %s mails from %s." % (n, sender))
    imap.close()    


def main():
    creds = get_creds()
    mImap = login(creds)
    
    running = True
    while running:
        mode = input("\nWhat would you like to do?: \n1. Select all mail from a sender.\n2. Quit.\n> ")
        if str(mode) == "1":
            sender = input("\nFrom what sender would you like to count email?\n> ")
            filter_inbox(mImap, sender)
        elif str(mode) == "2":
            running = False
        else:
            print("That is not a valid option...")
    
    mImap.logout()
       
main()
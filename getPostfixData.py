import os

def getMailData():

    directoryData = '/home/'+os.getenv('USERNAME')+'/mbox'

    f = open(directoryData)

    dataFile = f.readlines()

    listOfMails = []
    alreadyStart = False
    
    for item in dataFile:

        currentItem = item.split()

        if len(currentItem) == 7 and currentItem[0] == 'From':

            if alreadyStart:
                listOfMails.append(mail)

            if not alreadyStart:
                alreadyStart = True

            mail = []
        
        mail.append(item)

    listOfMails.append(mail)

    cleanedMails = []

    for i in range(len(listOfMails)):
        receiver = listOfMails[i][getIndexMail("Delivered-To:",listOfMails[i])].strip().replace("Delivered-To: ","")
        sender= listOfMails[i][getIndexMail("From:",listOfMails[i])].strip().replace("From: ","")
        date = listOfMails[i][getIndexMail("Date:",listOfMails[i])].strip().replace("Date: ","")
        subject=listOfMails[i][getIndexMail("Subject:",listOfMails[i])].strip().replace("Subject: ","")

        getBodyIndex = getIndexMail("X-UID:",listOfMails[i])+1

        body = []

        for j in range(getBodyIndex,len(listOfMails[i])):
            body.append(listOfMails[i][j])

        mailData = [receiver,sender,date,subject,body]
        cleanedMails.append(mailData)

    return cleanedMails

def getIndexMail(toFind,mailData):

    for i in range(len(mailData)):
        
        checkContent = mailData[i].split()[0]

        if checkContent == toFind:
            return i

if __name__ == '__main__':
    result = getMailData()

    print(result)
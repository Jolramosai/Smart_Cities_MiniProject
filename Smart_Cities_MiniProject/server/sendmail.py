import yagmail
from realtime_database import get_contacts

def sendmail(mymail,mypassword,sendto,message,subject,image_path):
    
    try:
        message = [message,image_path]
        yag = yagmail.SMTP(mymail,mypassword)

        yag.send(to=sendto,subject=subject,contents=message)
    
    except:
        print("Couldn't send mail")

def sendmails(mymail,mypassword,messageFunc,subject,image_path):
    contacts = get_contacts()
    print(contacts)

    for name,contact in contacts:
        message = messageFunc(name)
        sendmail(mymail,mypassword,contact,message,subject,image_path)
    
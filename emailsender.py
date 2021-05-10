import smtplib  

def emailsender( username, password, tolist, fromaddr, subject, body, server):
    server = smtplib.SMTP(server)  
    server.starttls()  
    server.login(username,password)
    for to in tolist:
        msg = """\
From: %s
To: %s
Subject: %s

%s
""" % (fromaddr, to, subject, body)
        print "msg:\n", msg
        server.sendmail(fromaddr, to, msg)  
    server.quit()

if __name__ == '__main__':
    if 1:
        fromaddr = 'varanda.m@emssatcom.com'  
        server = 'SAT-EX07.ems-tcanada.com' 
        username = 'varanda'  
        password = 'xxxxxxx'
    else:
        fromaddr = 'mv_email@yahoo.com'  
        server = 'smtp.mail.yahoo.com:587' 
        username = 'uuuuuuu'  
        password = 'ppppppp'
    tolist  = ["mv_email@yahoo.com","varanda.m@emssatcom.com"]  

    body = "Worked fine.\n\nbye"
    subject = "email test EMS"

    emailsender( username, password, tolist, fromaddr, subject, body, server )
    print "Done\n"

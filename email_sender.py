import smtplib as s
ob=s.SMTP('smtp.gmail.com',587)
ob.ehlo()
ob.starttls()
ob.login('saikrishna64999@gmail.com','password')
subject="test python"
body="I Love Python"
massage="subject:{}\n\n{}".format(subject,body)
listadd=['saikrishna64888@gmail.com','saikrishna64666@gmail.com','saikrishna649993@gmail.com']
ob.sendmail('saikrishna64999@gmail.com',listadd,massage)
print("send mail")
ob.quit()

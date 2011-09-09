import _mysql, time, smtplib, email

# Import the email modules we'll need
# from email.mime.text import MIMEText
from email.MIMEText import MIMEText

db=_mysql.connect(host="192.168.1.10",user="thermd", passwd="skruvmejsel23",db="thermd")

db.query("""SELECT max(reading_ts) as MaxDate FROM readings""")
r = db.store_result()

while 1:
    row = r.fetch_row()
    if not row: break
    maxdate = row[0][0]

print maxdate

print "Calculate difference between maxdate in db and current datetime"
#print "Calculate difference between two times (12 hour format) of a day:"
## time1 = raw_input("Enter first time (format 11:25:00AM or 03:15:30PM): ")
# pick some plausible date
# timeString1 = "03/06/05 " + time1
# create a time tuple from this time string format eg. 03/06/05 11:22:00AM
# timeTuple1 = time.strptime(timeString1, "%m/%d/%y %I:%M:%S%p")
timeTuple1 = time.strptime(maxdate, "%Y-%m-%d %H:%M:%S")
# timeTupleNow = time.now()

# time_difference = time.mktime(timeTupleNow) - time.mktime(timeTuple1)
time_difference = time.time() - time.mktime(timeTuple1)
#print type(time_difference)  # test <type 'float'>
print "Time difference = %d seconds" % int(time_difference)
print "Time difference = %0.1f minutes" % (time_difference/60.0)
print "Time difference = %0.2f hours" % (time_difference/(60.0*60))

mindiff = (time_difference/60.0)

if mindiff > 11:
	print "%f minutes since last database update, sending email..." % mindiff
	smtpserver = 'smtp.glocalnet.net'
	#smtpserver = '192.168.1.10'
	AUTHREQUIRED = 1 # if you need to use SMTP AUTH set to 1
	smtpuser = 'goransander12@glocalnet.net'  # for SMTP AUTH, set SMTP username here
	# smtpuser = 'goran'
	smtppass = 'MgT5O1Kg'  # for SMTP AUTH, set SMTP password here
	# smtppass = 'fnuttegurra'

	# RECIPIENTS = ['goran@goranna.se']
	RECIPIENTS = ['goran.sander@gmail.com']
	SENDER = 'goran@goranna.se'
	# SENDER = 'goran.sander@glocalnet.net'

	# Open a plain text file for reading.  For this example, assume that
	# the text file contains only ASCII characters.
	fp = open('/home/goran/project/thermd_mon/mssg.txt', 'rb')
	# Create a text/plain message
	msg = MIMEText(fp.read())
	fp.close()

	# me == the sender's email address
	# you == the recipient's email address
	msg['Subject'] = 'URGENT: thermd database values overdue - 1-wire readings'
	msg['From'] = 'goran@goranna.se'
	msg['To'] = 'goran.sander@gmail.com'



	session = smtplib.SMTP(smtpserver)
	if AUTHREQUIRED:
		session.login(smtpuser, smtppass)
	# smtpresult = session.sendmail(SENDER, RECIPIENTS, mssg)
	smtpresult = session.sendmail(SENDER, RECIPIENTS, msg.as_string())


	if smtpresult:
		errstr = ""
		for recip in smtpresult.keys():
			errstr = """Could not delivery mail to: %s

	Server said: %s
	%s

	%s""" % (recip, smtpresult[recip][0], smtpresult[recip][1], errstr) 
		raise smtplib.SMTPException, errstr

	session.quit()
	print "Done."
else:
	print "%f minutes since last database update, no reason to send an email." % mindiff
	


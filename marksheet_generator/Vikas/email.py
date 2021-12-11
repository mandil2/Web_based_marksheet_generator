def email_generator():
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    import csv
    import os

    fromaddr = "cs384pythontest@gmail.com"
    responses_path = r'media/responses.csv'
    if not os.path.exists(responses_path):
        print('ERROR')
        return

    responses_dict = {}
    with open(responses_path, 'r') as file:
        reader = csv.reader(file)
        # j = 0
        for row in reader:
            if row[6] != 'Roll Number':
                responses_dict[(row[6]).upper()] = [row[1], row[4]]
            else:
                continue
            toaddr1 = responses_dict[(row[6]).upper()][0]
            toaddr2 = responses_dict[(row[6]).upper()][1]

            # instance of MIMEMultipart
            msg = MIMEMultipart()

            # sender's email address
            msg['From'] = fromaddr

            # receivers email address and webmail address
            msg['To'] = toaddr1
            msg['To'] = toaddr2
            # email subject
            msg['Subject'] = "CS384 2021 - Marks - with Negative Marking"

            # body of email
            body = "Dear Student,EndSem Exam marks are attached for reference. +5 Correct, -1 for wrong."

            # attach the body with the msg instance
            msg.attach(MIMEText(body, 'plain'))

            # open the file to be sent i.e. RollNo.xlsx
            filename = r"Vikas/marksheets/"+(row[6]).upper()+'.xlsx'
            if os.path.exists(filename):
                attachment = open(filename, "rb")
            else:
                print('No such file'+filename+'exists')
                continue

            # instance of MIMEBase and named as x
            x = MIMEBase('application', 'octet-stream')

            # To change the payload into encoded form
            x.set_payload((attachment).read())

            # encode into base64
            encoders.encode_base64(x)

            x.add_header('Content-Disposition',
                         "attachment; filename= %s" % filename)

            # attach the instance 'x' to instance 'msg'
            msg.attach(x)

            # creating SMTP session
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()

            # Authentication
            s.login(fromaddr, "cs384python")

            # Converts the Multipart msg into a string
            text = msg.as_string()

            # sending the mail
            s.sendmail(fromaddr, toaddr1, text)
            s.sendmail(fromaddr, toaddr2, text)

            print("DONE")
            s.quit()
            # j += 1
            # if j == 10:
            #     break

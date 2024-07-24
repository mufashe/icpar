import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.conf import settings
from django.core.mail import get_connection, EmailMessage
from django.shortcuts import render


def sendEmailNotification(request):
    if request.method == "POST":
        with get_connection(
                host=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                username=settings.EMAIL_HOST_USER,
                password=settings.EMAIL_HOST_PASSWORD,
                use_tls=settings.EMAIL_USE_TLS) as connection:
            subject = request.POST.get("subject")
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST.get("email"), ]
            message = request.POST.get("message")
            EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()

    return render(request, 'icparsa/notification/email/expiration/expiration.html')


def sendEmail(request):
    smtp_server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    smtp_server.starttls()

    senderEmail = 'mufasheonline@gmail.com'
    passWord = 'jemy yorr xgnp ihdk'

    msg = MIMEMultipart()
    msg['From'] = senderEmail
    msg['To'] = 'theogene.ndacyayisenga@icparwanda.com'
    msg['Subject'] = 'Testing ICPARS Notification'

    body = 'Testing send email to notify the expiration of contract'
    msg.attach(MIMEText(body, 'plain'))

    try:
        smtp_server.login(senderEmail, passWord)
        print("Login successful")
        smtp_server.send_message(msg)
        smtp_server.quit()
        message = 'Email Sent successfully'
    except Exception as e:
        print(f"Exception: {str(e)}")
        message = f"Failed to send email : {str(e)}"
        print("Login Failed")

    return render(request, 'icparsa/notification/email/expiration/expiration.html', {'message': message})

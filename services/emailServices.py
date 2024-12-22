import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def sendAccountCreationEmail(recipientEmail, userId, userName, created_at):
    """
    Sends an email with the account creation details.

    :param recipientEmail: Recipient's email address
    :param userId: Unique ID of the user
    :param userName: Username of the user
    :param createdAt: Account creation timestamp
    """
    smtpServer = "smtp.gmail.com"
    smtpPort = 587
    senderEmail = "noreply.iotstudio@gmail.com" 
    senderPassword = "bqao clyg pkfx lacp"  

    subject = "Account Created Successfully🎉🎉 - IoT Studio"
    body = f"""
    Dear {userName},

    Welcome to IoT Studio! Your account has been created successfully. 
    Here are your account details:

    - User ID: {userId}
    - Username: {userName}
    - Created At: {created_at}

    If you have any questions, feel free to contact us.

    Best Regards,
    IoT Studio Team
    ✨✨✨
    """

    try:
        msg = MIMEMultipart()
        msg["From"] = senderEmail
        msg["To"] = recipientEmail
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(smtpServer, smtpPort) as server:
            server.starttls() 
            server.login(senderEmail, senderPassword) 
            server.sendmail(senderEmail, recipientEmail, msg.as_string())  

        print(f"Email sent successfully to {recipientEmail}!")

    except Exception as e:
        print(f"Failed to send email: {e}")

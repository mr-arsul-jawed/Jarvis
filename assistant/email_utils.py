import imaplib
import email
from email.header import decode_header
from .speech import speak, takecommand

import os

def check_new_email():
    username = os.getenv('EMAIL_USER')
    password = os.getenv('EMAIL_PASS')

    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(username, password)
    imap.select("inbox")

    status, messages = imap.search(None, 'UNSEEN')
    mail_ids = messages[0].split()

    if len(mail_ids) == 0:
        imap.close()
        imap.logout()
        return None

    latest_email_id = mail_ids[-1]
    status, msg_data = imap.fetch(latest_email_id, "(RFC822)")

    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")

            from_ = msg.get("From")

            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))

                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        body = part.get_payload(decode=True).decode()
                        break
            else:
                body = msg.get_payload(decode=True).decode()

            imap.close()
            imap.logout()

            return {
                "subject": subject,
                "from": from_,
                "body": body
            }
    imap.close()
    imap.logout()
    return None

def get_user_confirmation(prompt):
    speak(prompt)
    print(f"Prompt: {prompt}")
    for _ in range(2):
        response = takecommand()
        if any(word in response for word in ["yes", "sure", "okay", "read full email", "yes please", "yes, please"]):
            return True
        elif any(word in response for word in ["no", "not now", "later", "skip"]):
            return False
        else:
            speak("I didn’t catch that. Could you please repeat?")
    speak("I'll skip it for now.")
    return False

def check_notifications():
    email_data = check_new_email()
    if email_data is None:
        speak("You have no new emails.")
        return

    if get_user_confirmation(f"You have a new email from {email_data['from']}. Would you like me to read the subject?"):
        speak(f"The subject is: {email_data['subject']}")
        if get_user_confirmation("Would you like me to read the body?"):
            speak(email_data['body'])
        else:
            speak("Okay, I won't read the body.")
    else:
        speak("Okay, I won't read it.")

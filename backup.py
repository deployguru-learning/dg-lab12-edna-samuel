import os
import shutil
from datetime import datetime
import requests
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def backup_files(source_dir="/var/www/html", dest_dir="/opt/backups"):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_folder = os.path.join(dest_dir, timestamp)

    try:
        os.makedirs(backup_folder)
        for item in os.listdir(source_dir):
            source_item = os.path.join(source_dir, item)
            dest_item = os.path.join(backup_folder, item)
            if os.path.isdir(source_item):
                shutil.copytree(source_item, dest_item)
            else:
                shutil.copy2(source_item, dest_item)
        
        send_email(backup_folder)
        send_slack(backup_folder)  

    except Exception as e:
        print(f"Error: {e}")

def send_slack(backup_folder):
    webhook_url = 'https://hooks.slack.com/services/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'
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d %H:%M:%S") + ' UTC'  
    notification = {
        "Notification_by": "Edna Samuel",
        "Backup_path": backup_folder,
        "Backup_time": formatted_date,
        "No. of files": count_files(backup_folder)  
    }
    
    message_payload = {"text": f"```{json.dumps(notification, indent=4)}\n```"}
    response = requests.post(webhook_url, json=message_payload)
    
    if response.status_code == 200:
        print("Slack notification sent successfully")
    else:
        print(f"Failed to send slack notification, status code: {response.status_code}")
        
def send_email(backup_folder):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'vedna8221@gmail.com'
    smtp_password = 'clvt uilr inpb lvxl'
    from_email = 'vedna8221@gmail.com'
    to_emails = 'vedna8221@gmail.com, felix@deployguru.com'
    subject = 'Backup Notification'
    formatted_date = datetime.now().strftime("%a %Y-%m-%d %H:%M:%S") + ' UTC'
    
    # Creating CSV content with column titles
    csv_content = "Status,Backup Time,Backup Path,No. of Files\n"
    csv_content += f"Backup Completed,{formatted_date},{backup_folder},{count_files(backup_folder)}\n"
    
    # The Email body
    body = f"The Backup succefully completed.\n\n"
    
    # Create  MIME multipart message
    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_emails 
    message['Subject'] = subject
    
    # Attach email body
    message.attach(MIMEText(body, 'plain'))
    
    # Attach  CSV file
    filename = os.path.basename(backup_folder) + '.csv'
    attachment = MIMEBase('application', 'octet-stream')
    attachment.set_payload(csv_content.encode())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', f'attachment; filename={filename}')
    message.attach(attachment)
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as smtp:
            smtp.starttls()
            smtp.login(smtp_username, smtp_password)
            smtp.sendmail(from_email, to_emails.split(','), message.as_string())
            print("Email sent")
    except Exception as error:
            print(f'Something went wrong: {error}')


def count_files(backup_folder):
    total_files = sum(1 for file in os.listdir(backup_folder) 
    if os.path.isfile(os.path.join(backup_folder, file)))
    return total_files

backup_folder_path = '/opt/backups'

# Call the count_files function to retrieve the number of files
num_files = count_files(backup_folder_path)

# Print the number of files
print(f'Number of files in the backups folder: {num_files}')

if __name__ == '__main__':
    backup_files()

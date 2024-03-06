# Automated Backup and Notification Script

## Overview

This Python script automates the backup process of a specified directory (/var/www/html ) to a backup folder(/opt/backups/) and sends email and Slack notifications upon completion of the backup.

## Features 
- The script is designed to run on a schedule (e.g., daily) using cron

- **Automated Backup:** 
Automatically creates a timestamped folder in the backup directory and copies files from the source directory to the backup folder.

- **Email Notification:** 
Sends an email notification to specified recipients with details of the backup, including the number of files backed up.
The script is designed to be run as a cron job, sending an email notification when the backup process completes. T

- **Slack Notification:** Sends a notification to a specified Slack channel using a webhook URL.
- **Cron Job Scheduling:** The script can be run on a schedule (e.g., daily, weekly) by setting up a cron job with the provided crontab

## Usage

1. **Setup Configuration:**
   - Ensure Python is installed on your system.
   - Configure the source directory (`source_dir`) and destination directory (`dest_dir`) in the script as needed.

2. **Dependencies:**
   - Ensure the required Python libraries are installed: `requests`.
   You can install it via pip by running `pip install requests` in terminal.
   
3. **Configuration:**
   - Configure email and Slack settings:
     - Set up a Gmail account and enable less secure apps.
     - Obtain a Slack webhook URL.
     
4. **Running the Script:**
   - Run the script using the Python interpreter:
     ```bash
     python backup_script.py
     ```

## Customization

- Customize the email subject, message body, and recipients according to your requirements.
- Modify the Slack webhook URL to point to your Slack channel.


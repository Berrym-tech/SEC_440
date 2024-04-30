#!/bin/bash

# Check if Veeam is installed
if ! command -v veeam &> /dev/null
then
    echo "Veeam Agent for Linux not found, installing..."
    # Add the Veeam repository and key
    wget -O- http://repository.veeam.com/keys/veeam_software.pub | gpg --dearmor | tee /usr/share/keyrings/veeam-archive-keyring.gpg > /dev/null
    echo "deb [signed-by=/usr/share/keyrings/veeam-archive-keyring.gpg] http://repository.veeam.com/backup/linux/agent/debian/ xUbuntu_$(lsb_release -rs) main" | tee /etc/apt/sources.list.d/veeam.list
    # Update the repo and install Veeam
    apt-get update
    apt-get install veeam -y
fi

# Configure the backup job (This part may need to be customized based on specific backup requirements)
JOB_NAME="XubuntuVMBackup"
REPOSITORY_PATH="/mnt/backup_repository"  # Define your backup repository path
BACKUP_LEVEL="Incremental"  # Backup type: Incremental, Full

# Check if a job with the specified name already exists
if ! veeamconfig job list | grep -q "$JOB_NAME"
then
    echo "Creating new backup job..."
    # Create a new backup job
    veeamconfig job create --name "$JOB_NAME" --repo "$REPOSITORY_PATH" --isincremental $BACKUP_LEVEL
else
    echo "Backup job already exists."
fi

# Schedule the backup using cron
CRON_JOB="0 2 * * * /usr/bin/veeamconfig job start --name $JOB_NAME"
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

# Display final confirmation and next steps
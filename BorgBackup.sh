#!/bin/bash

# Configuration
REPO="/home/maxwell/Desktop/Backups"
SOURCE="/home/maxwell/"
export BORG_PASSPHRASE='your_secure_passphrase'

# Initialize the repository if not already done
if ! borg list $REPO &> /dev/null; then
    echo "Initializing Borg repository..."
    borg init --encryption=repokey-blake2 $REPO
else
    echo "Repository already initialized."
fi

# Create a backup
echo "Starting backup..."
borg create --verbose --filter AME --list --stats --compression lz4 --exclude-caches \
            $REPO::'{hostname}-{now:%Y-%m-%d_%H:%M:%S}' $SOURCE

# Pruning settings - keeping last 7 daily, 4 weekly, and 6 monthly archives
echo "Pruning repository..."
borg prune --list --prefix '{hostname}-' --show-rc --keep-daily=7 --keep-weekly=4 --keep-monthly=6 $REPO

# Check for errors
exit_status=$?
if [ $exit_status -eq 0 ]; then
    echo "Backup and Prune finished successfully"
elif [ $exit_status -eq 1 ]; then
    echo "Backup and/or Prune finished with warnings"
else
    echo "Backup and/or Prune finished with errors"
fi
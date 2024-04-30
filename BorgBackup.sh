#!/bin/bash

# Set the location of the Borg repository
REPO="/home/maxwell/Desktop/Backups"

# Set the backup source directory
SOURCE="/home/maxwell/Desktop/Happy Files"

# Export Borg passphrase in environment variable (replace 'your_borg_passphrase' with your actual passphrase)
export BORG_PASSPHRASE='Backup'

# Initialize the repository if it does not exist
if [ ! -d "$REPO" ]; then
    echo "Initializing Borg repository..."
    borg init --encryption=repokey-blake2 $REPO
fi

# Create a new backup
echo "Starting backup..."
borg create --verbose --filter AME --list --stats --show-rc --compression lz4 --exclude-caches \
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
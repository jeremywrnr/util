#!/bin/bash

# Script to force macOS to resync time with NTP servers
# This mimics the "uncheck/recheck" process you're doing manually

# Force sync with Apple's time servers
sudo sntp -sS time.apple.com

# Alternative: Force sync using built-in NTP
# sudo ntpdate -s time.apple.com

# Log the sync attempt
echo "$(date): Time sync attempted" >> ~/Library/Logs/time_sync.log

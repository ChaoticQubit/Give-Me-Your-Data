#!/bin/bash

PLIST_NAME="com.chaoticqubit.githubcommithistory.plist"
PLIST_SRC="$(pwd)/$PLIST_NAME"
PLIST_DEST="$HOME/Library/LaunchAgents/$PLIST_NAME"

# Ensure the destination directory exists
mkdir -p "$HOME/Library/LaunchAgents"

# Unload existing service if it exists (suppress errors if not loaded)
launchctl unload "$PLIST_DEST" 2>/dev/null

# Copy the new plist
cp "$PLIST_SRC" "$PLIST_DEST"

# Load the new service
launchctl load "$PLIST_DEST"

echo "Service installed and loaded."
echo "Check status with: launchctl list | grep githubcommithistory"
echo "Check logs at: /tmp/github_commit_history.log"

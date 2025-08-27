#!/bin/bash
set -e

# ========= CONFIG =========
#FTP_HOST="ftp.clusterXXX.hosting.ovh.net"   # replace with your OVH FTP host
#FTP_USER="your-ftp-username"                # replace with your OVH FTP username
#FTP_PASS="your-ftp-password"                # replace with your OVH FTP password
REMOTE_DIR="/www"                           # usually /www on OVH
# ==========================

echo "👉 Building Jekyll site..."
bundle exec jekyll build

echo "👉 Uploading to OVH ($REMOTE_DIR)..."
lftp -u "$FTP_USER","$FTP_PASS" "$FTP_HOST" <<EOF
mirror -R --delete _site $REMOTE_DIR
quit
EOF

echo "✅ Deploy finished!"


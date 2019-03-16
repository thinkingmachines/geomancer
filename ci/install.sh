#!/bin/bash

# Use latest sqlite3 from the disco distribution
echo "deb http://archive.ubuntu.com/ubuntu disco main" >> /etc/apt/sources.list
cat > /etc/apt/preferences <<EOF
Package: sqlite3
Pin: release n=sqlite3
Pin-Priority: 900
EOF
apt-get -qq update
apt-get -y --allow-unauthenticated install sqlite3 libsqlite3-mod-spatialite


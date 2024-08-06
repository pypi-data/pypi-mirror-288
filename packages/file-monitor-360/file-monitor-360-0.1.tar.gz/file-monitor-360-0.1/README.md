# Saferhub Client Setup Guide

This guide provides step-by-step instructions to set up Saferhub Server on Ubuntu.

## Step 1: Switch to root user

sudo su

## Step 2: Install evtch

### 2.1 Copy evtch files in Ubuntu

Copy `evtch.tgz` to your Ubuntu server.

### 2.2 Update package list

apt-get update

### 2.3 Extract evtch.tgz and navigate to directory evtch

tar -xzf evtch.tgz
cd evtch

### 2.4 Run install.sh script

sh install.sh

### 2.5 Start evtch

./evtch

## Step 3: Install PIP

sudo apt-get install python3 python3-pip

## Step 4: Install Node.js and NPM

### 4.1 Install Node.js and NPM

sudo apt install nodejs npm

### 4.2 Check Node.js version

node -v

### 4.3 Check NPM version

npm -v

## Step 5: Install PM2

sudo npm install -g pm2

## Step 6: Run Saferhub Python script using PM2

### 6.1 Extract saferhub_client.zip file and navigate to the extracted folder

unzip saferhub_client.zip
cd saferhub_client

### 6.2 Install required Python packages

pip install websocket-client
pip install watchdog

### 6.3 Start Saferhub script using PM2

pm2 start ecosystem.config.json

## Step 7: Install AnyDesk

### 7.1 Download AnyDesk package

wget https://download.anydesk.com/linux/anydesk_6.3.2-1_amd64.deb

### 7.2 Install AnyDesk package

sudo dpkg -i anydesk_6.3.2-1_amd64.deb

### 7.3 Resolve dependencies (if libgtkglext1 error occurs)

sudo apt-get update
sudo apt-get upgrade
sudo apt --fix-broken install
sudo apt-get install libcanberra-gtk-module
sudo dpkg -i anydesk_6.3.2-1_amd64.deb

### 7.4 For anydesk wayland error (allow_display):

sudo nano /etc/gdm3/custom.conf
### Uncomment the following 
 AutomaticLoginEnable
 AutomaticLogin
 WaylandEnable=false 
save the file


### 8 Auto RUN PM2 On startup

sudo pm2 startup systemd -u <your_user> --hp /home/<your_user>
sudo env PATH=$PATH:/usr/bin /usr/local/lib/node_modules/pm2/bin/pm2 startup systemd -u <your_user> --hp /home/<your_user>
pm2 save

### 9 Auto RUN evtch on startup

sudo chmod +x /path/to/install.sh
sudo chmod +x /path/to/evtch
crontab -e
Put the following commands in crontab and save the file
@reboot /path/to/install.sh
@reboot /path/to/evtch



# File Watcher

This package includes scripts for file watching and monitoring.
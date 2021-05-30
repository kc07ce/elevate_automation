#!/bin/bash

SCRIPT=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPTPATH=$(dirname "$SCRIPT")


echo 'Installing packages and chromedriver'
sudo cp $SCRIPTPATH/chromedriver /usr/bin/
pip install -U selenium

echo '------------------------------------------'

rm automate.conf > automate.log
echo 'Enter elevate email:'
read username
echo 'Enter elevate password:'
read password

echo $username >> automate.conf
echo $password >> automate.conf

echo 'clockin hour in 24hr format'
read ih
echo 'clockin minute'
read im
echo 'clockout hour in 24hr format'
read oh
echo clockout minute
read om

#write out current crontab
crontab -r >> automate.log 2>&1
crontab -l > mycron
#echo new cron into cron file
echo "$im $ih * * * /usr/bin/python $SCRIPTPATH/script.py >> $SCRIPTPATH/automate.log 2>&1" >> mycron
echo "$om $oh * * * /usr/bin/python $SCRIPTPATH/script.py >> $SCRIPTPATH/automate.log 2>&1" >> mycron
#install new cron file
crontab mycron
rm mycron
echo 'Done'


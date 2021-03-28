#!/bin/bash
# 
python /opt/uSvxCard/callconfignum.py --dept $1 --call $2 --band $3
sleep 2
IDok=$(find /opt/Analog_Bridge/ -mindepth 1 -maxdepth 1 -name "*" -mmin -1)
if [ "$IDok" ] ; then
echo "Restart Spotnik"
reboot
else
echo "Restart svxlink"
/etc/spotnik/restart
fi

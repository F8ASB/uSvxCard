test1=$(grep -c "\#\* \* \* \* \* root pgrep svxlink" /etc/crontab)
 echo "$test1"

  if [ $test1 = 0 ]
  then
   echo "Ajout du #"
   sed -i '/root pgrep/ s/^/#/' /etc/crontab && service cron restart && pkill svxlink
 else 
#  then
   echo "Enleve le #"
   sed -i '/root pgrep/s/^#//' /etc/crontab && service cron restart && /etc/spotnik/restart
fi

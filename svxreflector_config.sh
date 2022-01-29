############################
#Configuration svxreflector#
#        F8ASB 2022        #
############################

whiptail --title "INFORMATION:" --msgbox "Ce programme permet de configurer un serveur regional avec svxreflector.                                                                             Team F4ICR/F5SWB/F8ASB" 15 60

while : ; do

choix=$(whiptail --title "Choisir votre action" --radiolist \
"Que voulez vous faire ?" 15 50 4 \
"1" "CONFIGURATION de SvxReflector " ON \
"2" "ACTIVER SvxReflector au demarrage " OFF 3>&1 1>&2 2>&3)

exitstatus=$?

if [ $exitstatus = 0 ]; then
    echo "Your chosen option:" $choix
else
    echo "You chose Cancel."; break;
fi

choix_port()
{
port=$(whiptail --inputbox "Entrez le Port: ?" 8 39 4500 --title "Frequence TX" 3>&1 1>&2 2>&3)

exitstatus=$?

if [ $exitstatus = 0 ]; then
    echo "Port: " $port
    choix_password
else
    echo "Annulation"; break;
fi
}

choix_password()
{
password=$(whiptail --inputbox "Votre mot de passe ?" 8 39 1234567 --title "Entrez votre mot de passe:" 3>&1 1>&2 2>&3)

exitstatus=$?

if [ $exitstatus = 0 ]; then
    echo "Mot de passe " $password
    configuration_save
else
    echo "Annulation"; break;
fi

}

configuration_save()
{
#telechargement du fichier svxreflector
wget -N https://raw.githubusercontent.com/F8ASB/uSvxCard/main/svxreflector.conf -P /etc/spotnik/

#definition du port
sed -i 's/LISTEN_PORT=XXXX/LISTEN_PORT='$port'/g' /etc/spotnik/svxreflector.conf > /dev/null 2>&1

#definition du mot de passe
sed -i 's/AUTH_KEY=XXXXX/AUTH_KEY='$password'/g' /etc/spotnik/svxreflector.conf > /dev/null 2>&1
}

activer_demarrage()
{
#ajout de la commande au demarrage
sed -i '/make start/a \sleep 2' /etc/rc.local
sed -i '/make start/a \svxreflector --config=/etc/spotnik/svxreflector.conf --daemon --logfile=/tmp/svxreflector.log' /etc/rc.local
sed -i '/make start/a \#DEMARRAGE SVXREFLECTOR' /etc/rc.local
sed -i '/make start/a \ ' /etc/rc.local
}

case $choix in

1) 
choix_port
;;

2) 
activer_demarrage
;;

esac

done
exit 0

#!/bin/sh

############################
#Configuration svxreflector#
#        F8ASB 2022        #
############################

whiptail --title "INFORMATION:" --msgbox "Ce programme permet de configurer un serveur regional avec svxreflector.                                                                             Team F4ICR/F5SWB/F8ASB" 15 60

while : ; do

choix=$(whiptail --title "Choisir votre action" --radiolist \
"Que voulez vous faire ?" 15 50 4 \
"1" "CONFIGURATION de SvxReflector " ON \
"2" "CONFIGURATION de Salon régional " OFF \
"3" "ACTIVER SvxReflector au demarrage " OFF 3>&1 1>&2 2>&3)

exitstatus=$?

if [ $exitstatus = 0 ]; then
    echo "Your chosen option:" $choix
else
    echo "You chose Cancel."; break;
fi

choix_port()
{
port=$(whiptail --inputbox "Entrez le Port: ?" 8 39 5300 --title "Frequence TX" 3>&1 1>&2 2>&3)

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

ip_adresse=$(curl ifconfig.me);

ajout de la commande au demarrage
sed -i '/make start/a \sleep 2' /etc/rc.local
sed -i '/make start/a \svxreflector --config=/etc/spotnik/svxreflector.conf --daemon --logfile=/tmp/svxreflector.log' /etc/rc.local
sed -i '/make start/a \#DEMARRAGE SVXREFLECTOR' /etc/rc.local
sed -i '/make start/a \ ' /etc/rc.local

whiptail --title "INFORMATION SERVEUR REGIONAL:" --msgbox "Informations à transmettre aux utilisateurs:

-Adresse IP:$ip_adresse 
-Port:$port
-Mot de passe:$password


Un redemarrage sera necessaire pour la prise en compte de la configuration


Cliquer sur Ok pour continuer..." 20 60
}

choix_adresse_salon()
{
host=$(whiptail --inputbox "Entrez l'adresse du serveur: ?" 8 39 xxxxxxxxxx --title "Adresse du serveur:" 3>&1 1>&2 2>&3)

exitstatus=$?

if [ $exitstatus = 0 ]; then
    echo "Port: " $host
    choix_auth_salon
else
    echo "Annulation"; break;
fi
}

choix_auth_salon()
{
password2=$(whiptail --inputbox "Entrez le mot de passe du serveur: ?" 8 39 xxxxxxx --title "Mot de passe du salon:" 3>&1 1>&2 2>&3)

exitstatus=$?

if [ $exitstatus = 0 ]; then
    echo "Port: " $password2
    choix_port_salon
else
    echo "Annulation"; break;
fi
}

choix_port_salon()
{
port2=$(whiptail --inputbox "Entrez le Port: ?" 8 39 5300 --title "Port du salon" 3>&1 1>&2 2>&3)

exitstatus=$?

if [ $exitstatus = 0 ]; then
    echo "Port: " $port2
    ecrire_config_salon
else
    echo "Annulation"; break;
fi
}

ecrire_config_salon()
{

#telechargement du fichier restart.reg
wget -N https://raw.githubusercontent.com/F8ASB/uSvxCard/main/restart.reg -P /etc/spotnik/
sleep 2
#remplacement du fichier restar.reg par les valeurs données
sed -i 's/HOST=XXXXXXXXXXXXXX/HOST='$host'/g' /etc/spotnik/restart.reg 
sed -i 's/AUTH_KEY=XXXXX/AUTH_KEY='$password2'/g' /etc/spotnik/restart.reg 
sed -i 's/PORT=5300/PORT='$port2'/g' /etc/spotnik/restart.reg 

whiptail --title "INFORMATION SALON REGIONAL:" --msgbox "Votre salon régional est maintenant configuré


Cliquer sur Ok pour continuer..." 10 60
}


case $choix in

1) 
choix_port
;;

2) 
choix_adresse_salon
;;

3) 
activer_demarrage
;;

esac

done
exit 0


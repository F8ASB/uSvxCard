#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# F8ASB 2020

import configparser, os
import json
import sys
import getopt

from configparser import ConfigParser

svxlinkcfg='/etc/spotnik/svxlink.cfg'
svxlinkel='/etc/spotnik/svxlink.el'
moduleecholinkconf='/etc/spotnik/svxlink.d/ModuleEchoLink.conf'
Json="/etc/spotnik/config.json"
fileId= '/var/lib/mmdvm/DMRIds.dat'
analogbridgeini= "/opt/Analog_Bridge/Analog_Bridge.ini"
mmdmvbridgeini="/opt/MMDVM_Bridge/MMDVM_Bridge.ini"
YSFGatewayini="/opt/YSFGateway/YSFGateway.ini"
mmdvmbridgedmr="/opt/MMDVM_Bridge/MMDVM_Bridge.dmr"


version="1.00"
call = " "
dept= " "
band = " "
usage= " "
Id = " "
test=0

# lancement avec argument
    
def main(argv):
    global dept 
    global call
    global band

    try:
        options, remainder = getopt.getopt(argv, '', ['help', 'version', 'dept=', 'call=', 'band='])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    
    for opt, arg in options:
        if opt == '--help':
            usage()
            sys.exit()
        elif opt == '--version':
            print(version)
            sys.exit()
        elif opt in ('--dept'):
            if arg != "":
                dept=str(arg)        
        elif opt in ('--call'):
            if arg != "":
                call=(arg)
                                            
        elif opt in ('--band'):
            if arg != "":
                band=str(arg)
                

    Input_control(dept,call,band)
                
            
    
def Input_control(dept,call,band):

    if dept==" " or call==" " or band==" ":
        print(dept+call+band)
        usage()
    else:
#Mise en forme des calls
        upcallsignSVX=(call)
        upcallsignEL=( "EL-" +call)
        upcallsignRRF=("(" +dept+ ") " +call+" "+band)

#Impression des calls
        print(call)
        print( call + "-EL")
        print("(" +dept+ ") " +call+" "+band)

#MAJ dans les fichiers de config
        updatecall(upcallsignSVX,upcallsignEL,upcallsignRRF)
        updatecallel(upcallsignSVX,upcallsignEL)
        updatecallelconf(upcallsignSVX)
        updatecall_json()
        searchId(call)
        updateIdMMDMV_Bridge(call,Id)
        updateIdANALOG_Bridge(call,Id)
        updateGateway(call,YSFGatewayini)
        updateMMDVM(call,mmdvmbridgedmr)

def usage():
    print('Usage: callconfig.py [options ...]')
    print()
    print('--help                           Cette aide')
    print('--version                        Numéro de version')
    print()
    print('Parametrages:')
    print() 
    print('  --dept       nombre      Entrer le numero de departement ex:88')
    print('  --call       texte       Entrer votre indicatif ex:F1ABC')
    print('  --band       nombre      Entrer la type acces (H,V,U,10M,R,T,T10M,S)')
    print()
    print('73 de F8ASB Juan')


#Fonction ecriture dans svxlink.cfg
def updatecall(callsignSVX,callsignEL,callsignRRF):
 
    config = ConfigParser()
    config.optionxform = str

    config.read(svxlinkcfg)

    string_val = config.get('SimplexLogic', 'CALLSIGN')
    config.set('SimplexLogic', 'CALLSIGN', callsignSVX)

    string_val = config.get('LocationInfo', 'CALLSIGN')
    config.set('LocationInfo', 'CALLSIGN', callsignEL)

    string_val = config.get('ReflectorLogic', 'CALLSIGN')
    config.set('ReflectorLogic', 'CALLSIGN', callsignRRF)

    with open(svxlinkcfg, 'w') as configfile:
        config.write(configfile, space_around_delimiters=False)

#Fonction ecriture dans svxlink.el
def updatecallel(callsignSVX,callsignEL):

    config = ConfigParser()
    config.optionxform = str

    config.read(svxlinkel)

    string_val = config.get('SimplexLogic', 'CALLSIGN')
    config.set('SimplexLogic', 'CALLSIGN', callsignSVX)

    string_val = config.get('LocationInfo', 'CALLSIGN')
    config.set('LocationInfo', 'CALLSIGN', callsignEL)

    with open(svxlinkel, 'w') as configfile:
        config.write(configfile, space_around_delimiters=False)

#Fonction ecriture dans moduleecholinkconf
def updatecallelconf(callsignSVX):

    config = ConfigParser()
    config.optionxform = str

    config.read(moduleecholinkconf)

    string_val = config.get('ModuleEchoLink', 'CALLSIGN')
    config.set('ModuleEchoLink', 'CALLSIGN', callsignSVX)

    with open(moduleecholinkconf, 'w') as configfile:
        config.write(configfile, space_around_delimiters=False)


#Fonction ecriture dans config.json
def updatecall_json():

    #lecture de donnees JSON
    with open(Json, 'r') as f:
        config = json.load(f)
        config['callsign'] = call
        config['Departement'] = dept
        config['band_type'] = band
    #ecriture de donnees JSON
    with open(Json, 'w') as f:
        json.dump(config, f)    
#
#PARTIE NUMERIQUE
#

#rechercher Id selon call
def searchId(callsignId):
    global Id
    
    fichier = open(fileId,"r")
    print("Recherche de l'Id ...")
    for ligne in fichier:
        if callsignId in ligne:
            Id = ((ligne).split())
            print(Id[0])
            Id = Id[0]
    fichier.close()

    if Id==" ":
            print('\x1b[7;37;41m'+"->VOTRE INDICATIF NE FIGURE PAS DANS LA DATABASE DMRIds.dat "+'\x1b[0m')
            os.system('sh /usr/local/sbin/DMRIDUpdate.sh')

            if test==0:
                searchId(callsignId)
                test=1
            else:
                sys.exit()

    else:
        controlID(Id,analogbridgeini)

#Mise a jour Id dans les fichiers de config numeriques

def updateIdMMDMV_Bridge(callsign,Id):
        
    config = ConfigParser()
    config.optionxform = str

    config.read(analogbridgeini)

    string_val = config.get('AMBE_AUDIO', 'gatewayDmrId')
    config.set('AMBE_AUDIO', 'gatewayDmrId', Id)

    string_val = config.get('AMBE_AUDIO', 'repeaterID')
    config.set('AMBE_AUDIO', 'repeaterID', Id+"01")

    with open(analogbridgeini, 'w') as configfile:
    #
        config.write(configfile, space_around_delimiters=False)
        print("Ecriture MMDMV_Bridge.ini ...")

def updateIdANALOG_Bridge(callsign,Id):

    config = ConfigParser()
    config.optionxform = str

    config.read(mmdmvbridgeini)

    string_val = config.get('General', 'Callsign')
    config.set('General', 'Callsign', callsign )

    string_val = config.get('General', 'Id')
    config.set('General', 'Id', Id)
      
    with open(mmdmvbridgeini, 'w') as configfile:
        config.write(configfile, space_around_delimiters=False)
        print("Ecriture ANALOG_Bridge.ini ...")

#Mise a jour des fichiers gateway
def updateGateway(callsign,fileini):
        
    config = ConfigParser()
    config.optionxform = str

    config.read(fileini)

    string_val = config.get('General', 'Callsign')
    config.set('General', 'Callsign', callsign )
    
    string_val = config.get('General', 'Id')
    config.set('General', 'Id', Id)

    with open(fileini, 'w') as configfile:
        config.write(configfile, space_around_delimiters=False)
        print("Ecriture "+fileini+" ...")    

#Mise a jour du fichier MMDVM_Bridge.dmr
def updateMMDVM(callsign,fileini):

    config = ConfigParser()
    config.optionxform = str

    config.read(fileini)

    string_val = config.get('General', 'Callsign')
    config.set('General', 'Callsign', callsign )

    string_val = config.get('General', 'Id')
    config.set('General', 'Id', Id)

    with open(fileini, 'w') as configfile:
        config.write(configfile, space_around_delimiters=False)
        print("Ecriture "+fileini+" ...")

def controlID(Nid,fileini):
    
    print(Nid)
    print(fileini)

    config = ConfigParser()
    config.optionxform = str

    config.read(fileini)

    string_val = config.get('AMBE_AUDIO', 'gatewayDmrId')
    print(string_val)



if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        pass

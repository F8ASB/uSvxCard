#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser, os
import json
import sys
import getopt

svxlinkcfg='/etc/spotnik/svxlink.cfg'
Json="/etc/spotnik/config.json"
version="1.00"
call = " "
dept= " "
band = " "
usage=""
# lancement avec argument
    
def main(argv):
    dept = " "
    call=" "
    band=" "

    try:
        options, remainder = getopt.getopt(argv, '', ['help', 'version', 'dept=', 'call=', 'band='])
    except getopt.GetoptError:
        l.usage()
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
        upcallsignEL=( call + "-EL")
        upcallsignRRF=("(" +dept+ ")" +call+" "+band)

#Impression des calls
#        print(call)
#        print( call + "-EL")
#        print("(" +dept+ ")" +call+" "+band)
#MAJ dans les fichiers
        updatecall(upcallsignSVX,upcallsignEL,upcallsignRRF)
        updatecall_json()
                
        

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
    
    try:
        from configparser import ConfigParser
    except ImportError:
        from ConfigParser import ConfigParser  # ver. < 3.0

    # instantiate
    config = ConfigParser()

    # parse existing file
    config.read(svxlinkcfg)

    # lecture et maj
    string_val = config.get('SimplexLogic', 'callsign')
    config.set('SimplexLogic', 'callsign', callsignSVX)

    # lecture et maj
    string_val = config.get('LocationInfo', 'callsign')
    config.set('LocationInfo', 'callsign', callsignEL)

    # lecture et maj
    string_val = config.get('ReflectorLogic', 'callsign')
    config.set('ReflectorLogic', 'callsign', callsignRRF)

    # Enregistrement
    with open(svxlinkcfg, 'w') as configfile:
        config.write(configfile)

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

#Question pour parametrage
#print('Entrer votre indicatif:')
#call = input()
#print('Entrez votre departement:')
#dept = input()
#print('Entrez votre bande: ( V,U,R,H')
#band = input()


#Impression des calls
#print(call)
#print( call + "-EL")
#print("(" +dept+ ")" +call+" "+band)

#Mise en forme des calls
#upcallsignSVX=(call)
#upcallsignEL=( call + "-EL")
#upcallsignRRF=("(" +dept+ ")" +call+" "+band)

#MAJ dans les fichiers
#updatecall(upcallsignSVX,upcallsignEL,upcallsignRRF)
#updatecall_json()

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        pass



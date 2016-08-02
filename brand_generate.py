#!/usr/bin/env python3
# coding: utf8
from __future__ import unicode_literals

__author__ = 'lgp'

import sys
import re


def myread(filename):
    """
        Extrait la marque d'un des champs et génère un champ supplémetaire avec la marque seule

        Utilisation de la lib regexp : re

        3 cas :

        Marque déjà fournie => Pas de modif
        Input : A-000000-00231;PRODITION AGIL ITE OTICON PRIX AUDIOPROTHESE prodition;Oticon
        Output : A-000000-00231;PRODITION AGIL ITE OTICON PRIX AUDIOPROTHESE prodition;Oticon

        Marque non fournie et détectée dans le 2eme champ => ajout de la marque en 3ème champ
        Input : A-000000-00231;PRODITION AGIL ITE OTICON PRIX AUDIOPROTHESE prodition;
        Output : A-000000-00231;PRODITION AGIL ITE OTICON PRIX AUDIOPROTHESE prodition;Oticon

        Marque non fournie et pas de match dans le 2eme champ => ajout de la marque Autre en 3ème champ
        Input : A-000000-00231;PRODITION AGIL ITE OTICON PRIX AUDIOPROTHESE prodition;Oticon
        Output : A-000000-00231;PRODITION AGIL ITE OTICON PRIX AUDIOPROTHESE prodition;Oticon
    """

    f = open(filename,'r')

    pattern_list = ['audio service', 'beltone', 'bernafon', 'biotone rexton',
                    'coselgi appareil auditif', 'hansaton - audiomedi', 'interton', 'newson',
                    'oticon', 'phonak', 'resound', 'rexton', 'siemens', 'sona', 'sonic innovations',
                    'starkey', 'unitron hearing', 'widex', 'autre']


    for line in f:
        tab = line.split(";")
        id = tab[0]
        libelle = tab[1].lower()
        brand = tab[2].strip()

        if (brand == ''):
            i =  0
            for pattern in pattern_list:
                brandreg = re.compile(pattern)
                result = brandreg.search(libelle)
                if (result) :
                    print(id + ";" + tab[1] + ";" + pattern)
                    break
                elif (i == len(pattern_list)-1):
                    print(id +  ";" + tab[1] + ";autre")
                i = i + 1
        else:
            print(id + ";" + tab[1] + ";" + brand)


if __name__ == '__main__':

    if len(sys.argv) > 1:
        myread(sys.argv[1])
    else:
        print("Script needs an argument (filename)")
    pass
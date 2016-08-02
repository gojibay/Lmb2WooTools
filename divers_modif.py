#!/usr/bin/env python3
# coding: utf8
from __future__ import unicode_literals

__author__ = 'lgp'

import sys
import re
import fnmatch

def type(filename):
    pat = {
        "Branche de lunette" : "branche_de_lunette",
        "Branche de lunette auditive" : "branche_de_lunette_auditive",
        "Contour d'oreille" : "contour_d_oreille",
        "Contour d'oreille standard" : "contour_d_oreille_standard",
        "Contour écouteur déporté" : "contour_ecouteur_deporte",
        "Intra classique" : "intra_classique",
        "Intra très discret" : "intra_tres_discret",
        "Intra-auriculaire" : "intra_auriculaire",
        "Intra-auriculaire discret" : "intra_auriculaire_discret",
        "Intra-auriculaire très discret" : "intra_auriculaire_tres_discret",
        "Intra-auriculaire classique" : "intra_auriculaire_classique",
        "Micro contour d'oreille" : "micro_contour_d_oreille",
        "Micro contour open" : "micro_contour_open",
        "Micro contour standard" : "micro_contour_standard",
        "Micro contour à écouteur déporté" : "micro_contour_a_ecouteur_deporte",
        "Micro contour écouteur déporté" : "micro_contour_ecouteur_deporte",
        "appareil auditif invisible" : "appareil_auditif_invisible",
        "appareil auditif très discret" : "appareil auditif_tres_discret",
        "intra CIC micro déporté" : "intra_cic_micro_deporte",
        "intra conduit micro déporté" : "intra_conduit_micro_deporte",
        "intra invisible" : "intra_invisible",
    }

    f = open(filename,'r')

    for line in f:
        #print("LINE : " + line.strip())
        tab = line.strip().split(sep=";")
        sku = tab[0].strip()
        if (len(tab) > 1):
            dat = tab[1].strip()
            if (dat != ""):
                print(sku + ";" + pat[dat])
            else:
                print(line.strip())
        else:
            print(line.strip())



def date_sortie(filename):
    #f = open(filename, 'r')
    f = open(filename,'r')


    pat = {
     "Avant 2011" : "2011_avant" ,
     "Debut 2012" : "2012_debut" ,
     "Fin 2012" : "2012_fin" ,
     "Mi 2012" : "2012_mi" ,
     "Debut 2013" : "2013_debut" ,
     "Fin 2013" : "2013_fin" ,
     "Mi 2013" : "2013_mi" ,
     "Debut 2014" : "2014_debut" ,
     "Fin 2014" : "2014_fin" ,
     "Debut 2015" : "2015_debut" ,
     "Fin 2015" : "2015_fin" ,
     "2016" : "2016",
     "2015" : "2015",
     "2014" : "2014",
     "2013" : "2013",
     "2012" : "2012",
     "2011" : "2011",
     "Debut 2016" : "2016_debut" ,
     "Fin 2016" : "2016_fin" ,
     "Mi 2016" : "2016_mi" ,
     "Debut 2017" : "2017_debut" ,
     "Fin 2017" : "2017_fin" ,
     "Mi 2017" : "2017_mi" ,
     "date_de_sortie" : "date_de_sortie"
    }



    for line in f:
        #print("LINE : " + line.strip())
        tab = line.strip().split(sep=";")
        sku = tab[0].strip()
        if (len(tab) > 1):
            dat = tab[1].strip()
            if (dat != ""):
                print(sku + ";" + pat[dat])
            else:
                print(line.strip())
        else:
            print(line.strip())


if __name__ == '__main__':

    if len(sys.argv) > 1:
        type(sys.argv[1])
    else:
        print("Script needs an argument (filename)")
    pass
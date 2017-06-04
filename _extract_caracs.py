#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'lgp'

import pymysql
import logging
import csv
import pprint as pp
from optparse import OptionParser
import re





if __name__ == '__main__':



    usage = """

        Script qui extrait des données de la db1 et génère soit :
            - les requêtes sql pour l'update d'une deuxième base
            - le fichier csv contenant les datas

        %prog --user1 username --pass1 pwd --db1 dbname

    """

    parser=OptionParser(usage=usage)
    parser.add_option("--trace" ,action="store_true",dest="trace",default=False,help="A utiliser pour declencher un mode verbeux. Default=False")
    parser.add_option("--user1" , dest="user", help='user Default=user1', default="audiologys")
    parser.add_option("--pass1" , dest="pwd1", help='pwd Default=pass1', default="audiologys")
    parser.add_option("--db1"   , dest="db1"  , help='db Default=db1', default="audiologys_utf8")
    parser.add_option("--output", dest="csv_filename", default='output.csv', help='filename for csv output Default=output.csv')

    (opts,args) = parser.parse_args()

    l = [{'ref_carac': 'ACC-000000-0000d', 'valeur': 'non', 'ref_article': 'A-000000-02286'}, 
        {'ref_carac': 'ACC-000000-0000e', 'valeur': 'non', 'ref_article': 'A-000000-02286'}, 
        {'ref_carac': 'ACC-000000-0000f', 'valeur': 'oui', 'ref_article': 'A-000000-02286'}, 
        {'ref_carac': 'ACC-000000-0000g', 'valeur': 'non', 'ref_article': 'A-000000-02286'}, 
        {'ref_carac': 'ACC-000000-0000h', 'valeur': 'non', 'ref_article': 'A-000000-02286'}, 
        {'ref_carac': 'ACC-000000-0000i', 'valeur': 'non', 'ref_article': 'A-000000-02286'}, 
        {'ref_carac': 'ACC-000000-0000j', 'valeur': '10', 'ref_article': 'A-000000-02286'}, 
        {'ref_carac': 'ACC-000000-0000k', 'valeur': 'oui', 'ref_article': 'A-000000-02286'}, 
        {'ref_carac': 'ACC-000000-0000m', 'valeur': '17 canaux', 'ref_article': 'A-000000-02286'}, 
        {'ref_carac': 'ACC-000000-0000n', 'valeur': 'Oui', 'ref_article': 'A-000000-02286'}, 
        {'ref_carac': 'ACC-000000-0000l', 'valeur': 'www.resound.fr/', 'ref_article': 'A-000000-02286'}, 
        {'ref_carac': 'ACC-000000-0000o', 'valeur': 'www.youtube.com/watch?v=OmaWrxoclAk&feature=channel&list=UL', 'ref_article': 'A-000000-02286'}, 
        {'ref_carac': 'ACC-000000-0000p', 'valeur': 'www.facebook.com/login.php', 'ref_article': 'A-000000-02286'}, 
        {'ref_carac': 'ACC-000000-00001', 'valeur': 'Micro contour écouteur déporté', 'ref_article': 'A-000000-02288'}, 
        {'ref_carac': 'ACC-000000-00006', 'valeur': 'Elite', 'ref_article': 'A-000000-02288'}, 
        {'ref_carac': 'ACC-000000-00008', 'valeur': 'Surdité légere à moyenne de 20 à 70 % de perte', 'ref_article': 'A-000000-02288'}, 
        {'ref_carac': 'ACC-000000-0000b', 'valeur': 'Classe D', 'ref_article': 'A-000000-02288'}, 
        {'ref_carac': 'ACC-000000-0000q', 'valeur': 'Début 2016', 'ref_article': 'A-000000-02288'}, 
        {'ref_carac': 'ACC-000000-0000d', 'valeur': 'oui', 'ref_article': 'A-000000-02288'}]

    d = dict()
    for item in l :
        ref_article = item['ref_article']
        ref_carac   = item['ref_carac']
        valeur      = item['valeur']
        if check_key(ref_article, d):
            if( not check_key(ref_carac, d[ref_article])):
                d[ref_article][ref_carac] = valeur
            else:
                print("Key " + ref_carac + " already assigned to " + ref_article)
        else:
            elt = dict()
            elt[ref_carac] = valeur
            d[ref_article] = elt

    print(d)







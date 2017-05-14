#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Script to extact external product from LMB Community db into csv for WooCommerce import 

    1/ extract products (text info) from db
    2/ get images url and generate csv for import

"""

__author__ = 'lgp'

import pymysql
import logging
import csv
import pprint as pp
from optparse import OptionParser
import re

class connector:

    def __init__(self, host='localhost', port=3306, user='user1', password='pass', database='db', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor):
        self.conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset=charset,
            cursorclass=cursorclass,
            autocommit=True
        )
        self.cursor = self.conn.cursor()

class myops:

    def __init__(self, connector):
        self.connector = connector
        self.categories = dict()
        self.annuaire = dict()
        self.images = dict()

    def initialize(self):
        self.fetch_categories()
        #print(self.categories)
        self.fetch_contacts()
        #print(self.annuaire)
        self.fetch_images()

    def retrieve_fields(self, table="", fields_to_retrieve=[], filter_on={}, filter_exclude={}):
        """
        This function retrieves the fields given in 'fields_to_retrieve' of the entries having 'key' and matching values 'filter_on' and excluding filter_exclude

        Exemple : 
        ref_article
        filter ref_art_categ = A.C-000000-00003
        desc_courte
        desc_longue


        """

        # retrieve fields to get data from
        fields = ""
        for f in fields_to_retrieve:
            fields += f + ","
        fields = fields.strip(',')

        # retrieve field and value to filter on
        # !!!! first versin on one only value
        #print(filter_on["ref_art_categ"])

        sql_filter_on = ""
        if len(filter_on) > 0:
            for key,value in filter_on.items():
                sql_filter_on = key + " = '" + value + "'"
                #print(sql_filter_on)

        sql_filter_exclude = ""
        if len(filter_exclude) > 0:
            for key,value in filter_exclude.items():
                sql_filter_exclude = key + " != '" + value + "'"
                #print(sql_filter_exclude)

        sql_filter = ""
        if ( sql_filter_on == "" and sql_filter_exclude == "") :
            pass
        elif ( sql_filter_on == "" and sql_filter_exclude != "" ) :
            sql_filter = sql_filter_exclude
        elif sql_filter_exclude == "":
            sql_filter = sql_filter_on
        else:
            sql_filter = sql_filter_on + " AND " + sql_filter_exclude 

        # generate MYSQL request
        myrequest = "SELECT " + fields + " "
        myrequest += " FROM " + table + " "
        if len(sql_filter):
            myrequest += " WHERE " + sql_filter
        myrequest += " ;"

        #print(myrequest)

        self.connector.cursor.execute(myrequest)
        #print(self.cursor.description)

        # retrieve all data in array
        result = self.connector.cursor.fetchall()
        return result


    def write_csv(self, fname="output.csv", keyfields=['ref_article'], data=[]):
        """
        This function writes the data 'data' in a csv file

        exemple data : [
                        {'desc_longue': b'Placer le lien vers la fiche PDF constructeur<br>',
                        'desc_courte': b'appareil auditif dual V OTICON',
                        'ref_article': 'A-000000-00005'}
                        ]

            csv file :
            A-000000-00005;'appareil auditif dual V OTICON';'Placer le lien vers la fiche PDF constructeur<br>'

        """

        print("Writing to " +  str(fname) + " ... ")
        #print(data)

        newline_regexp = ""

        spamwriter = ''
        #print("#######################################")
        with open(fname, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            # generate lines
            for elt in data:
                line = []

                for field in keyfields:
                    if ( field == 'image'):
                        v = elt['ref_article']
                        v = self.get_image_filename(v)
                    else:
                        v = elt[field]


                    if ( field == "ref_art_categ" ):
                        #print(field + " "  + v)
                        ## on n'importe que le code catégorie pour dans un 1er temps
                        #v = self.get_categorylib_from_ref(v) + ' ## ' + v
                        pass

                    if ( field == "ref_constructeur" ):
                        #print(field + " "  + str(v))
                        if v:
                            v = self.get_nom_from_refcontact(v)
                    if ( field == 'image'):
                        v = elt['ref_article']
                        v = self.get_image_filename(v)

                    if ( field == 'dispo'):
                        #print(field + " "  + str(v))
                        if v == 1:
                            v="publish"
                        else:
                            v="draft"

                    # force de decoding
                    forcedec_v = self.force_decode(v)
                    #print("@@@@@@@@@@@@@@@@@" + str(forcedec_v))
                    # force encode to a codec
                    if type(forcedec_v) == type(str()):
                        forcedec_v.encode("utf8")
                        line.append(forcedec_v.replace('\r\n', ' ').replace('\n', ' '))
                    else:
                        line.append(forcedec_v)

                """
                Let's add these fields
                   xxx              = manage_stock -> no    
                   xxx              = visibility  -> hidden or catalog
                   xxx              = featured -> no
                   xxx              = comment_status -> closed
                   xxx              = ping_status -> closed
                """
                line.append("no")
                line.append("catalog")
                line.append("no")
                line.append("closed")
                line.append("closed")
                spamwriter.writerow(line)



    def fetch_categories(self):
        """
            fetch categories from art_categs table and return a dict of ref:lib  

            exemple : {'A.C-000000-00026':'ACCESSOIRES DIVERS'}
        """
        req = "SELECT ref_art_categ, lib_art_categ FROM `art_categs`"
        self.connector.cursor.execute(req)
        result = self.connector.cursor.fetchall()
        d = {}
        for item in result:
            ref = item['ref_art_categ']
            lib = item['lib_art_categ']
            d[ref] = lib
            #print(ref + ' ' +  lib)

        self.categories = d


    def fetch_contacts(self):
        """
            fetch names from 'annuaire' table and return a dict of ref:lib  

            exemple : {'C-000000-00026':'REXTON'}
        """
        req = "SELECT ref_contact, nom FROM `annuaire`"
        self.connector.cursor.execute(req)
        result = self.connector.cursor.fetchall()
        d = {}
        for item in result:
            ref = item['ref_contact']
            lib = item['nom']
            d[ref] = lib

        self.annuaire = d

    def fetch_images(self):
        request = "SELECT a.ref_article, b.lib_file, c.ref_art_categ FROM articles_images AS a, images_articles AS b, articles AS c WHERE a.id_image=b.id_image AND a.ref_article=c.ref_article AND a.ordre=1 AND c.ref_art_categ!='A.C-000000-00003'"
        d = self.fetch_data_in_db(request, 'ref_article', 'lib_file')
        self.images = d

    def fetch_data_in_db(self, req, key, value):
        """
            exemple 
            SELECT a.ref_article, b.lib_file, c.ref_art_categ FROM articles_images AS a, images_articles AS b, articles AS c WHERE a.id_image=b.id_image AND a.ref_article=c.ref_article AND a.ordre=1 AND c.ref_art_categ!='A.C-000000-00003'
        """
        d = {}
        try:
            if req:
                self.connector.cursor.execute(req)
                result = self.connector.cursor.fetchall()
                for item in result:
                    k = item[key]
                    v = item[value]
                    d[k] = v
            return d
        except:
            return {}

    def get_categorylib_from_ref(self, ref):
        if len(self.categories):
            return self.categories[ref]
        return ''

    def get_nom_from_refcontact(self, ref):
        if len(self.annuaire):
            return self.annuaire[ref]
        return ''

    def get_image_filename(self, ref):
        if len(self.images):
            try:
                fimg = self.images[ref]
                #url = "http://www.audiologys.com/catalogue/fichiers/images/articles/"+fimg
                url = "http://www.audiologys.com/image_pour_import/articles/"+fimg
                return url
            except:
                return ''
                
        return ''

    def force_decode(self, string, codecs=['cp1252', 'utf8', 'iso-8859-1']):
        """
            the function tries to decode the string given a list of codecs
            return nothing is cannot decode
        """
        for i in codecs:
            try:
                s = string.decode(i)
                return s
            except:
                pass
        return string
        logging.warn("cannot decode url %s" % ([string]))




if __name__ == '__main__':



    usage = """

        Script qui extrait des données de la db1 et génère soit :
            - les requêtes sql pour l'update d'une deuxième base
            - le fichier csv contenant les datas

        Usage : script.py --user1 username --pass1 pwd --db1 dbname --output filename.csv

    """

    parser=OptionParser(usage=usage)
    parser.add_option("--trace" ,action="store_true",dest="trace",default=False,help="A utiliser pour declencher un mode verbeux. Default=False")
    parser.add_option("--user1" , dest="user", help='user Default=user1', default="audiologys")
    parser.add_option("--pass1" , dest="pwd1", help='pwd Default=pass1', default="audiologys")
    parser.add_option("--db1"   , dest="db1"  , help='db Default=db1', default="audiologys_utf8")
    parser.add_option("--port1"   , dest="port1"  , help='port Default=3307', default=3307)

    parser.add_option("--output", dest="csv_filename", default='output.csv', help='filename for csv output Default=output.csv')

    (opts,args) = parser.parse_args()


    #print(opts)
    #print(args)

    if len(args) > 0:
        mode = args[0].lower()

    user1 = str(opts.user)
    pass1 = str(opts.pwd1)
    db1   = str(opts.db1)
    port1 = opts.port1
    csv_filename = str(opts.csv_filename)

    # create a connection handler
    # 2 connection to 2 different databases
    myconn1 = connector("127.0.0.1", port1, user1, pass1, db1 )
    #myconn2 = connector("127.0.0.1", 3306, "user", "passwd", "db_name" )

    # create instance of myops class
    print("Create instance...")
    controller = myops(myconn1)
    print("Initializing...")
    controller.initialize()

    print("Retrieving fields...")
    # launch task function
    data = controller.retrieve_fields("articles", 
        ["ref_article", "lib_article", "desc_courte", "desc_longue", "ref_art_categ", "modele", "ref_constructeur", "paa_ht", "id_tva", "dispo", "ref_article"], 
        {"ref_art_categ" : "A.C-000000-00003" },
        {}
        )

    """
    ref_article         = SKU
    lib_article         = post_title
    desc_courte         = post_excerpt
    desc_longue         = post_content
    ref_art_categ       = category
    modele              = 
    ref_constructeur    = marque 
    paa_ht              = regular_price
    id_tva              = tax_class
    dispo               = post_status -> publish
                                        private ou draft
    image               = featured_image

       xxx              = manage_stock -> no    
       xxx              = visibility  -> hidden  / catalog
       xxx              = featured -> no
       xxx              = comment_status -> closed
       xxx              = ping_status -> closed

    "ref_article", "lib_article", "desc_courte", "desc_longue", "ref_art_categ", "modele", "ref_constructeur", "paa_ht", "id_tva", "dispo", "ref_article"




    """

    table_correspondance = {
        "ref_article"       : "SKU",
        "lib_article"       : "post_title",
        "desc_courte"       : "post_excerpt",
        "desc_longue"       : "post_content",
        "ref_art_categ"     : "category",
        "modele"            : "modele",
        "ref_constructeur"  : "marque" ,
        "paa_ht"            : "regular_price",
        "id_tva"            : "tax_class",
        "dispo"             : "post_status -> publish / private ou draft",
        "image"             : "featured_image"
    }

    # xxx              = manage_stock -> no    
    # xxx              = visibility  -> hidden
    # xxx              = featured -> no
    # xxx              = comment_status -> closed
    # xxx              = ping_status -> closed



    #myops_write.write_mysql_update_request("articles_write_utf8", "ref_article", data)

    #print(data)

    controller.write_csv(csv_filename, 
        ["ref_article", "lib_article", "desc_courte", "desc_longue", 
        "ref_art_categ", "modele", "ref_constructeur", 
        "paa_ht", "id_tva", "dispo", "image"], 
        data)



    # close cursor and connection
    # connexion 1
    myconn1.cursor.close()
    myconn1.conn.close()
    # connexion 2
    #myconn2.cursor.close()
    #myconn2.conn.close()

    pass

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
import string

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

    def __init__(self, connector, filename_id_sku):
        self.connector = connector
        self.categories = dict()
        self.annuaire = dict()
        self.images = dict()
        self.filename_id_sku = filename_id_sku
        self.table_correspondance = dict()

    def initialize(self):
        self.fetch_categories()
        #print(self.categories)
        self.fetch_contacts()
        #print(self.annuaire)
        self.fetch_images()

        self.generate_table_correspondances(self.load_id_sku())


    # à partir de la table du csv sku;id;ref-lmb extraite de WP on créé la table de corresondance
    def load_id_sku(self):    
        with open(self.filename_id_sku , 'r') as f:
            correspondance = f.readlines()
        correspondance = [x.strip() for x in correspondance]
        return correspondance

    def generate_table_correspondances(self, maliste):
        """
            création d'un dict aec A-000000-00xxxx en clé et l'id en value
            regarde warning si doublons
        """
        print("Generate_table_correspondances")
        d = dict()
        for elt in maliste:
            c = elt.split(",")
            reflmb = c[2]
            wpid   = c[1]
            #print(reflmb)
            if reflmb.startswith( 'A-000000-' ):
                if not reflmb in d.keys():
                    d[reflmb] = wpid
                else:
                    print("WARNING THIS REFERENCE IS ALREADY LINKED TO ANOTHER ID => " + reflmb + " / " + wpid)

        self.table_correspondance = d
        #print(d)

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
            if f not in ["lib_article_clean"]:
                fields += f + ","
        fields = fields.strip(',')
        print(fields)
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

        result =self.execute_request(myrequest)
        return result

    def execute_request(self, request):
        self.connector.cursor.execute(request)
        #print(self.cursor.description)

        # retrieve all data in array
        result = self.connector.cursor.fetchall()
        return result


    def extract_liaisons(self):
        print("extract_liaisons")
        # requette mysql pour récupérer les articles associés de type 1
        request =  "SELECT al.`ref_article`, al.`ref_article_lie`, al.`id_liaison_type` "
        request += "FROM articles_liaisons al, articles a "
        request += "WHERE a.`ref_article` = al.`ref_article` "
        request += "AND a.`ref_art_categ` = 'A.C-000000-00003' "
        request += "AND al.`id_liaison_type` = 1 "

        result =self.execute_request(request)

        # cleanup
        d = self.cleanup_liaisons(result)


        all_update_requests = ""
        # generer les champ meta_value
        for k,v in d.items():
            # on récupère la chaine  a:0:{} ...
            m = self.generate_upsells_ids(k, v)
            #print(k + " " + m)

            if k in self.table_correspondance.keys():
                _post_id = self.table_correspondance[k]
                updaterequest = 'UPDATE `wp_postmeta` SET `meta_value`="' + m + '" WHERE `post_id`="'+ _post_id +'" AND `meta_key` = "_upsell_ids";\n'
                all_update_requests += updaterequest


        return all_update_requests

    def cleanup_liaisons(self, data):
        print("cleanup_liaisons")
        # on transforme la data extraite de la base mysql en un dict
        d = dict()

        for elt in data:
            appar = elt['ref_article']
            assoc = elt['ref_article_lie']
            if appar in d.keys():
                d[appar].append(assoc)
            else:
                d[appar] = [assoc]

        return d  


    def generate_upsells_ids(self, ID, upsell_ids_list):
        # update wp_postmeta table 
        d = dict()
        metvalue=""
        l = upsell_ids_list.__len__()
        if l > 0:
            
            idx = 0
            for upsell_id in upsell_ids_list:
                if upsell_id in self.table_correspondance.keys():
                    upsell_id = self.table_correspondance[upsell_id]
                    metvalue += "i:"+str(idx)+";i:"+upsell_id+";"
                    idx += 1

            metvalue += '}'
            prefmetvalue = 'a:'+str(idx)+':{'

            metvalue = prefmetvalue + metvalue

        return metvalue




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
                    ### ici on a utilsié des noms de champs qui nexistent pas dans lmb
                    if ( field == 'image'):
                        v = elt['ref_article']
                        v = self.get_image_filename(v)
                    elif (field == 'lib_article_clean'):
                        v = elt['lib_article']
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
                        paa = elt['paa_ht']
                        #print(paa)

                        if v == 1:
                            if paa and paa > 0.0 :
                                v="publish"
                            else:
                                v='draft'
                        else:
                            v="draft"

                    if ( field == 'lib_article_clean' ):
                        v = self.cleanup_title(v)
                        #print("--------------------\n" + v + "\n" + v2)
                        #print("--------------------\n"  + v2)

                    # force de decoding
                    forcedec_v = self.force_decode(v)
                    #print("@@@@@@@@@@@@@@@@@" + str(forcedec_v))
                    # force encode to a codec
                    if type(forcedec_v) == type(str()):
                        forcedec_v.encode("utf8")
                        line.append(forcedec_v.replace('\r\n', ' ').replace('\n', ' '))
                    else:
                        line.append(forcedec_v)



                ### ADAPT TO YOUR NEEDS ####
                """
                Let's add these fields
                   xxx              = manage_stock -> no    
                   xxx              = visibility  -> hidden or catalog
                   xxx              = featured -> no
                   xxx              = comment_status -> closed or open
                   xxx              = ping_status -> closed
                """

                if PRODUCT_TYPE == "optionnal":
                    line.append("no")
                    line.append("catalog")
                    line.append("no")
                    line.append("closed")
                    line.append("closed")
                if PRODUCT_TYPE == "appareil":
                    line.append("no")
                    line.append("search")
                    line.append("no")
                    line.append("open")
                    line.append("open")
            
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




    def cleanup_title(self, title):
        pat = [
            "appareils? auditifs?", "audio ?proth.ses?", "proth.ses? auditives?", "syst.mes? auditifs?", "appareil correcteur .lectronique",
            "aide auditive",
            "audioprothese rechargeable proposée par l’audioprothésiste aux malentendants très agés et malhabiles",
            "correcteur de surdité",
            "toutes les surdités", 
            "surdit. mixte", 
            "acouph.nes?", 
            "patient atteint de surdité de transmission", 
            "pour toutes les surdités", 
            "prix .quivalent au", "prix", "moins cher", "cher", "surpuissant", "pour", "contre", "existe aussi",
            "biotone rexton",  "biotone" ,"widex", "starkey", "resound", "beltone", "rexton", "siemens", "phonak", "oticon", "bernafon", 
            "prodition", "hansaton", "hansaton -? ?audimedi", "unitron", "unitron hearing", "sonic", "sonic innovations", "sona", "newson"
            ]

        x = title
        for p in pat:
            x = re.sub(p, '', x, flags=re.IGNORECASE)

        x = re.sub(' +', ' ', x)

        return x.strip(' ')   

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

    parser.add_option("--output", dest="csv_filename", default='products.csv', help='filename for csv output Default=output.csv')
    parser.add_option("-t", "--type", dest="product_type", default="optionnal", help="set this option to 'appareil' or 'optionnal' depending on type of product")


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

    PRODUCT_TYPE  = str(opts.product_type)

    # create a connection handler
    # 2 connection to 2 different databases
    myconn1 = connector("127.0.0.1", port1, user1, pass1, db1 )
    #myconn2 = connector("127.0.0.1", 3306, "user", "passwd", "db_name" )

    # create instance of myops class
    print("Create instance...")
    controller = myops(myconn1, "liste-id-sku-NO-DELETE-may14.csv")

    print("Initializing...")
    controller.initialize()


    #controller.generate_upsells_ids("1234", ["6789", "643734", "4534534", "344"])
    #import sys
    updatedata = controller.extract_liaisons()
    with open("update_requests.txt", 'w') as f:
        f.write(updatedata)

    exit(0)
    print("Retrieving fields...")
    # launch task function


    # RETRIEVE DATA
    if PRODUCT_TYPE == 'optionnal':
        #on filtre sur les appareils pour extraire tout lce qui n'est pas un appareil
        
        # Optional products : 
        fields_list     = ["ref_article", "lib_article", "desc_courte", "desc_longue", "ref_art_categ", "modele", "ref_constructeur", "paa_ht", "id_tva", "dispo", "ref_article"]
        fields_list_csv = ["ref_article", "lib_article", "desc_courte", "desc_longue", "ref_art_categ", "modele", "ref_constructeur", "paa_ht", "id_tva", "dispo", "ref_article", "image"]
        # Appareils auditifs
        #fields_list = ["ref_article", "lib_article"]
        data = controller.retrieve_fields("articles", 
            fields_list, 
            {},
            {"ref_art_categ" : "A.C-000000-00003" }
            )
    
    if PRODUCT_TYPE == 'appareil':
        #on filtre sur les appareils
        
        # Appareils auditifs
        #fields_list = ["ref_article", "lib_article", "desc_courte", "desc_longue", "modele", "ref_constructeur", "paa_ht", "id_tva", "dispo", "ref_article", ""]
        
        fields_list = ["ref_article", "lib_article", "paa_ht", "dispo"]
        fields_list_csv = ["ref_article", "ref_article", "lib_article", "lib_article_clean", "paa_ht", "dispo"]
        # 2 lib_article en version longue et courte
        # les descriptions sont déjà importées proprement
        data = controller.retrieve_fields("articles", 
            fields_list, 
            {"ref_art_categ" : "A.C-000000-00003" },
            {}
            )

    #myops_write.write_mysql_update_request("articles_write_utf8", "ref_article", data)

    #print(data)

    # WRITE DATA
    # write fields list to csv file
    controller.write_csv(csv_filename, 
        fields_list_csv, 
        data)


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




    # close cursor and connection
    # connexion 1
    myconn1.cursor.close()
    myconn1.conn.close()
    # connexion 2
    #myconn2.cursor.close()
    #myconn2.conn.close()

    pass

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Script to extract product from LMB Community db into csv for WooCommerce import 

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
import ressources

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

    def __init__(self, connector, filename_id_sku=''):
        self.connector = connector
        self.categories = dict()
        self.annuaire = dict()
        
        # conteint la liste de la featured image pour les produits
        self.images = dict()

        # conteint la liste des autres image pour les produits
        self.images_for_gallery = dict()

        self.filename_id_sku = filename_id_sku

        # used for sku / wpip correspondance
        self.table_correspondance = dict()

        # A.C.... -> LMB name of the "caracteristiques"
        self.caracs_dict = ressources.caracteristiques_id_name

        # A.C.... -> dict of lmb2wp correspondance
        self.caracs_dict_lmb2wp = ressources.caracteristiques_id_lmb2wp

        # 
        self.caracs_dict_ordered = sorted(self.caracs_dict.keys())
        self.caracs_dict_lmb2wp_ordered = sorted(self.caracs_dict_lmb2wp.keys())

    def initialize(self):
        self.fetch_categories()
        #print(self.categories)
        self.fetch_contacts()
        #print(self.annuaire)
        # on récupère les images 
        self.fetch_images()
        self.fetch_gallery_images()

        # dict de caracteristiques des produits
        # { ref_aticle : { carac1: value1, carac2 : value2, ... }}
        self.articles_caracs = self.extract_caracs()

        if self.filename_id_sku != '':
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
        This function generate the mysql request that retrieves the fields given in 'fields_to_retrieve' 
        of the entries having 'key' and matching values 'filter_on' and excluding filter_exclude

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


    def extract_liaisons(self, filename):
        """
            Generates mysql request to apply on wp/woocommerce db to link product with upsell products

            Write requests to file 'filename' 
        """
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


        with open(filename, 'w') as f:
            f.write(all_update_requests)


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


    def extract_caracs(self):
        """
            Generates mysql request extract caracteristics of a given article


        """
        print("extract_caracs")
        # requette mysql pour récupérer les articles associés de type 1
        request =  "SELECT ac.`ref_article`, ac.`ref_carac`, ac.`valeur` "
        request += "FROM articles_caracs ac, articles a "
        request += "WHERE a.`ref_article` = ac.`ref_article` "

        result =self.execute_request(request)
        #print(result)
        # cleanup
        d = self.cleanup_caracs(result)
        return d

    def cleanup_caracs(self, data):
        print("cleanup_caracs")
        # on transforme la data extraite de la base mysql en un dict
        d = dict()
        for item in data :
            ref_article = item['ref_article']
            ref_carac   = item['ref_carac']
            valeur      = item['valeur']
            if self.check_key(ref_article, d):
                if( not self.check_key(ref_carac, d[ref_article])):
                    d[ref_article][ref_carac] = valeur
                else:
                    print("Key " + ref_carac + " already assigned to " + ref_article)
            else:
                elt = dict()
                elt[ref_carac] = valeur
                d[ref_article] = elt

        return d


    def check_key(self, k, d):
        return k in d.keys()



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
                    elif ( field == 'images_product_gallery'):
                        v = elt['ref_article']
                        v = self.get_images_filenames_for_gallery(v)     
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
                    # TODO : add caracs
                    #print(elt['ref_article'])
                    c = self.append_caracs(elt['ref_article'])
                    
                    line += c 
                    line.append("no")
                    line.append("search")
                    line.append("no")
                    line.append("open")
                    line.append("open")
                    
                    #print(line)


                spamwriter.writerow(line)


    def append_caracs(self, ref_article):
        buf = []
        # on parcourt une liste de caracteristiuqes
        for carac in self.caracs_dict_ordered:
            #print(carac)
            # si l'article a cette caracteristique
            if ref_article in self.articles_caracs.keys():

                # si la caracteristique est présente pour cet article
                if carac in self.articles_caracs[ref_article].keys():
                    # on récupere la valeur extraite de lmb
                    c_lmb_value = self.articles_caracs[ref_article][carac]
                    # la valeur de lmb sera la valeur par défaut
                    val_for_buf = c_lmb_value
                    # check that la caracteristique est dans acf
                    if carac in self.caracs_dict_lmb2wp_ordered :   
                        c_lmb2acf   = self.caracs_dict_lmb2wp[carac]
                        # si on a une table de correspondance alors val_for_buf est updaté
                        if ( c_lmb_value in c_lmb2acf.keys() ):
                            val_for_buf = self.caracs_dict_lmb2wp[carac][c_lmb_value]
                        elif ( c_lmb_value.lower() in c_lmb2acf.keys() ):
                            val_for_buf = self.caracs_dict_lmb2wp[carac][c_lmb_value.lower()]
                        elif ( c_lmb_value.title() in c_lmb2acf.keys() ):
                            val_for_buf = self.caracs_dict_lmb2wp[carac][c_lmb_value.title()]
                        else:
                            print("MMMMH this value should be dealt with and it is not... check that : " + str(c_lmb_value) + " is in " + str(carac))    

                    # val_for_buf vaut soit la valeur dans lmb soit la valeur de la table de corresondance
                    buf.append(val_for_buf)
                else:
                    # si l'entrée n'existe pas pour ce produit on ajoute un champ vide dans le csv
                    buf.append('')
            else:
                buf.append('')
        #print(buf)
        return buf


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
        request = "SELECT a.ref_article, b.lib_file, c.ref_art_categ \
                    FROM articles_images AS a, images_articles AS b, articles AS c \
                    WHERE a.id_image=b.id_image AND a.ref_article=c.ref_article AND a.ordre=1 "

        if PRODUCT_TYPE == 'appareil':
            request += " AND c.ref_art_categ = 'A.C-000000-00003'"
        else:
            request += " AND c.ref_art_categ != 'A.C-000000-00003'"

        d = self.fetch_data_in_db(request, 'ref_article', 'lib_file')
        self.images = d

    def fetch_gallery_images(self):
        request = "SELECT a.ref_article, b.lib_file, c.ref_art_categ \
                    FROM articles_images AS a, images_articles AS b, articles AS c \
                    WHERE a.id_image=b.id_image AND a.ref_article=c.ref_article AND a.ordre>1 "

        if PRODUCT_TYPE == 'appareil':
            request += " AND c.ref_art_categ = 'A.C-000000-00003'"
        else:
            request += " AND c.ref_art_categ != 'A.C-000000-00003'"

        d = self.fetch_data_in_db_for_gallery(request, 'ref_article', 'lib_file')
        self.images_for_gallery = d


    def fetch_data_in_db(self, req, key, value):
        """
            exemple 
            SELECT a.ref_article, b.lib_file, c.ref_art_categ FROM articles_images 
            AS a, images_articles AS b, articles AS c WHERE a.id_image=b.id_image AND a.ref_article=c.ref_article 
            AND a.ordre=1   <= !!!! we only have one article at a time 
            AND c.ref_art_categ!='A.C-000000-00003'
        """
        d = {}
        try:
            if req:
                self.connector.cursor.execute(req)
                result = self.connector.cursor.fetchall()
                #print(result)
                for item in result:
                    k = item[key]
                    #print(k)
                    v = item[value]
                    #print(v)

                    d[k] = v
            return d
        except:
            return {}


    def fetch_data_in_db_for_gallery(self, req, key, value):
        """
            exemple 
            SELECT a.ref_article, b.lib_file, c.ref_art_categ FROM articles_images 
            AS a, images_articles AS b, articles AS c WHERE a.id_image=b.id_image AND a.ref_article=c.ref_article 
            AND a.ordre > 1   <= !!!! we have multiple images possibly
            AND c.ref_art_categ!='A.C-000000-00003'
        """
        d = {}
        try:
            if req:
                self.connector.cursor.execute(req)
                result = self.connector.cursor.fetchall()
                # EXAMPLE :   {'ref_article': 'A-000000-02317', 'lib_file': '152bcd03be083c8a11ca257b30b45491cros.png', 'ref_art_categ': 'A.C-000000-00003'}, 
                #print(result)
                for item in result:
                    k = item[key]
                    v = item[value]
                    if k in d.keys():
                        #print("new image ")
                        d[k] =  d[k] + "|" + v
                    else:
                        d[k] = v
            #print(d)
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

    def get_images_filenames_for_gallery(self, ref):
        if len(self.images_for_gallery):
            try:
                fimg = self.images_for_gallery[ref]
                url=""
                for image_name in fimg.split('|'):
                    url += "http://www.audiologys.com/image_pour_import/articles/"+image_name + "|"
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
            "proposée par l’audioprothésiste aux malentendants très agés et malhabiles",
            "correcteur de surdité",
            "toutes les surdités", 
            "surdit. mixte", 
            "acouph.nes?", 
            "telecommande rc dex comprise",
            "generateur de bruit",
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

        Usage : script.py --user1 username --pass1 pwd --db1 dbname --output filename.csv --type [appareil|optionnal]

        Example : python extract_products.py --type appareil --output ici.csv -U
        extracts product of type appareil + generates upsell requests

    """

    parser=OptionParser(usage=usage)
    parser.add_option("--trace" ,action="store_true",dest="trace",default=False,help="A utiliser pour declencher un mode verbeux. Default=False")
    parser.add_option("--user1" , dest="user", help='user Default=user1', default="audiologys")
    parser.add_option("--pass1" , dest="pwd1", help='pwd Default=pass1', default="audiologys")
    parser.add_option("--db1"   , dest="db1"  , help='db Default=db1', default="audiologys_utf8")
    parser.add_option("--port1"   , dest="port1"  , help='port Default=3307', default=3307)

    parser.add_option("--output", dest="csv_filename", default='products.csv', help='filename for csv output Default=output.csv')
    parser.add_option("-t", "--type", dest="product_type", default="optionnal", help="set this option to 'appareil' or 'optionnal' depending on type of product")
    parser.add_option("-U", "--upsells", action="store_true", dest="upsell", default=False, help="set this option to generate upsell requests")

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
    UPSELL = opts.upsell
    PRODUCT_TYPE  = str(opts.product_type)

    # create a connection handler
    # 2 connection to 2 different databases
    myconn1 = connector("127.0.0.1", port1, user1, pass1, db1 )
    #myconn2 = connector("127.0.0.1", 3306, "user", "passwd", "db_name" )

    # create instance of myops class
    print("Create instance...")
    if UPSELL:
        controller = myops(myconn1, "liste-id-sku-NO-DELETE-may14.csv")
    else:
        controller = myops(myconn1)

    print("Initializing...")
    controller.initialize()

    ## FOR TESTING
    
    if UPSELL:
        print("Extracting links between products and optionnal products for upsells linking...")
        controller.extract_liaisons("update_requests.txt")


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
        
        """
            indiquer le nom du champ dans la base lmb ou encore les champs suivants qui on un traitement spécial

            image -> renvoie l'url de l'image qui sera récupérée par WP à l'import
            images_product_gallery-> renvoie l'url des images d'ordre > 1 pour gallery d'images
            lib_article_clean -> génére le libellé de l'article nettoyé
        """

        # Appareils auditifs
        #fields_list = ["ref_article", "lib_article", "desc_courte", "desc_longue", "modele", "ref_constructeur", "paa_ht", "id_tva", "dispo", "ref_article", ""]
        
        fields_list = ["ref_article", "lib_article", "desc_courte", "desc_longue", "paa_ht", "dispo" ]
        fields_list_csv = ["ref_article", "ref_article", "lib_article", "lib_article_clean", "image", "images_product_gallery", "paa_ht", "dispo"]
        #fields_list_csv = ["ref_article", "image", "images_product_gallery"]
        
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

    caracs ...



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



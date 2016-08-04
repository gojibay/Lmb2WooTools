#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'lgp'

import pymysql
import logging
from optparse import OptionParser

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

    def retrieve_fields(self, table="", fields_to_retrieve=[], filter_on={}):
        """
        This function retrieves the fields given in 'fields_to_retrieve' of the entries having 'key' and matching values 'filter_on'

        ref_article
        filter ref_art_categ = A.C-000000-00003
        desc_courte
        desc_longue
        """

        # retrieve fields to get data from
        fields = ""
        for f in fields_to_retrieve:
            fields = fields + f + ","
        fields = fields.strip(',')

        # retrieve fields and value to filter on
        # first versin on one only value
        #print(filter_on["ref_art_categ"])
        filter = ""
        for key,value in filter_on.items():
            filter = key + " = '" + value + "'"


        # generate MYSQL request
        myrequest = "SELECT " + fields + " "
        myrequest = myrequest + " FROM " + table + " "
        myrequest = myrequest + " WHERE " + filter
        myrequest = myrequest + " ;"

        #print(myrequest)

        self.connector.cursor.execute(myrequest)
        #print(self.cursor.description)

        # retrieve all data in array
        result = self.connector.cursor.fetchall()
        return result

    def write_fields(self, table="", key_field="ref_article", data=[]):
        """
        This function writes the data 'data' in table 'table'

        exemple data : [
                        {'desc_longue': b'Placer le lien vers la fiche PDF constructeur<br>',
                        'desc_courte': b'appareil auditif dual V OTICON',
                        'ref_article': 'A-000000-00005'}
                        ]

        """
        # will store all the requests
        myrequests = []

        key_field_value = ""

        # generate mysql requests
        for elt in data:
            cols_values = ""
            myrequest = ""
            myrequest_insert = ""
            for k,v in elt.items():
                if k != key_field:
                    forcedec_v = self.force_decode(v)
                    forcedec_v.encode("iso-8859-1")
                    forcedec_v = forcedec_v.replace("'", "\\'")
                    cols_values = cols_values + k + "='" + str(forcedec_v) + "',"

                else:
                    key_field_value = str(v)
                    # used once if table empty (for test purpose)
                    myrequest_insert = "INSERT INTO "+table+"("+key_field+") VALUES ('"+ key_field_value +"')"
            cols_values = cols_values.strip(',')

            # generate MYSQL request
            myrequest = "UPDATE " + table + " "
            myrequest = myrequest + " SET " + cols_values + " "
            myrequest = myrequest + " WHERE " + key_field +"='" + key_field_value  + "' "
            myrequest = myrequest + " ;"

            #myrequests.append(myrequest_insert)
            myrequests.append(myrequest)




        for req in myrequests:
            #print(req)
            self.connector.cursor.execute(req)
            self.connector.conn.commit()
            pass

    def force_decode(self, string, codecs=['cp1252', 'utf8', 'iso-8859-1']):
        for i in codecs:
            try:
                s = string.decode(i)
                return s
            except:
                pass

        logging.warn("cannot decode url %s" % ([string]))


if __name__ == '__main__':

    usage = """

        Script qui extrait des données de la db1 et génère soit :
            - les requêtes sql pour l'update d'une deuxième base db2
            - le fichier csv contenant les datas

        %prog --user1 username --pass1 pwd --db1 dbname --user2 username --pass2 pwd --db2 dbname

    """

    parser=OptionParser(usage=usage)
    parser.add_option("--trace" ,action="store_true",dest="trace",default=False,help="A utiliser pour declencher un mode verbeux. Default=False")
    parser.add_option("--user1" , dest="user1", help='user Default=user1')
    parser.add_option("--pwd1" , dest="pwd1", help='pwd Default=pass1')
    parser.add_option("--db1"   , dest="db1"  , help='db Default=db1')
    parser.add_option("--user2" , dest="user2", help='user Default=user2')
    parser.add_option("--pwd2" , dest="pwd2", help='pwd Default=pass2')
    parser.add_option("--db2"   , dest="db2"  , help='db Default=db2')
    parser.add_option("--output", dest="csv_filename", default='output.csv', help='filename for csv output Default=output.csv')

    (opts,args) = parser.parse_args()

    if len(args) > 0:
        mode = args[0].lower()

    # db1 info
    user1 = str(opts.user1)
    pwd1 = str(opts.pwd1)
    db1   = str(opts.db1)


    # db2 info
    user2 = str(opts.user2)
    pwd2 = str(opts.pwd2)
    db2   = str(opts.db2)

    csv_filename = str(opts.csv_filename)

    # create a connection handler
    # 2 connection to 2 different databases
    myconn1 = connector("127.0.0.1", 3307, user1, pwd1, db1 )
    myconn2 = connector("127.0.0.1", 3307, user2, pwd2, db2 )

    # 2 instances of myops class
    myops_read  = myops(myconn1)
    myops_write = myops(myconn2)

    # launch task function
    # 1/ retrieve data
    data = myops_read.retrieve_fields("articles", ["ref_article", "desc_courte", "desc_longue"], {"ref_art_categ" : "A.C-000000-00003" })

    # 2/ write data
    myops_write.write_fields("articles_write_utf8", "ref_article", data)

    # close cursor and connection
    # connexion 1
    myconn1.cursor.close()
    myconn1.conn.close()
    # connexion 2
    myconn2.cursor.close()
    myconn2.conn.close()

    pass

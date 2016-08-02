#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'lgp'

import pymysql
import logging

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

    # create a connection handler
    # 2 connection to 2 different databases
    myconn1 = connector("127.0.0.1", 3306, "user", "passwd", "db_name" )
    myconn2 = connector("127.0.0.1", 3306, "user", "passwd", "db_name" )

    # 2 instances of myops class
    myops_read  = myops(myconn1)
    myops_write = myops(myconn2)

    # launch task function
    data = myops_read.retrieve_fields("articles", ["ref_article", "desc_courte", "desc_longue"], {"ref_art_categ" : "A.C-000000-00003" })
    myops_write.write_fields("articles_write_utf8", "ref_article", data)

    # close cursor and connection
    # connexion 1
    myconn1.cursor.close()
    myconn1.conn.close()
    # connexion 2
    myconn2.cursor.close()
    myconn2.conn.close()

    pass

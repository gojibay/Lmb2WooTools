#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'lgp'

import sys

class UserInfoHandler:

    def __init__(self, line):
        self.line = line
        self.data = self.line.split(';')
        self.l_validity = self.data[0]
        self.l_col2 = self.data[1]
        self.l_libelle = self.data[2]
        self.l_username = self.data[3]
        self.l_website = self.data[4]
        self.l_col6 = self.data[5]
        self.l_vip = self.data[6]
        self.l_php_version = self.data[7]
        self.l_col9 = self.data[8]
        self.l_db_name = self.data[9]
        self.l_db_user = self.data[10]
        self.l_db_pass = self.data[11]

    def get_db_name(self):
        return self.l_db_name

    def get_db_user(self):
        return self.l_db_user

    def get_db_pass(self):
        return self.l_db_pass


class GenerateMysqlDbRequests:
    """
        Class that generates mysql requests

    """
    def __init__(self, db_name, db_user, db_pass, host='localhost'):
        self.db_name = db_name
        self.db_user = db_user
        self.db_pass = db_pass
        self.host = host


    def gen_user_create(self):
        """
            Generates user create request
            :return: request
        """
        return("CREATE USER '"+ self.db_user +"'@'"+self.host+"' IDENTIFIED WITH '"+self.db_pass+"';")

    def gen_grant_usage(self):
        """
            Generates grant usage request
            :return: request
        """
        return("GRANT USAGE ON *.* TO '"+ self.db_user +"'@'"+self.host+"' REQUIRE NONE WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0;")

    def gen_db_create(self):
        """
            Generates db create request
            :return: request
        """
        return("CREATE DATABASE IF NOT EXISTS `"+ self.db_name +"`;")

    def gen_grant_all(self):
        """
            Generates grant all request
            :return: request
        """
        return("GRANT ALL PRIVILEGES ON `"+ self.db_name +"`.* TO '"+ self.db_user +"'@'"+self.host+"';")

    def gen_alter_pass(self):
        return("SET PASSWORD FOR '"+ self.db_user +"'@'"+self.host+"' = PASSWORD('"+self.db_pass+"');")

    def gen_all(self):
        req = self.gen_user_create()  + "\n"
        req += self.gen_grant_usage() + "\n"
        req += self.gen_db_create()   + "\n"
        req += self.gen_grant_all()   + "\n"
        return(req)

def read_lines(infile):
    """ Lit un fichier
    et retourne une list d'instances de Example
    """
    stream = open(infile)
    user_data_list = []
    user_data = None
    while 1:
        line = stream.readline()
        if not line:
            break
        line = line[0:-1]
        if line.startswith("+"):
            user_data = UserInfoHandler(line)
            user_data_list.append(user_data)

    return user_data_list



if __name__ == '__main__':

    # exemple de data du fichier d'entrée
    line = "+;;Piles auditives;piles;mon.site.fr;;vip5;php5;;piles_presta;piles_presta;password"

    if (len(sys.argv) <= 1):
        exit("Il manque un argument")

    # generation de la liste de handlers
    lines_handler = read_lines(sys.argv[1])

    # parcourt de la liste et affichage des requets
    for h in lines_handler:
        g = GenerateMysqlDbRequests(h.get_db_name(), h.get_db_user(), h.get_db_pass())
        #print(g.gen_all())
        print(g.gen_alter_pass())

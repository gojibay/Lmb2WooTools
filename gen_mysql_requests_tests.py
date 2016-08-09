import unittest
import gen_mysql_requests

class user_info_handlerTest(unittest.TestCase):

    def setUp(self):
        # variables to test against
        self.line = 'col1;col2;col3;col4;col5;col6;col7;col8;col9;col10;col11;col12'
        self.data = self.line.split(';')

        # create instance of object to test
        self.handler = gen_mysql_requests.UserInfoHandler(self.line)

    def tearDown(self):
        pass

    def test_user_info_handler_can_read_a_line_and_retriveve_correct_elements(self):
        # Agent reads a line
        self.assertEqual(self.handler.line, self.line)

        # Agent splits a line
        for i in range(len(self.handler.data)):
            self.assertEqual(self.handler.data[i], self.data[i])

        # Agent displays each element of data present the line
        # let's check the good data is present in each field
        self.assertEqual(self.handler.get_db_name(), 'col10')
        self.assertEqual(self.handler.get_db_user(), 'col11')
        self.assertEqual(self.handler.get_db_pass(), 'col12')

        # elements retrieved should be correctly placed in input line in the followinf format

#        import time
#        time.sleep(2)


        #self.fail('Finish the test!')

class GenerateMysqlDbRequestsTest(unittest.TestCase):

    def setUp(self):
        # variables to test against
        self.db_name = "test_db_name"
        self.db_user = "test_db_user"
        self.db_pass = "test_db_pass"
        self.host    = "localhost"
        self.req_create_user = "CREATE USER '"+self.db_user+"'@'"+self.host+"' IDENTIFIED WITH mysql_native_password AS '"+self.db_pass+"';"
        self.req_grant_usage = "GRANT USAGE ON *.* TO '"+self.db_user+"'@'"+self.host+"' REQUIRE NONE WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0;"
        self.req_create_db   = "CREATE DATABASE IF NOT EXISTS `"+self.db_name+"`;"
        self.req_grant_all   = "GRANT ALL PRIVILEGES ON `"+self.db_name+"`.* TO '"+self.db_user+"'@'"+self.host+"';"
        self.req_full = self.req_create_user + "\n" + self.req_grant_usage + "\n" + self.req_create_db + "\n" + self.req_grant_all + "\n"

        # create instance of object to test
        self.gen = gen_mysql_requests.GenerateMysqlDbRequests("test_db_name", "test_db_user", "test_db_pass")


    def tearDown(self):
        pass

    def test_user_and_db_create_request(self):
        # Agent generates the requests
        self.assertEqual(self.gen.gen_user_create(), self.req_create_user)
        self.assertEqual(self.gen.gen_grant_usage(), self.req_grant_usage)
        self.assertEqual(self.gen.gen_db_create(), self.req_create_db)
        self.assertEqual(self.gen.gen_grant_all(), self.req_grant_all)

        self.assertEqual(self.gen.gen_all(), self.req_full)

        # elements retrieved should be correctly placed in input line in the followinf format

#        import time
#        time.sleep(2)


        #self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')


import pymysql, os
import configparser as cparser

base_dir = os.path.dirname(os.path.dirname(__file__))
file_path = base_dir + "/db_config.ini"
cf = cparser.ConfigParser()
cf.read(file_path)
host = cf.get("mysqlconf", "host")
port = cf.get("mysqlconf", "port")
db = cf.get("mysqlconf", "db_name")
user = cf.get("mysqlconf", "user")
password = cf.get("mysqlconf", "password")
class DB:
    def __init__(self):
            try:
                self.conn = pymysql.connect(host=host,
                                            user=user,
                                            password=password,
                                            db=db,
                                            charset='utf8mb4',
                                            cursorclass=pymysql.cursors.DictCursor) #获取字典格式的数据

            except pymysql.err.OperationalError as e:
                print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    def clear(self, table_name):
        real_sql = "delete from %s;" % table_name
        with self.conn.cursor() as cursor:
                cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
                cursor.execute(real_sql)
        self.conn.commit()

    def insert(self, table_name, table_data):
        for key in table_data:
            table_data[key] ="'" + str(table_data[key]) + "'"
        key = ",".join(table_data.keys())
        # key = list(map(key_c  l, key1))
        value = ",".join(table_data.values())
        #real_sql =  "INSERT INTO " + table_name + " (" + key + ") VALUES (" + value + ")"
        real_sql = "insert into %s (%s) values (%s)" % (table_name, key, value)
        with self.conn.cursor() as cursor:
            print(real_sql)
            cursor.execute(real_sql)
        self.conn.commit()


    def close(self):
        self.conn.close()

if __name__ == '__main__':
    a = DB()
    data_guest = {'name': 'apd', 'limit': '2222', 'address': 'wqwq', 'status': 1}
    a.insert('sign_event', data_guest)
    a.close()
    # ALTER TABLE  `sign_event` CHANGE  `start_time`  `start_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    # ALTER TABLE  `sign_guest` CHANGE  `create_time`  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP



    # conn = pymysql.connect(host=host,user=user,password=password,db=db,cursorclass=pymysql.cursors.DictCursor)
# cursor = conn.cursor()
# cursor.execute("select * from sign_guest")
# r = cursor.fetchmany(1)
# for i in r:
#     for key in i:
#         i[key] = str(i[key])
#         print(type(i[key]))
#         print(i[key])
#
#     print(",".join(i.keys(  )))
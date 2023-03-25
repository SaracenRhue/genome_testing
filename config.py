import pymysql
# Establish a connection to the MySQL server
connection = pymysql.connect(
    host='genome-euro-mysql.soe.ucsc.edu',
    port=3306,
    user='genome',
    db='hgcentral',
    cursorclass=pymysql.cursors.DictCursor
)
from config import connection
import utils

print(utils.get_table_names())
#hubSearchText table to big
utils.to_json('hubSearchText')

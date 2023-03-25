from config import connection
import utils

print(utils.get_table_names())
utils.to_json('defaultDb')
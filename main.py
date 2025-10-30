from core.ORM import ORM
from core.settings import config
from core.models import *

database = ORM(config["DATABASE_URL"])

if __name__ == "__main__":
    # database.delete_table()
    # database.create_table()
    database.insert_buyer_data()
    database.insert_product_data()
    database.insert_categorie_data()
    database.insert_order_data()
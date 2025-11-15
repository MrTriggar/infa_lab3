from core.ORM import ORM

def export_command():
    results = ORM.show_export_menu()
    if results:
        print("Все успешно.")

if __name__ == "__main__":
    # ORM.delete_table()
    # ORM.create_table()
    # ORM.insert_categorie_data()
    # ORM.insert_seller_data()
    # ORM.insert_buyer_data()
    # ORM.insert_product_data()
    # ORM.insert_order_data()
    export_command()
    # ORM.select_data()
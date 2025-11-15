from core.models import *
from core.exporter import DatabaseExporter

class ORM:
    # def __init__(self, database_url):
    #     self.engine = create_engine(
    #         url=database_url,
    #         echo=True
    #     )
    #     self.localsession = sessionmaker(self.engine)
    #     self.tables = Tables

    @staticmethod
    def create_table():
        Base.metadata.create_all(engine)

    @staticmethod
    def delete_table():
        Base.metadata.drop_all(engine)

    @staticmethod
    def insert_product_data():
        with localsession() as session:
            product1 = Product(product_name="Книга", price=600, categorie_id=1, seller_id=1)
            product2 = Product(product_name="нига", price=1600, categorie_id=2, seller_id=1)
        session.add_all([product1, product2])
        session.commit()

    @staticmethod
    def insert_buyer_data():
        with localsession() as session:
            buyer1 = Buyer(buyer_firstname="Арч", buyer_surname="Линукс")
            buyer2 = Buyer(buyer_firstname="Я", buyer_surname="Куплю")
        session.add_all([buyer1, buyer2])
        session.commit()

    @staticmethod
    def insert_seller_data():
        with localsession() as session:
            seller = Seller(seller_name="Вроде_ровно")
        session.add(seller)
        session.commit()

    @staticmethod
    def insert_categorie_data():
        with localsession() as session:
            book_categorie1 = Categories(categorie_name="литература")
            book_categorie2 = Categories(categorie_name="что")
        session.add_all([book_categorie1, book_categorie2])
        session.commit()

    @staticmethod
    def insert_order_data():
        with localsession() as session:
            order = Order(buyer_id=1, order_price=1200, count_of_products=2, product_id=1)
        session.add(order)
        session.commit()

    @staticmethod
    def select_data():
        with localsession() as session:
            query = select(
                Buyer.id,
                Buyer.buyer_firstname,
                Buyer.buyer_surname
            ).select_from(Buyer)

            res = session.execute(query).all()
        session.commit()
        for buyer_id, buyer_name, buyer_surname in res:
            print(f"""ID покупателя: {buyer_id}\n
    полное имя: {buyer_name} {buyer_surname}\n""")

    @staticmethod
    def update_buyer_data(buyer_id: int = 2, new_firstname: str = "Не"):
        with localsession() as session:
            buyer_ya = session.get(Buyer, buyer_id)
            buyer_ya.buyer_firstname = new_firstname
        session.commit()

    @staticmethod
    def get_order_detail():
        with localsession() as session:
            query = select(
                Order.id,
                Order.order_price,
                Order.count_of_products,
                Buyer.buyer_firstname
            ).select_from(Order).join(Buyer.id)

            res = session.execute(query).all()

    @staticmethod
    def export_data(table_name=None, include_relations=False):
        """
        Экспортирует данные в JSON, CSV, XML, YAML
        """
        exporter = DatabaseExporter()

        if table_name:
            # Экспорт конкретной таблицы
            return exporter.export_table(table_name, include_relations)
        else:
            # Экспорт всех таблиц
            return exporter.export_all_tables()

    @staticmethod
    def show_export_menu():
        """
        Показывает меню для выбора таблицы для экспорта
        """
        tables = {
            '1': ('buyers', 'Покупатели'),
            '2': ('sellers', 'Продавцы'),
            '3': ('categories', 'Категории'),
            '4': ('products', 'Товары'),
            '5': ('orders', 'Заказы'),
            '6': ('all', 'Все таблицы')
        }

        exporter = DatabaseExporter()

        print("\n" + "=" * 50)
        print("ЭКСПОРТ ДАННЫХ В ФАЙЛЫ")
        print("=" * 50)

        for key, (table, description) in tables.items():
            print(f"{key}. {description} ({table})")

        choice = input("\nВыберите таблицу для экспорта: ").strip()

        if choice in tables:
            table_name, description = tables[choice]

            if table_name == 'all':
                return exporter.export_all_tables()
            else:
                include_relations = input(
                    f"Включать связанные данные для {description}? (y/n): "
                ).strip().lower() == 'y'

                return ORM.export_data(table_name, include_relations)
        else:
            print("Неверный выбор!")
            return None
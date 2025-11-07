from sqlalchemy import create_engine, select
from core.database import Base, engine, localsession
from core.models import *
from core.dataclasses import Tables

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
                Buyer.first_name,
                Buyer.second_name
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
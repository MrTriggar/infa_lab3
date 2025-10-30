from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select
from core.database import Base
from core.dataclasses import Tables

class ORM:
    def __init__(self, database_url):
        self.engine = create_engine(
            url=database_url,
            echo=True
        )
        self.localsession = sessionmaker(self.engine)
        self.tables = Tables

    def create_table(self):
        Base.metadata.create_all(self.engine)

    def delete_table(self):
        Base.metadata.drop_all(self.engine)

    def insert_product_data(self):
        with self.localsession() as session:
            product1 = self.tables.Product(product_name="Книга", price=600, categorie_name="литература")
            product2 = self.tables.Product(product_name="нига", price=1600, categorie_name="что")
        session.add_all([product1, product2])
        session.commit()

    def insert_buyer_data(self):
        with self.localsession() as session:
            buyer1 = self.tables.Buyer(buyer_firstname="Арч", buyer_surname="Линукс")
            buyer2 = self.tables.Buyer(buyer_firstname="Я", buyer_surname="Куплю")
        session.add_all([buyer1, buyer2])
        session.commit()

    def insert_seller_data(self):
        with self.localsession() as session:
            seller = self.tables.Seller(seller_name="Вроде_ровно", product_id=1)
        session.add_all(seller)
        session.commit()

    def insert_categorie_data(self):
        with self.localsession() as session:
            book_categorie = self.tables.Categories(categorie_name="литература")
        session.add_all(book_categorie)
        session.commit()

    def insert_order_data(self):
        with self.localsession() as session:
            order = self.tables.Order(bayer_id=1, order_price=1200, count_of_products=2)
        session.add_all(order)
        session.commit()

    def select_data(self):
        with self.localsession() as session:
            query = select(
                self.tables.Buyer.id,
                self.tables.Buyer.first_name,
                self.tables.Buyer.second_name
            ).select_from(self.tables.Buyer)

            res = session.execute(query).all()
            session.commit()
            for buyer_id, buyer_name, buyer_surname in res:
                print(f"""ID покупателя: {buyer_id}\n
        полное имя: {buyer_name} {buyer_surname}\n""")

    def update_buyer_data(self, buyer_id: int = 2, new_firstname: str = "Не"):
        with self.localsession() as session:
            buyer_ya = session.get(self.tables.Buyer, buyer_id)
            buyer_ya.buyer_firstname = new_firstname
        session.commit()
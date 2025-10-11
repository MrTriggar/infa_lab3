from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg://postgres_user:postgres_password@localhost:5430/postgres_db"

engine = create_engine(
    url=DATABASE_URL,
    echo=True
)

localsession = sessionmaker(engine)

class Base(DeclarativeBase):
    pass


class IVT(Base):
    __tablename__ = "ivt"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    second_name: Mapped[str]


def create_table():
    Base.metadata.create_all(engine)

def delete_table():
    Base.metadata.drop_all(engine)

def insert_data():
    with localsession() as session:
        student = IVT(first_name="Николай", second_name="Аносов")
        session.add_all([student])
        session.commit()


if __name__ == "__main__":
    delete_table()




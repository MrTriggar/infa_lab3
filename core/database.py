from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import create_engine, select, func

DATABASE_URL = "postgresql+psycopg://postgres_user:postgres_password@localhost:5430/postgres_db"

engine = create_engine(
    url=DATABASE_URL,
    echo=True
)

localsession = sessionmaker(engine)

class Base(DeclarativeBase):
    pass


# def create_table():
#     Base.metadata.create_all(engine)
#
# def delete_table():
#     Base.metadata.drop_all(engine)
#
# def insert_data():
#     with localsession() as session:
#         student1 = IVT(first_name="Николай", second_name="Аносов")
#         student2 = IVT(first_name="Заур", second_name="Бабаев")
#         student3 = IVT(first_name="Данила", second_name="Я ЛЮБЛЮ ЛИНУКС")
#
#         session.add_all([student1, student2, student3])
#         session.commit()
#
# def select_data():
#     with localsession() as session:
#         query = select(
#             IVT.id,
#             IVT.first_name,
#             IVT.second_name
#         ).select_from(IVT)
#
#         res = session.execute(query).all()
#         session.commit()
#
#         for student_id, student_name, student_surname in res:
#             print(f"""ID студента: {student_id}\n
# полное имя: {student_name} {student_surname}\n""")
#








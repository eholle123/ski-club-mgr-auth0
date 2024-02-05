from application.model import SkiPass
from application.config import settings

from sqlmodel import Session, SQLModel, create_engine


engine = create_engine(settings.database_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_ski_passes():  
    ski_pass_1 = SkiPass(serial_number="82343581")
    ski_pass_2 = SkiPass(serial_number="82343582")
    ski_pass_3 = SkiPass(serial_number="82343583")

    with Session(engine) as session:  
        session.add(ski_pass_1)  
        session.add(ski_pass_2)
        session.add(ski_pass_3)

        session.commit()  
    


def main():  
    create_db_and_tables()  
    create_ski_passes()  


if __name__ == "__main__":  
    main()
from sqlmodel import Session, SQLModel, create_engine

sqlite_file_name = r"D:\PROJECTS\trems\mpnapi\database\data_sampel.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def get_db():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
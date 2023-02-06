import sqlalchemy as sa
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as dec


SqlAlchemyBase = dec.declarative_base()


class DatabaseError(Exception):
    pass


class NotConnect(DatabaseError):
    pass


class Database:
    __instance = None
    __factory = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None or cls.__factory is None:
            raise NotConnect("База данных не подключена.")
        return cls.__instance

    def __enter__(self):
        return self.__factory()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    @classmethod
    def connect(cls, filepath: str):
        conn_str = f'sqlite:///{filepath.strip()}?check_same_thread=False'
        engine = sa.create_engine(conn_str, echo=False)
        factory = orm.sessionmaker(bind=engine)
        from . import _all_models
        SqlAlchemyBase.metadata.create_all(engine)
        cls.__factory = factory
        cls.__instance = super().__new__(cls)


if __name__ == "__main__":
    Database.connect("../db/db.db")


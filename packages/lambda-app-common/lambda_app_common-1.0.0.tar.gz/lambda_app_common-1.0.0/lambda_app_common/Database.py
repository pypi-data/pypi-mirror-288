import json
from abc import abstractmethod, ABC

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .env_vars import LOCAL, LOG_DB_TRANSACTIONS, DB_CREDENTIALS

DB = json.loads(DB_CREDENTIALS)

if LOCAL:
    print("Is Local: ", LOCAL)
    DB.update({
        "host": 'localhost',
        "port": 5433
    })

DB_CONNECTION_URL = f"{DB['engine']}://{DB['username']}:{DB['password']}@{DB['host']}:{DB['port']}/{DB['database']}"


class Database(ABC):

    def __init__(self, service_name):
        self.service_name = service_name

    @abstractmethod
    def connect(self):
        pass


class PgsqlDatabase(Database):

    def connect(self):
        print("#@#" * 33)
        print(
            f"<=^^^^^^^^^^^^^^^^^^^^^^^^ {self.service_name} Connecting to {DB_CONNECTION_URL} ^^^^^^^^^^^^^^^^^^^^^^^^ => ")
        engine = create_engine(DB_CONNECTION_URL, echo=LOG_DB_TRANSACTIONS)
        Session = sessionmaker(bind=engine)
        print("<=^^^^^^^^^^^^^^^^^^^^^^^^  DB POSTGRESQL Engine Initialized (CONNECTED) ^^^^^^^^^^^^^^^^^^^^^^^^ => ")
        print("#@#" * 33)
        return Session()

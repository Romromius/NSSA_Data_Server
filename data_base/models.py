from datetime import datetime
from sqlalchemy import *
from werkzeug.security import generate_password_hash, check_password_hash
from data_base.db_session import SqlAlchemyBase, create_session


class CCPlayer(SqlAlchemyBase):
    __tablename__ = "cc_player"

    id = Column(Integer, primary_key=True, autoincrement=True)
    _coins = Column(Float, default=0)
    _income = Column(Float, default=0)

    _last_check = Column(DateTime, default=datetime.now())

    _hashed_password = Column(String)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.hashed_password, password)

    def add_coins(self, value: int):
        self._coins += value

    def increase_income(self) -> bool:
        if self._coins > self._income * 100:
            self._income += 1
            self._coins -= self._income * 100
            return True
        else:
            return False

    def get_coins(self) -> int:
        seconds = (datetime.now() - self._last_check).seconds
        self._coins += float(self._income * seconds)
        self._last_check = datetime.now()
        return int(self._coins)

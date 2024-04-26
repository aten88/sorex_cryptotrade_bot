from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CoinValues(Base):
    """" Модель пороговых значений. """
    __tablename__ = 'coin_values'

    id = Column(Integer, primary_key=True)
    coin_name = Column(String)
    min_price = Column(Integer)
    max_price = Column(Integer)
    user_id = Column(Integer)

    def __repr__(self):
        return (
            f"<CoinValues(coin_name='{self.coin_name}', "
            f"min_price='{self.min_price}', max_price='{self.max_price}', "
            f"user_id='{self.user_id}')>"
        )

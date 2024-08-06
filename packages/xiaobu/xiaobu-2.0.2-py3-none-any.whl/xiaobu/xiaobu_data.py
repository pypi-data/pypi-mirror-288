import json

from sqlalchemy import create_engine, Column, Integer, String, and_, Date, Numeric, UniqueConstraint
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.testing import db

# 创建数据库连接
engine = create_engine('mysql+pymysql://root:XBJmysql126%40@192.168.1.22:3306/test_data?charset=utf8mb4')
Base = declarative_base()
Session = sessionmaker(bind=engine)
data_session = Session()


# 店铺
class TmPromotion(Base):
    __tablename__ = 'data_tm_link_promotion'

    id = Column(Integer, primary_key=True)
    shop_id = Column(Integer, nullable=False)
    promotionId = Column(String(20), nullable=False)
    date = Column(Date, nullable=False)
    type = Column(String(10), nullable=False)
    charge = Column(Numeric(15, 2), nullable=False)
    alipayInshopAmt = Column(Numeric(15, 2), nullable=False)
    click = Column(Integer, nullable=False)
    adPv = Column(Integer, nullable=False)

    @staticmethod
    def upsert(data: list, date, shop_id):
        data_session.query(TmPromotion).filter(and_(TmPromotion.date == date, TmPromotion.shop_id == shop_id, TmPromotion.promotionId == data['promotionId'])).delete()
        data_session.add_all(data)
        data_session.commit()


class TmCTB(Base):
    __tablename__ = 'data_tm_link_ctb'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    shop_id = Column(Integer, nullable=False)
    link_id = Column(String(20), nullable=False)

    sales = Column(Numeric(15, 2), nullable=False)
    refund = Column(Numeric(15, 2), nullable=False)
    replenish = Column(Numeric(15, 2), nullable=False)
    replenish_count = Column(Integer, nullable=False)

    @staticmethod
    def upsert(data: list, date, shop_id):
        data_session.query(TmCTB).filter(and_(TmCTB.date == date, TmCTB.shop_id == shop_id, TmCTB.link_id == data['link_id'])).delete()
        data_session.add_all(data)
        data_session.commit()


class PddPlatform(Base):
    __tablename__ = 'data_pdd_platform'

    id = Column(Integer, primary_key=True)
    shop_id = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)

    deal_amount = Column(Numeric(10, 2), nullable=False)
    refund_amount = Column(Numeric(10, 2), nullable=False)
    dd_search = Column(Numeric(10, 2), nullable=False)
    dd_scene = Column(Numeric(10, 2), nullable=False)
    fxt = Column(Numeric(10, 2), nullable=False)
    qztg = Column(Numeric(10, 2), nullable=False)
    bztg = Column(Numeric(10, 2), nullable=False)
    sptg = Column(Numeric(10, 2), nullable=False)

    __table_args__ = (
        UniqueConstraint("shop_id", "date", name='unique_shop_id_date'),
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def upsert(data):
        data_session.query(PddPlatform).filter(and_(PddPlatform.date.in_([i.date for i in data]),
                                                    PddPlatform.shop_id.in_([i.shop_id for i in data]))).delete()
        data_session.add_all(data)
        data_session.commit()


class RedisLike(Base):
    __tablename__ = 'redis_like'

    key = Column(String(50), primary_key=True)
    value = Column(String(500))

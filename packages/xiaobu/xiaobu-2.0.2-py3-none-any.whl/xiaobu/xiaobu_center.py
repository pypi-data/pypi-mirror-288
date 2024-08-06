# coding=utf-8
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from xiaobu.api.shop import get_shop_list
from xiaobu.xiaobu_erp import ErpSession

# 创建数据库连接
engine = create_engine('mysql+pymysql://root:XBJmysql126%40@192.168.1.22:3306/test_center?charset=utf8mb4')
Base = declarative_base()
Session = sessionmaker(bind=engine)
center_session = Session()
erp_session = ErpSession()


# 店铺
class Shop(Base):
    __tablename__ = 'center_shop'

    id = Column(Integer, primary_key=True)
    erp_id = Column(Integer, nullable=False, unique=True)
    shop_name = Column(String(50), nullable=False, unique=True)
    platform = Column(String(10), nullable=False)
    is_open = Column(Integer, nullable=False, default=1)
    cookie = Column(Text(500), nullable=True)
    account = Column(String(20), nullable=True)
    password = Column(String(20), nullable=True)
    update_time = Column(DateTime, nullable=True)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.shop_name)


def create_shop(shop_name, account, password):
    # 查询erp_shop_id
    shop_list = erp_session.erp_send(get_shop_list(shop_name=shop_name))
    if not shop_list:
        raise Exception('shop not found: %s' % shop_name)
    erp_id = shop_list[0]['shopId']
    platform = shop_list[0]['shopSite']
    shop = Shop(shop_name=shop_name,
                platform=platform,
                erp_id=erp_id,
                account=account,
                password=password,
                update_time=datetime.now())
    center_session.add(shop)
    center_session.commit()


def refresh_cookie(shop_id, cookie):
    shop = center_session.query(Shop).filter(Shop.id == shop_id).first()
    shop.cookie = cookie
    shop.update_time = datetime.now()
    center_session.commit()


# 链接绑定
class TmBinds(Base):
    __tablename__ = 'center_binds'

    id = Column(Integer, primary_key=True)
    emp_id = Column(Integer, nullable=False)
    shop_id = Column(Integer, nullable=False)
    link_id = Column(String(20), nullable=False, unique=True)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.link_id)


# 链接绑定记录
class TmBindsLog(Base):
    __tablename__ = 'center_binds_log'

    id = Column(Integer, primary_key=True)
    emp_id = Column(Integer, nullable=True)
    shop_id = Column(Integer, nullable=False)
    link_id = Column(String(20), nullable=False, unique=False)
    date = Column(DateTime, nullable=False)


# 员工
class Employee(Base):
    __tablename__ = 'center_employee'

    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False)
    account = Column(String(10), nullable=False)
    password = Column(String(300), nullable=False)
    status = Column(Integer, nullable=False, default=1)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.name)

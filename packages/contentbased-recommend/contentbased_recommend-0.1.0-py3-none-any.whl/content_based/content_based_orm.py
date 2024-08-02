from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Create a base class for declarative class definitions
Base = declarative_base()
Session = None


# Define ORM models
class SKUMASTER(Base):
    __tablename__ = 'SKUMASTER'
    SKU_KEY = Column(Integer, primary_key=True)
    SKU_CODE = Column(String)
    SKU_NAME = Column(String)
    SKU_ICDEPT = Column(Integer, ForeignKey('ICDEPT.ICDEPT_KEY'))
    SKU_ICCAT = Column(Integer, ForeignKey('ICCAT.ICCAT_KEY'))

    icdept = relationship("ICDEPT", back_populates="skus")
    iccat = relationship("ICCAT", back_populates="skus")


class ICCAT(Base):
    __tablename__ = 'ICCAT'
    ICCAT_KEY = Column(Integer, primary_key=True)
    ICCAT_CODE = Column(String)
    ICCAT_NAME = Column(String)

    skus = relationship("SKUMASTER", back_populates="iccat")


class ICDEPT(Base):
    __tablename__ = 'ICDEPT'
    ICDEPT_KEY = Column(Integer, primary_key=True)
    ICDEPT_CODE = Column(String)
    ICDEPT_THAIDESC = Column(String)

    skus = relationship("SKUMASTER", back_populates="icdept")


class TRANSTKD(Base):
    __tablename__ = 'TRANSTKD'
    TRD_TRH = Column(String, primary_key=True)
    TRD_GOODS = Column(String)
    TRD_SKU = Column(String, ForeignKey('SKUMASTER.SKU_CODE'))
    TRD_QTY = Column(Integer)
    TRD_SH_NAME = Column(String)
    TRD_KEY = Column(Integer)
    TRD_KEYIN = Column(String)
    TRD_NM_PRC = Column(String)
    TRD_UTQQTY = Column(Integer)
    TRD_UTQNAME = Column(String)

    sku = relationship("SKUMASTER", back_populates="transtkd")


class GOODSMASTER(Base):
    __tablename__ = 'GOODSMASTER'
    GOODS_KEY = Column(Integer, primary_key=True)
    GOODS_SKU = Column(String, ForeignKey('SKUMASTER.SKU_CODE'))
    GOODS_CODE = Column(String)
    GOODS_ENABLE = Column(String)
    GOODS_P_ENABLE = Column(String)

    sku = relationship("SKUMASTER", back_populates="goods")


SKUMASTER.transtkd = relationship("TRANSTKD", back_populates="sku")
SKUMASTER.goods = relationship("GOODSMASTER", back_populates="sku")


def configure_database(connection_url: str):
    global Session
    # Create SQLAlchemy engine
    engine = create_engine(connection_url)
    # Create a sessionmaker
    Session = sessionmaker(bind=engine)
    # Create the tables in the database (if not exists)
    Base.metadata.create_all(engine)

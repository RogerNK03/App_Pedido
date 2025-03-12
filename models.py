from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

CONN = "sqlite:///projeto2.db"

engine = create_engine(CONN, echo = True)
Session  = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Produto(Base):
    __tablename__ = "Produto"
    id = Column(Integer, primary_key=True)
    nome_produto = Column(String(50))
    preco = Column(Float())
    nome = Column(String(50))
    quantidade = Column(Integer())
    data = Column(Date)
    entregue = Column(Boolean, default=False)
    
class CatalogoProduto(Base):
    __tablename__ = "CatalogoProduto"
    id = Column(Integer, primary_key=True)
    nome_produto = Column(String(50))
    preco = Column(Float())

class HistoricoModel(Base): # Adicionando a classe Historico
    __tablename__ = "Historico"
    id = Column(Integer, primary_key=True)
    nome_produto = Column(String(50))
    preco = Column(Float())
    nome = Column(String(50))
    quantidade = Column(Integer())
    data = Column(Date)
    
Base.metadata.create_all(engine)
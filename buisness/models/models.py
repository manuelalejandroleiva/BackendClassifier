from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker, declarative_base


Base = declarative_base()


# Licencia sanitaria
# Licencia de arrendamiento

class Licencia(Base):
    __tablename__ = "Licencia"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True) 
    




  
class Buisness(Base):
    __tablename__ = "Buisness"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True) 
    capital_money=Column(Integer,index=True)
    licencia_id = Column(Integer, ForeignKey("licencia.id"))  # clave foránea
    licencia = relationship("Licencia", back_populates="licence")  # muchos a uno
    permisos=Column(String, index=True)
    categoria=Column(Integer, index=True)
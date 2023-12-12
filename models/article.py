from sqlalchemy import Column, String, Float
from sqlalchemy.orm import Mapped
from .base import Base

class Article(Base):
    __tablename__ = 'article'

    id_ldlc: Mapped[str] = Column(String)
    name: Mapped[str] = Column(String)
    image_link: Mapped[str] = Column(String)
    link: Mapped[str] = Column(String)
    price: Mapped[float] = Column(Float)
    note: Mapped[Float] = Column(Float)

    def __init__(self, id_ldlc, name, image_link, link, price, note):
        self.id_ldlc = id_ldlc
        self.name = name
        self.image_link = image_link
        self.link = link
        self.price = price
        self.note = note

    def __repr__(self):
        return f"<Article(id={self.id}, id_ldlc='{self.id_ldlc}', name='{self.name}', link='{self.link}', price={self.price}, note='{self.note}')>"

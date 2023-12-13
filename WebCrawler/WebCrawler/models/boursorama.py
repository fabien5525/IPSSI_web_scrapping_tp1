from sqlalchemy import Column, String, Float
from sqlalchemy.orm import Mapped
from .base import Base

class Boursorama(Base):
    __tablename__ = 'boursorama'

    label: Mapped[str] = Column(String)
    last: Mapped[str] = Column(Float)
    variation: Mapped[str] = Column(String)
    opening: Mapped[str] = Column(Float)
    highest: Mapped[str] = Column(Float)
    lowest: Mapped[str] = Column(Float)
    volume: Mapped[str] = Column(Float)
    valorization: Mapped[str] = Column(Float)
    datetime: Mapped[str] = Column(String)

    def __init__(self, label, last, variation, opening, highest, lowest, volume, valorization, datetime):
        self.label = label
        self.last = last
        self.variation = variation
        self.opening = opening
        self.highest = highest
        self.lowest = lowest
        self.volume = volume
        self.valorization = valorization
        self.datetime = datetime

    def __repr__(self):
        return f"<Boursorama(id={self.id}, label='{self.label}', last='{self.last}', variation='{self.variation}', opening='{self.opening}', highest='{self.highest}', lowest='{self.lowest}', volume='{self.volume}', valorization='{self.valorization}', datetime='{self.datetime}')>"

    
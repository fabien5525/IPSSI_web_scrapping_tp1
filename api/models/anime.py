from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.orm import Mapped
from .base import Base

class Anime(Base):
    __tablename__ = 'anime'

    name: Mapped[str] = Column(String(255), nullable=False)
    image: Mapped[str] = Column(String(255), nullable=False)
    description: Mapped[str] = Column(String(255), nullable=False)
    type: Mapped[str] = Column(String(255), nullable=False)
    episodes: Mapped[str] = Column(Integer, nullable=False)
    score: Mapped[str] = Column(Float, nullable=True)
    link: Mapped[str] = Column(String(255), nullable=False)

    def __init__(self, name, image, description, type, episodes, score, link):
        self.name = name
        self.image = image
        self.description = description
        self.type = type
        self.episodes = episodes
        self.score = score
        self.link = link

    def __repr__(self):
        return f'<Anime {self.name}>'
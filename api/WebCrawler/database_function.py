from WebCrawler.items import AnimeItem
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models.anime import Anime
from models.base import Base

def save_anime_db(anime: AnimeItem, from_spider : bool = False):

    if (from_spider):
        db_path = "sqlite:///../../sqlite.db"
    else:
        db_path = "sqlite:///sqlite.db"

    engine = create_engine(db_path, echo=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(Anime(
            name=anime["name"],
            image=anime["image"],
            description=anime["description"],
            type=anime["type"],
            episodes=int(anime["episodes"]),
            score=None if anime["score"] is None else float(anime["score"]),
            link=anime["link"]
        ))
        session.commit()
        
    engine.dispose()

def get_animes_db(search : str, offset : int, limit : int) -> list:
    engine = create_engine('sqlite:///sqlite.db', echo=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        if (search == ""):
            animes = session.query(Anime).offset(offset).limit(limit).all()
            engine.dispose()
            return animes

        animes = session.query(Anime).filter(
            Anime.name.like("%{}%".format(search)) | 
            Anime.description.like("%{}%".format(search)) | 
            Anime.type.like("%{}%".format(search)) | 
            Anime.episodes.like("%{}%".format(search)) | 
            Anime.score.like("%{}%".format(search))
        ).offset(offset).limit(limit).all()
        engine.dispose()
        return animes
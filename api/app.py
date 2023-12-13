import uvicorn
from fastapi import FastAPI
from WebCrawler.database_function import get_animes_db

app = FastAPI()

@app.get("/api/anime")
def get_anime(search : str = "", offset : int = 0, limit : int  = 15):
    search = search.strip()
    animes_list = get_animes_db(search, offset, limit)

    return {
        "animes": [
            {
                "name": anime.name,
                "image": anime.image,
                "description": anime.description,
                "type": anime.type,
                "episodes": anime.episodes,
                "score": anime.score,
                "link": anime.link
            }
            for anime in animes_list
        ]
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)

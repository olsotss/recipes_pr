from fastapi import FastAPI

from routers import rating_router, collection_router, comment_router, feed_router, recipe_router

app = FastAPI()


app.include_router(recipe_router, prefix="/recipe", tags=["Recipe"])
app.include_router(feed_router, prefix="/feed", tags=["Feed"])
app.include_router(comment_router, prefix="/comments", tags=["Comments"])
app.include_router(collection_router, prefix="/collections", tags=["Collections"])
app.include_router(rating_router, prefix="/ratings", tags=["Ratings"])


from fastapi import FastAPI, HTTPException
from datetime import date
from typing import Union

from fastapi.middleware.cors import CORSMiddleware
from libs.supabase import create_supabase_client
from pydantic import BaseModel

supabase = create_supabase_client()

# data = supabase.from_("post").select("*").eq("id", 2).execute()

# print("data:", data.data)
app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],)


class User(BaseModel):
    id: str
    username: str
    name: str
    bio: str
    website: str
    email: str
    provider: str
    password: str
    badge: str
    bgImage: str
    profileImage: str
    createdAt: date
    followersCount: int
    followingCount: int
    likeCount: int


class Tweet(BaseModel):
    id: str
    userId: str
    body: str
    images:  str
    likeCount: int
    retweetCount: int
    replyCount: int
    createdAt: date


class Retweet(BaseModel):
    id: str
    tweetId: str
    userId: str
    retweetDate: date


class Like(BaseModel):
    id: str
    userId: str
    tweetId: str
    createdAt: date


class Reply:
    id: str
    userId: str
    tweetId: str
    body: str
    images: str
    createdAt: date


class Bookmark:
    id: str
    userId: str
    tweetId: str
    createdAt: str

# db_user = User(id="user.id", username="user.username")

# print(db_user)


@app.get("/user")
async def read_root():
    try:
        data = supabase.from_("User").select(
            "*,Tweet(*),Retweet(*),Like(*),Reply(*),Bookmark(*)").execute()
        return data.data
    except:
        return HTTPException(500, "Internal Server Error")


@app.get("/user/{user_id}")
async def read_item(user_id: str, q: Union[str, None] = None):
    try:
        data = supabase.from_("User").select(
            "*,Tweet(*),Retweet(*),Like(*),Reply(*),Bookmark(*)").eq("id", user_id).single().execute()
        return data.data
    except:
        return HTTPException(500, "Internal Server Error")


@app.get("/tweet/{user_id}")
async def get_tweet_of_user(user_id: str, q: Union[str, None] = None):
    try:
        data = supabase.from_("Tweet").select(
            "*,User(*)").eq("userId", user_id).execute()
        return data.data
    except:
        return HTTPException(500, "Internal Server Error")


@app.get("/tweet/")
async def get_all_tweet():
    try:
        data = supabase.from_("Tweet").select(
            "*,User(*)").execute()
        return data.data
    except:
        return HTTPException(500, "Internal Server Error")

func = supabase.functions()
@app.get("/tweet/random")
async def get_random_tweets(): 
    try:
        data = func.invoke("get_random_tweet")
        return data.data 
    except: 
        return HTTPException(500, "Internal Server Error")

@app.post('/auth', response_model=User)
async def add_user(user: User):
    try:
        db_user = User(id=user.id, username=user.username)
        supabase.from_("User").insert({"id": user.id}).execute()
    except:
        return HTTPException(500, "Internal Server Error")

from fastapi import FastAPI, HTTPException
from datetime import date
from typing import Union
from datetime import datetime
import uuid

from fastapi.middleware.cors import CORSMiddleware
from libs.supabase import create_supabase_client
from pydantic import BaseModel

supabase = create_supabase_client()

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],)

# print(uuid.uuid4())
print(datetime.now())


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
    # id: str
    userId: str
    body: str
    images:  str
    # likeCount: int
    # retweetCount: int
    # replyCount: int
    # createdAt: datetime


class Retweet(BaseModel):
    id: str
    tweetId: str
    userId: str
    retweetDate: date


class Like(BaseModel):
    id: str
    userId: str
    tweetId: str
    createdAt: datetime


class Reply(BaseModel):
    id: str
    userId: str
    tweetId: str
    body: str
    images: str
    createdAt: datetime


class Bookmark:
    id: str
    userId: str
    tweetId: str
    createdAt: datetime


class Test(BaseModel):
    body: str
# db_tweet = Tweet()

# print(db_tweet)


@app.get("/user")
async def get_all_users():
    try:
        data = supabase.from_("User").select(
            "*,Tweet(*),Retweet(*),Like(*),Reply(*),Bookmark(*)").execute()
        return data.data
    except:
        return HTTPException(500, "Internal Server Error")


@app.get("/user/{user_id}")
async def get_user_by_id(user_id: str):
    try:
        data = supabase.from_("User").select(
            "*,Tweet(*),Retweet(*),Like(*),Reply(*),Bookmark(*)").eq("id", user_id).single().execute()
        return data.data
    except:
        return HTTPException(500, "Internal Server Error")


@app.get("/tweetuser/{user_id}")
async def get_tweet_of_user(user_id: str, q: Union[str, None] = None):
    try:
        data = supabase.from_("Tweet").select(
            "*,User(*),Like(*),Reply(*),Bookmark(*)").eq("userId", user_id).execute()
        return data.data
    except:
        return HTTPException(500, "Internal Server Error")


@app.get("/tweet/{tweet_id}")
async def get_tweet_by_id(tweet_id: str):
    try:
        data = supabase.from_("Tweet").select(
            "*,User(*),Like(*),Reply(*),Bookmark(*)").eq("id", tweet_id).single().execute()
        return data.data
    except:
        return HTTPException(500, "Internal Server Error")


@app.get("/tweet/")
async def get_all_tweet():
    try:
        data = supabase.from_("Tweet").select(
            "*,User(*),Like(*),Reply(*),Bookmark(*)").execute()
        return data.data
    except:
        return HTTPException(500, "Internal Server Error")

# func = supabase.functions()
# @asyncio.coroutine


@app.get("/tweet/random/")
async def get_random_tweets():
    try:
        data = supabase.rpc("get_random_tweet")
        return data.data
    except:
        return HTTPException(500, "Internal Server Error")

# loop = asyncio.get_event_loop()
# resp = loop.run_until_complete(get_random_tweets(loop))
# loop.close()


@app.post('/tweet')
async def add_tweet(tweet: Tweet):
    # try:
    tweet = supabase.from_("Tweet").insert(
        {"body": tweet.body, "userId": tweet.userId, "images": tweet.images}).execute()
    #     if tweet:
    #         return {"message": "Tweet created successfully"}
    #     else:
    #         return {"message": "Tweet creation failed"}
    # except Exception as e:
    #     print("Error: ", e)
    #     return e


@app.delete("/tweet/{tweet_id}")
async def deleteTweet(tweet_id: str):
    supabase.from_("Tweet").delete().eq("id", tweet_id).execute()


@app.post("/auth/signout")
async def sign_out():
    res = supabase.auth.sign_out()
    return res


@app.get("/usermeta")
async def get_all_meta_users():
    try:
        data = supabase.auth.get_user()
        return data
    except:
        return HTTPException(500, "Internal Server Error")


@app.post('/test')
async def add_test(test: Test):
    try:
        test = supabase.from_("Test").insert(
            {"body": test.body}).execute()
        if test:
            return {"message": "Tweet created successfully"}
        else:
            return {"message": "Tweet creation failed"}
    except Exception as e:
        print("Error: ", e)
        return e

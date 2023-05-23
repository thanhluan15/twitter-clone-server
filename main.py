from fastapi import FastAPI, HTTPException
from typing import Union

from fastapi.middleware.cors import CORSMiddleware
from libs.supabase import create_supabase_client

supabase = create_supabase_client()

data = supabase.from_("post").select("*").eq("id", 2).execute()

print("data:", data.data)
app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],)


@app.get("/post")
async def read_root():
    try:
        data = supabase.from_("post").select("*").execute()
        return data.data
    except:
        return HTTPException(500, "Internal Server Error")


@app.get("/item/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    try:
        data = supabase.from_("post").select("*").eq("id", item_id).execute()
        return data.data
    except:
        return HTTPException(500, "Internal Server Error")

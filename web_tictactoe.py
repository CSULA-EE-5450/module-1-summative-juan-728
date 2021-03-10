import uvicorn
from typing import Optional
from fastapi import FastAPI, HTTPException, Path, status, Query, Depends
from user_db import UserDB
from fastapi.security import HTTPBasic, HTTPBasicCredentials
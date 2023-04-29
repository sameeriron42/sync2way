import pytest
from typing import Generator, Any
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.core.databases import Base
from app.init_app import create_app

@pytest.fixture(scope="function")
def app()->Generator[FastAPI,Any,None]:
    app =  create_app("test")
    yield app
    Base.metadata.drop_all(app.sql_engine)

@pytest.fixture(scope="function")
def client(app:FastAPI)->Generator[TestClient,Any,None]:
    with TestClient(app) as client:
        yield client
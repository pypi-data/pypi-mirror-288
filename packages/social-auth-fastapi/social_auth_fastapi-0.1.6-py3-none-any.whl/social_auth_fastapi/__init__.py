#!/usr/bin/env python3
from typing import Optional

from fastapi import FastAPI
from loguru import logger

from .base.database import create_engine_and_session
from .conf import settings, SettingsSocial
from .models import SocialAccount
from .models.base import create_table
from .routers import router
from .social.sso.base import OpenID


async def register_auth_social_init(
    app: FastAPI,
    user_model,
    sqlalchemy_database_uri: str,
    token_secret_key: Optional[str] = None,
    token_algorithm: Optional[str] = None,
    token_expire_seconds: Optional[int] = None,
    token_refresh_expire_seconds: Optional[int] = None,
    google_client_id: Optional[str] = None,
    google_client_secret: Optional[str] = None,
    github_client_secret: Optional[str] = None,
    facebook_client_id: Optional[str] = None,
    facebook_client_secret: Optional[str] = None,
    fibit_client_id: Optional[str] = None,
    fibit_client_secret: Optional[str] = None,
    gitlab_client_id: Optional[str] = None,
    gitlab_client_secret: Optional[str] = None,
    gitlab_base_endpoint_url: Optional[str] = None,
    line_client_id: Optional[str] = None,
    line_client_secret: Optional[str] = None,
    linkedin_client_id: Optional[str] = None,
    linkedin_client_secret: Optional[str] = None,
    notion_client_id: Optional[str] = None,
    notion_client_secret: Optional[str] = None,
    twitter_client_id: Optional[str] = None,
    twitter_client_secret: Optional[str] = None,
):
    """
    Start initialization

    :return:
    """
    settings.USER_MODEL = user_model
    engine, db_session = create_engine_and_session(sqlalchemy_database_uri)
    settings.ENGINE = engine
    settings.DB_SESSION = db_session
    if token_secret_key:
        settings.TOKEN_SECRET_KEY = token_secret_key

    if token_algorithm:
        settings.TOKEN_ALGORITHM = token_algorithm

    if token_expire_seconds:
        settings.TOKEN_EXPIRE_SECONDS = token_expire_seconds

    if token_refresh_expire_seconds:
        settings.TOKEN_REFRESH_EXPIRE_SECONDS = token_refresh_expire_seconds

    settings.GOOGLE_CLIENT_ID = google_client_id
    settings.GOOGLE_CLIENT_SECRET = google_client_secret

    settings.GITHUB_CLIENT_ID = github_client_secret
    settings.GITHUB_CLIENT_SECRET = github_client_secret

    settings.FACEBOOK_CLIENT_ID = facebook_client_id
    settings.FACEBOOK_CLIENT_SECRET = facebook_client_secret

    settings.FIBIT_CLIENT_ID = fibit_client_id
    settings.FIBIT_CLIENT_SECRET = fibit_client_secret

    settings.GITLAB_CLIENT_ID = gitlab_client_id
    settings.GITLAB_CLIENT_SECRET = gitlab_client_secret
    settings.GITLAB_BASE_ENDPOINT_URL = gitlab_base_endpoint_url

    settings.LINE_CLIENT_ID = line_client_id
    settings.LINE_CLIENT_SECRET = line_client_secret

    settings.LINKEDIN_CLIENT_ID = linkedin_client_id
    settings.LINKEDIN_CLIENT_SECRET = linkedin_client_secret

    settings.NOTION_CLIENT_ID = notion_client_id
    settings.NOTION_CLIENT_SECRET = notion_client_secret

    settings.TWITTER_CLIENT_ID = twitter_client_id
    settings.TWITTER_CLIENT_SECRET = twitter_client_secret

    # Create database table
    logger.warning('Creating table first...')
    await create_table()
    logger.success('Create table successful')
    app.include_router(router)

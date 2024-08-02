import inspect
from typing import Optional

from fastapi import Request
from loguru import logger
from sqlalchemy import Integer, String, TIMESTAMP
from sqlalchemy.ext.asyncio import AsyncSession

from .. import settings
from ..cruds.crud_model_base import BaseDao
from ..oauth import jwt
from ..oauth.timezone import timezone
from ..social.services import *
from ..social.sso.base import OpenID
from ..social.sso.errors import SSOExceptionError
from ..cruds.crud_social_account import SocialAccountDao
from ..schemas.social_account import RegisterSocialAccountParam

from ..social.sso.constant import ProviderEnum


class SocialService:
    def __init__(self, provider):
        self.provider = provider
        self.sso_service = self.__init_sso__by_provider()

    def __init_sso__by_provider(self):
        match self.provider:
            case ProviderEnum.GOOGLE:
                return GoogleService()
            case ProviderEnum.GITHUB:
                return GithubService()
            case ProviderEnum.GITLAB:
                return GitlabService()
            case ProviderEnum.FACEBOOK:
                return FacebookService()
            case ProviderEnum.FITBIT:
                return FitbitService()
            case ProviderEnum.LINE:
                return LineService()
            case ProviderEnum.LINKEDIN:
                return LinkedInService()
            case ProviderEnum.NOTION:
                return NotionService()
            case ProviderEnum.TWITTER:
                return TwitterService()
            case _:
                raise SSOExceptionError(msg='Provider invalid')

    async def build_auth_url(self, redirect_uri: str):
        return await self.sso_service.build_auth_url(redirect_uri)

    async def verify_login(self, request: Request, redirect_uri: Optional[str] = None):
        try:
            # user_profile = await self.sso_service.sso.verify_and_process(request, redirect_uri=redirect_uri)
            usr_dict = {'id': '103127236837536345788', 'email': 'training.team113@gmail.com', 'first_name': 'training',
                        'last_name': 'team', 'display_name': 'training team',
                        'picture': 'https://lh3.googleusercontent.com/a/ACg8ocJ0wepnpXclYYMWK4kGDysMquVC4-FS3th5YRvK4qhEeC9hgQ=s96-c',
                        'provider': 'google'}
            user_profile = OpenID(**usr_dict)
            async with settings.DB_SESSION() as db:
                account = await SocialAccountDao.get_by_login_id_and_provider(
                    db=db, login_id=user_profile.id, provider=user_profile.provider
                )

                if account is None:
                    user, primary_key = await self.build_user_model_inst_from_open_id(user_profile)
                    user_model = await BaseDao.create_(db, create_data=user)
                    account = await self.create_new_account(
                        db, user_profile.id, str(user_model.__dict__.get(primary_key)), user_profile.provider
                    )

                access_token, access_token_expire_time = await jwt.create_access_token(
                    str(account.login_id), provider=user_profile.provider
                )
                refresh_token, refresh_token_expire_time = await jwt.create_refresh_token(
                    str(account.login_id), access_token_expire_time, provider=user_profile.provider
                )
                await db.commit()
                return (access_token, refresh_token, access_token_expire_time, refresh_token_expire_time)
        except Exception as e:
            logger.error(e)
            raise e

    async def create_new_account(self, db: AsyncSession, login_id, user_id, provider):
        register_account = RegisterSocialAccountParam(login_id=login_id, provider=provider, user_id=user_id)
        account = await SocialAccountDao.create(db, register_account)
        return account

    async def build_user_model_inst_from_open_id(self, user_profile: OpenID) -> settings.USER_MODEL:
        if settings.USER_MODEL is None:
            return None
        user_req = dict()
        columns = settings.USER_MODEL.__table__.columns
        constructor_params = [
            param for param in inspect.signature(settings.USER_MODEL.__init__).parameters.keys() if param != 'self'
        ]
        primary_key = None
        for column in columns:
            if column.primary_key:
                primary_key = column.name

            if column.name not in constructor_params:
                continue

            if column.default or (column.autoincrement and column.autoincrement not in ['auto', 'ignore_fk']):
                user_req.update({column.name: None})
                continue

            if not column.primary_key and column.nullable and not isinstance(column.type, String):
                user_req.update({column.name: None})
                continue

            if isinstance(column.type, Integer):
                user_req.update({column.name: 0})
            elif isinstance(column.type, TIMESTAMP):
                user_req.update({column.name: timezone.now})
            elif isinstance(column.type, String):
                if 'first_name' in column.name:
                    user_req.update({column.name: user_profile.first_name})
                elif 'last_name' in column.name:
                    user_req.update({column.name: user_profile.last_name})
                elif 'name' in column.name:
                    if user_profile.display_name:
                        user_req.update({column.name: user_profile.display_name})
                    else:
                        name = (
                            user_profile.first_name
                            if user_profile.first_name
                            else '' + user_profile.last_name
                            if user_profile.last_name
                            else ''
                        )
                        user_req.update({column.name: name})
                elif 'email' in column.name:
                    user_req.update({column.name: user_profile.email})

        return settings.USER_MODEL(**user_req), primary_key

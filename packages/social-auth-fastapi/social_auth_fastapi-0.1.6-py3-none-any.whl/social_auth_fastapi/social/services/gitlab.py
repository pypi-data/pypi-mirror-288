from ... import settings
from ..sso.gitlab import GitlabSSO


class GitlabService:
    def __init__(self):
        self.sso = GitlabSSO(
            client_id=settings.GITLAB_CLIENT_ID,
            client_secret=settings.GITLAB_CLIENT_SECRET,
            base_endpoint_url=settings.GITLAB_BASE_ENDPOINT_URL,
            use_state=True,
            allow_insecure_http=True,
        )

    async def build_auth_url(self, redirect_uri: str):
        with self.sso:
            self.sso.redirect_uri = redirect_uri
            url = await self.sso.get_login_redirect()

        return url

    async def get_profile(self, request, redirect_uri: str):
        with self.sso:
            user = await self.sso.verify_and_process(request, redirect_uri=redirect_uri)

        return user

from dishka import Provider, Scope, provide

from commons.http_api.auth import JwtManager
from mini_crm.infrastructure.http_api import ApiSecuritySettings


class AuthProvider(Provider):
    scope = Scope.APP

    @provide
    def create_jwt_manager(
        self,
        api_security_settings: ApiSecuritySettings,
    ) -> JwtManager:
        return JwtManager(
            secret_key=api_security_settings.SECRET_KEY,
            jwt_algorithm=api_security_settings.JWT_ALGORITHM,
            jwt_access_token_expire_minutes=api_security_settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
            jwt_refresh_token_expire_minutes=api_security_settings.JWT_REFRESH_TOKEN_EXPIRE_MINUTES,
        )

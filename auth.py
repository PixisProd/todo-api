from datetime import timedelta
from authx import AuthX, AuthXConfig
from config import jwt_secret_key

config = AuthXConfig()
config.JWT_SECRET_KEY = jwt_secret_key
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ['cookies']
config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
config.JWT_COOKIE_CSRF_PROTECT = False

security = AuthX(config=config)

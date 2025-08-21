from pydantic import BaseModel


class FeatureFlags(BaseModel):
    enable_api: bool = False

class Config(BaseModel):
    env: str = "dev"
    users_url: str = "http://users:5000"
    orders_url: str = "http://orders:5001"
    logging_level: str = "INFO"
    feature_flags: FeatureFlags = FeatureFlags()
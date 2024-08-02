from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    aws_key: str
    aws_secret: str

    db_rov_proxy_host: str
    db_rov_proxy_port: str
    db_rov_proxy_user: str
    db_rov_proxy_password: str

    db_rov_geodata_database: str
    db_rov_gis_database: str
    db_rov_landing_database: str
    db_rov_sentinel_database: str
    db_rov_ine_database: str

    geoserver_api_url: str
    geoserver_api_user: str
    geoserver_api_password: str

    gis_inference_bucket: str
    gis_inference_region: str

    run_results_bucket: str

    s3_region: str

    sentinel_user: str
    sentinel_password: str
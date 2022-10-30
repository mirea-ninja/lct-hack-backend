from contextlib import asynccontextmanager

from aiobotocore.session import ClientCreatorContext, get_session

from app.config import config

s3_session = get_session()


@asynccontextmanager
async def get_s3_client() -> ClientCreatorContext:
    async with s3_session.create_client(
        service_name="s3",
        region_name=config.STORAGE_REGION,
        endpoint_url=config.STORAGE_ENDPOINT,
        aws_secret_access_key=config.STORAGE_ACCESS_KEY,
        aws_access_key_id=config.STORAGE_ACCESS_KEY_ID,
    ) as client:
        try:
            yield client
        finally:
            await client.close()

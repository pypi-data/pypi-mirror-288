from fastapi import FastAPI
import os
from dotenv import load_dotenv
load_dotenv()
from gai.lib.common.logging import getLogger
logger = getLogger(__name__)
import asyncio
from gai.lib.common.utils import this_dir
import httpx
import sys

def app_version():
    ver_file=os.path.join(this_dir(__file__),"VERSION")
    if os.path.exists(ver_file):
        with open(ver_file) as f:
            return f.read()
    return "Not found."
APP_VERSION=app_version()

def lib_version():
    import subprocess
    import re
    try:
        command_output = subprocess.check_output("pip list | grep gai-sdk", shell=True).decode()
    except subprocess.CalledProcessError:
        raise Exception("gai-sdk is not installed.")
    version = re.search(r'(\d+\.\d+)', command_output)
    if version:
        return version.group()
    else:
        return "Not installed."
LIB_VERSION=lib_version()

# This tells fastapi which path to host the swagger ui page.
def get_swagger_url():
    swagger_url=None
    if "SWAGGER_URL" in os.environ and os.environ["SWAGGER_URL"]:
        swagger_url=os.environ["SWAGGER_URL"]
        logger.info(f"swagger={swagger_url}")
    else:
        logger.info("swagger_url=disabled.")
    return swagger_url

def configure_cors(app: FastAPI):
    from fastapi.middleware.cors import CORSMiddleware
    allowed_origins_str = "*"
    if "CORS_ALLOWED" in os.environ:
        allowed_origins_str = os.environ["CORS_ALLOWED"]    # from .env
    allowed_origins = allowed_origins_str.split(",")  # split the string into a list
    logger.info(f"allow_origins={allowed_origins}")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def configure_semaphore():
    use_semaphore = os.getenv("USE_SEMAPHORE", "False").lower() == "true"
    semaphore = None
    if use_semaphore:
        logger.info("Using semaphore")
        import asyncio
        semaphore = asyncio.Semaphore(2)
    return semaphore

async def acquire_semaphore(semaphore):
    while semaphore:
        try:
            await asyncio.wait_for(semaphore.acquire(), timeout=0.1)
            break
        except asyncio.TimeoutError:
            logger.warn("_streaming: Server is busy")
            await asyncio.sleep(1)

def release_semaphore(semaphore):
    if semaphore:
        semaphore.release()
        logger.debug("_streaming: Server is available")

def self_test():
    # Check if the necessary packages are installed
    import site
    sites = site.getsitepackages()
    if not sites:
        raise Exception("site.getsitepackages() returned empty list.")
    if not os.path.exists(sites[0]):
        raise Exception(f"site-packages directory {sites[0]} does not exist.")
    if sites[0] not in sys.path:
        raise Exception(f"site-packages directory {sites[0]} not in sys.path.")
    
    site_package_gai_dir = os.path.join(sites[0], "gai")
    if not os.path.exists(site_package_gai_dir):
        raise Exception(f"site-packages directory {site_package_gai_dir} does not exist.")
    
    site_package_gai_lib_dir = os.path.join(site_package_gai_dir, "lib")
    if not os.path.exists(site_package_gai_lib_dir):
        raise Exception(f"site-packages directory {site_package_gai_lib_dir} does not exist.")
    
    site_package_gai_ttt_dir = os.path.join(site_package_gai_dir, "ttt")
    if not os.path.exists(site_package_gai_ttt_dir):
        raise Exception(f"site-packages directory {site_package_gai_ttt_dir} does not exist.")
    
    logger.info("self_test: OK")
    
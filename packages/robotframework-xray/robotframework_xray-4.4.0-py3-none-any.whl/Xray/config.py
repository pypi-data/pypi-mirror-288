import os
from os.path import join
from dotenv import load_dotenv

class Config:
    def get(value: str):
        load_dotenv(join(os.path.abspath(os.curdir), '.env'))
        return os.getenv(value)
    
    def debug() -> bool:
        try:
            return os.getenv('XRAY_DEBUG', Config.get('XRAY_DEBUG')).lower().capitalize() == "True"
        except:
            return False
    
    def project_key():
        return os.getenv('PROJECT_KEY', Config.get('PROJECT_KEY'))
    
    def xray_api():
        return os.getenv('XRAY_API', Config.get('XRAY_API'))
    
    def xray_client_id():
        return os.getenv('XRAY_CLIENT_ID', Config.get('XRAY_CLIENT_ID'))
    
    def xray_client_secret():
        return os.getenv('XRAY_CLIENT_SECRET', Config.get('XRAY_CLIENT_SECRET'))
    
    def cucumber_path():
        return os.getenv('CUCUMBER_PATH', Config.get('CUCUMBER_PATH'))
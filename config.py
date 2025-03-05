
import os
from dotenv import load_dotenv
load_dotenv()
def config():
    # Now you can access your variables
    image_path = os.getenv("image_path")
    save_path = os.getenv("save_path")
    
    # os.makedirs(image_path, exist_ok= True)
    # os.makedirs(save_path, exist_ok=True)
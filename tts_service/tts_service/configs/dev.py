import os
import dotenv

dotenv_file = ".env_dev"
if os.path.exists(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

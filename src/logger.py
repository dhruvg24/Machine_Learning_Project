# for any kind of execution logger will be the file which will keep a information store of it (has errors as well)

import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

logs_path = os.path.join(os.getcwd(),"logs",LOG_FILE)
# current working directory

os.makedirs(logs_path,exist_ok=True)
# exist_ok ensures appending even if file with same name exists.

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)


logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO

)


# if __name__ == "__main__":
#     logging.info("Logging has started")

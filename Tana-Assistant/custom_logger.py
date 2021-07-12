import logging
import os
dir_path = f"{os.path.dirname(os.path.realpath(__file__))}"
logging.basicConfig(filename=f"{dir_path}/log_files/tana.log", format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.INFO)

log = logging.getLogger(__name__)
# logging.disable(logging.CRITICAL) # disable logging

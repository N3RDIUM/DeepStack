import os
import time
import importlib

from logger import logger

logger.debug(f"[{__name__}] Loading utils...")
utils = {}
files_to_load = [f for f in os.listdir("utils") if f.endswith(".py") and not f.startswith("__") and not f.startswith("base_util")]
tic = time.time()
for file in files_to_load:
    module_name = file.replace(".py", "")
    module = importlib.import_module(f"utils.{module_name}")
    util= module.EXPORT_UTIL()
    utils[util.__class__.__name__] = util
    logger.debug(f"[{__name__}] Loaded {module_name} from {file}")
toc = time.time()
logger.debug(f"[{__name__}] Loaded {len(utils)} utils in {toc-tic} seconds.")
logger.debug(f"\n[{__name__}] Available utils:\n================")
for util in utils:
    logger.debug(f"[{__name__}] {utils[util].__class__.__name__}: {utils[util].whatsthis()}")
logger.debug("================\n")
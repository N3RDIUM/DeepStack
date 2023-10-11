from logger import logger
import uuid

class BaseUtil:
    hint = "This is a base utility."
    def __init__(self):
        """
        BaseUtil
        
        A base class for all the extensible utils out there!
        This class can be inherited from to create new utils.
        """
        self.id = uuid.uuid4()
        logger.debug(f"[{__name__}] Registered new utility with ID {self.id}")
        self.funcs = {}
        
    def whatsthis(self):
        """
        whatsthis
        
        Returns a string describing the utility
        """
        return self.hint
        
EXPORT_UTIL = BaseUtil
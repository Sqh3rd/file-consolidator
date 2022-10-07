from Import_Object import Import_Object
from Logger import Logger

class Import_Object_Factory:
    def create_import_object(self, logger: Logger, file_name: str) -> Import_Object:
        return Import_Object(logger, file_name)
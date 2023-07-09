import logging
from datetime import datetime
from os.path import join, isdir
from os import getcwd, makedirs

log_location_format = {
    "date_dir": datetime.now().date().isoformat(),
    "time_dir": ''.join(datetime.now().time().isoformat().split('.')[0].split(":")[:-1])
}
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


class AndrewsLogger:
    def __init__(self, log_location: str = None, chosen_format: str = None,
                 project_name: str = None, logger_levels: list = None):

        self.default_log_location_format = {
            "date_dir": datetime.now().date().isoformat(),
            "time_dir": ''.join(datetime.now().time().isoformat().split('.')[0].split(":")[:-1])
        }
        self.timestamp = datetime.now().isoformat(timespec='minutes').replace(':', '')

        if not logger_levels:
            self.logger_levels = ["DEBUG", "INFO", "ERROR"]
        elif logger_levels:
            self.logger_levels = logger_levels

        if not log_location:
            self.log_location = (f"../logs/{self.default_log_location_format['date_dir']}/"
                                 f"{self.default_log_location_format['time_dir']}")
            self._CheckMakeLogLocation()
        elif log_location:
            self.log_location = self._CheckMakeLogLocation()

        if not chosen_format:
            self.chosen_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        elif chosen_format:
            self.chosen_format = chosen_format

        if not project_name:
            self.project_name = self._GetProjectName()
        elif project_name:
            self.project_name = project_name

        self.logger = logging.getLogger('new_logger')
        self.formatter = logging.Formatter(chosen_format)

        self.is_initialized = False

    def FinalInit(self):
        # info log the handlers that have been assigned
        self.logger.propagate = True
        self._MakeFileHandlers()

        self.logger.setLevel(10)
        print("logger initialized")
        self.logger.info(f"Starting {self.project_name} with the following FileHandlers:\n"
                         f"{[x for x in self.logger.handlers]}")
        self.is_initialized = True

    def _CheckMakeLogLocation(self):
        if isdir(self.log_location):
            return self.log_location
        else:
            makedirs(self.log_location)
            return self.log_location

    @staticmethod
    def _GetProjectName():
        pname = getcwd().split("\\")[-2]
        return pname

    def _MakeFileHandlers(self):
        """ Add three filehandlers to the logger then set the log level to debug.
        This way all messages will be sorted into their appropriate spots"""
        for lvl in self.logger_levels:
            self.logger.setLevel(lvl)
            if self.logger.level == 10:
                level_string = "DEBUG"
            elif self.logger.level == 20:
                level_string = "INFO"
            elif self.logger.level == 40:
                level_string = "ERROR"
            else:
                print("other logger level detected, defaulting to DEBUG")
                level_string = "DEBUG"
            log_path = join(self.log_location, '{}-{}-{}.log'.format(level_string,
                                                                     self.project_name,
                                                                     self.timestamp))

            # Create a file handler for the new_logger, and specify the log file location
            file_handler = logging.FileHandler(log_path)
            # Set the logging format for the file handler
            file_handler.setFormatter(self.formatter)
            file_handler.setLevel(self.logger.level)
            # Add the file handlers to the loggers
            self.logger.addHandler(file_handler)


"""def create_logger(log_location: str = (f"../logs/{log_location_format['date_dir']}/"
                                       f"{log_location_format['time_dir']}"),
                  chosen_format: str = log_format,
                  project_name=None) -> logging.Logger:
    def _GetProjectName():
        pname = getcwd().split("\\")[-2]
        return pname

    def _CheckMakeLogLocation():
        if isdir(log_location):
            pass
        else:
            makedirs(log_location)

    def _MakeFileHandlers(log_lvls):
        Add three filehandlers to the logger then set the log level to debug.
        This way all messages will be sorted into their appropriate spots
        for lvl in log_lvls:
            new_logger.setLevel(lvl)
            if new_logger.level == 10:
                level_string = "DEBUG"
            elif new_logger.level == 20:
                level_string = "INFO"
            elif new_logger.level == 40:
                level_string = "ERROR"
            else:
                print("other logger level detected, defaulting to DEBUG")
                level_string = "DEBUG"
            # TODO: add in filename to log filename
            log_path = join(log_location, '{}-{}-{}.log'.format(level_string, project_name, timestamp))

            # Create a file handler for the new_logger, and specify the log file location
            file_handler = logging.FileHandler(log_path)
            # Set the logging format for the file handler
            file_handler.setFormatter(formatter)
            file_handler.setLevel(new_logger.level)
            # Add the file handlers to the loggers
            new_logger.addHandler(file_handler)

    if not project_name:
        project_name = _GetProjectName()

    _CheckMakeLogLocation()
    # timestamp now includes HHMM time, the : seems to cause filename issues, so it is omitted
    # for just the date use datetime.now().date().isoformat()
    timestamp = datetime.now().isoformat(timespec='minutes').replace(':', '')
    formatter = logging.Formatter(chosen_format)
    logger_levels = ["DEBUG", "INFO", "ERROR"]

    # Create a new_logger with a specified name and make sure propagate is True
    new_logger = logging.getLogger('new_logger')
    new_logger.propagate = True

    # create and assign a filehandler for each of the logger levels
    _MakeFileHandlers(logger_levels)

    # set the new_logger level back to DEBUG, so it handles all messages
    new_logger.setLevel(10)

    # info log the handlers that have been assigned
    new_logger.info(f"Starting {project_name} with the following FileHandlers:\n"
                    f"{[x for x in new_logger.handlers]}")

    print("logger initialized")
    return new_logger"""


if __name__ == "__main__":
    # logger = create_logger()
    main_logger = AndrewsLogger()
    main_logger.FinalInit()
    # TODO: figure out a way to not let any logger calls be made unless FinalInit() has be called.
    main_logger.logger.error("error test")


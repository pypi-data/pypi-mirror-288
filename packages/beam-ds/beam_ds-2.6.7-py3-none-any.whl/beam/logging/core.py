import sys
from contextlib import contextmanager

import loguru
from ..utils import running_platform
from ..path import beam_path
import atexit


class BeamLogger:

    def __init__(self, path=None, print=True):
        self.logger = loguru.logger.opt(depth=1)
        self._level = None
        self.logger.remove()
        self.handlers_queue = []
        self.running_platform = running_platform()

        self.handlers = {}
        self.tags = {}
        if print:
            self.print()

        self.file_objects = {}
        self.path = None
        if path is not None:
            self.add_file_handlers(path)

        self.set_verbosity('INFO')

        atexit.register(self.cleanup)

    def dont_print(self):
        self.logger.remove(self.handlers['stdout'])

    def print(self):
        self.handlers['stdout'] = self.stdout_handler()

    def cleanup(self, print=True):
        for k, handler in self.handlers.items():
            if k == 'stdout' and print:
                continue
            try:
                self.logger.remove(handler)
            except ValueError:
                pass

        if print:
            self.handlers = {k: v for k, v in self.handlers.items() if k == 'stdout'}
        else:
            self.handlers = {}

        for k, file_object in self.file_objects.items():
            file_object.close()
        self.file_objects = {}

    def add_file_handlers(self, path, tag=None):

        path = beam_path(path)

        debug_path = path.joinpath('debug.log')
        file_object = debug_path.open('w')
        self.file_objects[str(debug_path)] = file_object

        if self.running_platform == 'script':
            format = '{time:YYYY-MM-DD HH:mm:ss} ({elapsed}) | BeamLog | {level} | {file} | {function} | {line} | {message}'
        else:
            format = '{time:YYYY-MM-DD HH:mm:ss} ({elapsed}) | BeamLog | {level} | %s | {function} | {line} | {message}' \
                     % self.running_platform

        handler = self.logger.add(file_object, level='DEBUG', format=format)

        self.handlers[str(debug_path)] = handler

        json_path = path.joinpath('json.log')
        file_object = json_path.open('w')
        self.file_objects[str(json_path)] = file_object

        format = 'JSON LOGGER'
        handler = self.logger.add(file_object, level='DEBUG', format=format, serialize=True)

        self.handlers[str(json_path)] = handler
        if tag is not None:
            self.tags[tag] = path

    def remove_tag(self, tag):
        path = self.tags[tag]
        self.remove_file_handler(path)

    def remove_default_handlers(self):
        self.remove_tag('default')

    def open(self, path):
        path = beam_path(path)
        self.handlers_queue.append(path)
        return self

    def __enter__(self):
        self.add_file_handlers(self.handlers_queue[-1])
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        path = self.handlers_queue.pop()
        self.remove_file_handler(path)

    def remove_file_handler(self, name):
        for suffix in ['debug.log', 'json.log']:
            fullname = str(name.joinpath(suffix))
            self.logger.remove(self.handlers[fullname])
            self.handlers.pop(fullname)

    def debug(self, message, **extra):
        self.logger.debug(message, **extra)

    def info(self, message, **extra):
        self.logger.info(message, **extra)

    def warning(self, message, **extra):
        self.logger.warning(message, **extra)

    def error(self, message, **extra):
        self.logger.error(message, **extra)

    def critical(self, message, **extra):
        self.logger.critical(message, **extra)

    def exception(self, message, **extra):
        self.logger.exception(message, **extra)

    def __getstate__(self):

        if self.path is None:
            path = None
        elif isinstance(self.path, str):
            path = self.path
        else:
            path = self.path.as_uri()
        state = {'path': path}
        return state

    def __setstate__(self, state):
        self.__init__(state['path'])

    def stdout_handler(self, level='INFO'):
        return self.logger.add(sys.stdout, level=level, colorize=True,
                               format=f'🔥 | <green>{{time:HH:mm:ss}} ({{elapsed}})</green> | '
                                      f'<level>{{level:<8}}</level> 🗎 <level>{{message}}</level> '
                                      f'<cyan>(∫{{file}}:{{function}}-#{{line}})</cyan>')

    @property
    def level(self):
        return self._level

    def set_verbosity(self, level):
        """
        Sets the log level for all handlers to the specified level.
        """
        # Convert the level string to uppercase to match Loguru's expected levels
        level = level.upper()
        self._level = level

        if 'stdout' in self.handlers:
            self.logger.remove(self.handlers['stdout'])

        self.handlers['stdout'] = self.stdout_handler(level=level)

    def debug_mode(self):
        self.set_verbosity('DEBUG')
        self.debug('Debug mode activated')

    def info_mode(self):
        self.set_verbosity('INFO')
        self.info('Info mode activated')

    def warning_mode(self):
        self.set_verbosity('WARNING')
        self.warning('Warning mode activated (only warnings and errors will be logged)')

    def error_mode(self):
        self.set_verbosity('ERROR')
        self.error('Error mode activated (only errors will be logged)')

    def critical_mode(self):
        self.set_verbosity('CRITICAL')
        self.critical('Critical mode activated (only critical errors will be logged)')

    @contextmanager
    def as_debug_mode(self):
        mode = self.logger.level
        self.debug_mode()
        yield
        self.set_verbosity(mode)

    @contextmanager
    def as_info_mode(self):
        mode = self.logger.level
        self.info_mode()
        yield
        self.set_verbosity(mode)

    @contextmanager
    def as_warning_mode(self):
        mode = self.logger.level
        self.warning_mode()
        yield
        self.set_verbosity(mode)

    @contextmanager
    def as_error_mode(self):
        mode = self.logger.level
        self.error_mode()
        yield
        self.set_verbosity(mode)

    @contextmanager
    def as_critical_mode(self):
        mode = self.logger.level
        self.critical_mode()
        yield
        self.set_verbosity(mode)


beam_logger = BeamLogger()

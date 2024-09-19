#
# Copyright (C) 2007 Andrew Resch <andrewresch@gmail.com>
#
# This file is part of Deluge and is licensed under GNU General Public License 3.0, or later, with
# the additional special exception to link portions of this program with the OpenSSL library.
# See LICENSE for more details.
#

import inspect
import logging
import sys

import deluge.common
import deluge.configmanager
import deluge.log
from deluge.argparserbase import ArgParserBase
from deluge.i18n import setup_translation

log = logging.getLogger(__name__)


# try:
#     from setproctitle import setproctitle
#     logging.getLogger('kcxxx').info('%s: imported setproctitle', __file__)
# except ImportError:
#     logging.getLogger('kcxxx').info('%s: failed to import setproctitle, stubbing', __file__)
#     def setproctitle(title):
#         return
def setproctitle(title):
    logging.getLogger('kcxxx').info('%s: setproctitle(%s)', __file__, title)
    return


class UI:
    """
    Base class for UI implementations.

    """

    cmd_description = """Override with command description"""

    def __init__(self, name, **kwargs):
        self.__name = name
        self.ui_args = kwargs.pop('ui_args', None)
        setup_translation()
        self.__parser = ArgParserBase(**kwargs)

    def parse_args(self, parser, args=None):
        logging.getLogger('kcxxx').info('%s: parse_args, parser=%s', __name__, parser)
        options = parser.parse_args(args)
        logging.getLogger('kcxxx').info('%s: parse_args2', __name__)
        if not hasattr(options, 'remaining'):
            options.remaining = []
        logging.getLogger('kcxxx').info('%s: returning', __name__)
        return options

    @property
    def name(self):
        return self.__name

    @property
    def parser(self):
        return self.__parser

    @property
    def options(self):
        return self.__options

    def start(self, parser=None):
        logging.getLogger('kcxxx').info('UI::start: here')
        args = sys.argv[1:]
        frame = inspect.currentframe()
        logging.getLogger('kcxxx').info(
            '%s:%d: setting parser', frame.f_code.co_filename, frame.f_lineno
        )
        if parser is None:
            parser = self.parser
        logging.getLogger('kcxxx').info('%s: UI::start: here3', __name__)
        self.__options = self.parse_args(parser, args)

        logging.getLogger('kcxxx').info('UI::start: about to setproctitle')
        setproctitle('deluge-%s' % self.__name)

        logging.getLogger('kcxxx').info('%s: here4', __file__)
        log.info('Deluge ui %s', deluge.common.get_version())
        logging.getLogger('kcxxx').info('%s: here5', __name__)
        log.debug('options: %s', self.__options)
        logging.getLogger('kcxxx').info('%s: here6', __name__)
        log.info('Starting %s ui..', self.__name)
        logging.getLogger('kcxxx').info('UI::start: done')

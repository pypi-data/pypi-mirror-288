#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: nu:ai:ts=4:sw=4

#
#  Copyright (C) 2024 Joseph Areeda <joseph.areeda@ligo.org>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
""""""

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'

import configparser
import logging
import os
from pathlib import Path


class OmicronConfig:
    """
    Representing the configuration of all LSC Omicron programs in one place.
    The hierarchy of where to get the information. First one of ther list found.
    1. File path passed in creation or in set_file method
    2. Environment variable OMICRON_CONFIG
    3. ${HOME}/.ligoomicron.ini
    4. Internal defaults. See ligoomicron.ini in this project.

    Our philosophy is to put as many options as we can into the configuration.
    """

    def __init__(self, path=None, logger=None):
        """

        :param Path|str path: path to configuration file
        :param logging.Logger logger: program logger
        """
        self.config = None
        if logger is None:
            # global logger
            log_file_format = "%(asctime)s - %(levelname)s - %(funcName)s %(lineno)d: %(message)s"
            log_file_date_format = '%m-%d %H:%M:%S'
            logging.basicConfig(format=log_file_format, datefmt=log_file_date_format)
            self.logger = logging.getLogger('OmicronConfig')
            self.logger.setLevel(logging.INFO)
        else:
            self.logger = logger
        self.path = path if path is None else self.set_file(path)

    def set_file(self, path):
        """
        Read the configuration file replacing any existing values
        :param Path|str path: path to configuration file
        :return configparser.ConfigParser: copy of the config
        """
        if path is None or not Path(path).exists():
            raise FileNotFoundError(f'{path} does not exist')
        self.path = Path(path)
        self.config = configparser.ConfigParser()
        self.config.read(self.path)
        self.logger.debug(f'Configuration read from {self.path.absolute()}')
        return self.config

    def get_config(self):
        """
        The preferred way to get current configuratio. This does the loo through list of places to look for the
        configuration file
        :return configparser.ConfigParser:

        """
        if self.config is None:
            path = os.getenv('OMICRON_CONFIG', None)
            if path is None:
                path = Path.home() / '.ligoomicron.ini'
            if path is None or not path.exists():
                me = Path(__file__)
                mydir = me.parent
                path = mydir / 'ligoomicron.ini'
            self.logger.debug(f'Read config file {path.absolute()}')

            if path.exists():
                config = configparser.ConfigParser()
                config.read(path)
                self.config = config
            else:
                raise FileNotFoundError('No configuration file found')
        return self.config

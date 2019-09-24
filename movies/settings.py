# -*- coding: utf-8 -*-
import os


class BaseConfig(object):
    """Base configuration."""
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(BASEDIR, os.pardir))
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BaseConfig.BASEDIR, "movies.sqlite")}'


class ProductionConfig(BaseConfig):
    pass


if os.environ.get('ENV') == 'prod':
    Config = ProductionConfig
else:
    Config = DevelopmentConfig

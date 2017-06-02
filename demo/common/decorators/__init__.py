#!/usr/bin/env python
# coding: utf-8

from common.decorators.cache import page_cache
from common.decorators.url import short_url_parse_wrap
from common.decorators.celery import task_exception_handler
# from common.decorators.auth import user_decrypto, user_encrypto
from common.decorators.mobile import mobile_detection
# from common.decorators.server import require_fuwo_server
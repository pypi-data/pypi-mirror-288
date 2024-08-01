# -*- coding: UTF-8 -*-

class BizException(Exception):

    def __init__(self, http_status: int, code: int, message: str,
                 alert_sentry: bool = False):
        self.http_status = http_status
        self.code = code
        self.message = message
        self.alert_sentry = alert_sentry

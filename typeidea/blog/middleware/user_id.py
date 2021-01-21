import uuid
import logging


logger = logging.getLogger(__name__)

USER_KEY = 'uid'
TEN_YEARS = 60 * 60 * 24 * 365 * 10

class UserIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        logger.info('Uid Function Call Start')
        uid = self.generate_uid(request)
        request.uid = uid
        response = self.get_response(request)
        response.set_cookie(USER_KEY, uid, max_age=TEN_YEARS, httponly=True)
        logger.debug('Set Cookies, uid = %s', uid)
        logger.info('Uid Function Call End')
        return response

    def generate_uid(self, request):
        logger.info('Generate Uid Start')
        try:
            uid = request.COOKIES[USER_KEY]
        except KeyError:
            uid = uuid.uuid4().hex
            logger.error('Generate New Uid: %s', uid)
        logger.info('Generate Uid End')
        return uid
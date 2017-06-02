# encoding: utf-8
'''
Created on 2015-2-5
@do: unit test
@author: leo.liu
'''
import inspect
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase

class FwTestCase(TestCase):
    
    def __init__(self, *args, **kwargs):
        self.req_url = None
        self.user = None
        self.user_name = 'fw_user'
        self.user_email = 'fw_user@fuwo.com'
        self.user_pwd = '123456'
        return super(FwTestCase, self).__init__(*args, **kwargs)
    
    def _create_user(self, user_name=None, user_email=None):
        user_name = user_name or self.user_name
        email = user_email or self.user_email
        return User.objects.create_user(username=user_name, email=email, password=self.user_pwd)
        
    def _init_user(self):
        self.user = self._create_user()
        
    def _login(self):
        if self.user == None:
            self._init_user()
        self.client.login(email=self.user_email, password=self.user_pwd)
    
    def _logout(self):
        self.client.logout()
        
    def _function_name(self):
        #=======================================================================
        # return sys._getframe().f_code.co_name
        #=======================================================================
        return inspect.stack()[1][3]
        
    def _post(self, data={}, **kwargs):
        return self.client.post(self.req_url, data, **kwargs)
        
    def _post_ajax(self, data={}, **kwargs):
        kwargs['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        return self.client.post(self.req_url, data, **kwargs)
    
    def _get(self, data={}, **kwargs):
        return self.client.get(self.req_url, data, **kwargs)
    
    def _get_ajax(self, data={}, **kwargs):
        kwargs['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        return self.client.get(self.req_url, data, **kwargs)
    
    def assertHttpCodeEqual(self, status_code, real_code):
        """
        @status_code: 预期返回的http code
        @real_code: 实际返回的code
        """
        self.assertEqual(status_code, real_code, 'http响应异常：code-%s' % real_code)
    
    def assertRedirect(self, response, redirect=None):
        redirect = redirect or self.req_url
        self.assertRedirects(response, '%s?next=%s'%(settings.LOGIN_URL, redirect), 302)
        
    def assertParamError(self, pkey, resp_msg, method='POST', less=True, assert_msg=None):
        method = method.upper()
        expected = u'缺少%s参数%s' % (method, pkey) if less else u'参数%s格式错误' % pkey
        assert_msg = assert_msg or expected
        
        self.assertEqual(expected, resp_msg, assert_msg)
        
    def assertAjaxSucc(self, resp, msg='succ'):
        self.assertEqual(10000, int(resp['code']), msg)
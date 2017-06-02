# #!/usr/bin/env python
# # coding: utf-8
# '''
# Created on 2011-4-20
#
# @author: butter
# '''
# from functools import wraps
# import ujson as json
#
# from django.conf import settings
# from django.http import HttpResponse
# from django.template.response import TemplateResponse
# from django.utils.decorators import available_attrs
#
# from common.utils.crypto import decrypto
#
# def user_encrypto(view_func):
#     '''
#     function : 加密
#                已登录用户信息加密，对 uid ,uname 进行des 加密生成 rnd
#     @param view_func:
#     @return:
#     '''
#     def wrapped_view(request,*args, **kwargs):
#         u_encrypto = {}
#         u_encrypto['uid'] = request.user.id
#         u_encrypto['uname'] = request.user.username
#         #u_encrypto['rnd'] = encrypto('%s,%s' % (request.user.id, request.user.username))
#         request.u_encrypto = u_encrypto
#         return view_func(request,*args,**kwargs)
#
#     return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)
#
# def user_decrypto(ajax=False):
#     '''
#     function : 解密
#                等同于用户校验 , 对post过来的rnd进行解密，并与uid，uname 比对
#     @param view_func:
#     @return:
#     '''
#     def decorator(view_func):
#         @wraps(view_func, assigned=available_attrs(view_func))
#         def wrapped_view(request,*args, **kwargs):
#             uid = request.POST.get('uid','')
#             uname = request.POST.get('uname','')
#             u_decrypto = decrypto(request.POST['rnd']).decode('utf8')
#             if u_decrypto == '%s,%s' % (uid, uname):
#                 return view_func(request, *args, **kwargs)
#             else:
#                 if request.is_ajax() or ajax:
#                     response = HttpResponse(json.dumps(settings.ERROR['PERM_ERR']),
#                                             content_type='application/json')
#                 else:
#                     response = TemplateResponse(request, settings.ERROR_TEMPLATE, {'rsp_data': settings.ERROR['PERM_ERR']})
#                 return response
#
#         return wrapped_view
#
#     return decorator

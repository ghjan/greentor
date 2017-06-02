# encoding: utf-8
'''
Created on 2015-11-13
@author: leo.liu
'''

from django.core.cache import cache

from common import settings as common_settings

def set_proxy_ip_cache(value, timeout=common_settings.COMMON_PROXY_IP_CACHE_TIME):
    
    cache.set(common_settings.COMMON_PROXY_IP_CACHE_KEY, value, timeout=timeout)
    
def get_proxy_ip_cache():
    
    return cache.get(common_settings.COMMON_PROXY_IP_CACHE_KEY)

def get_proxy_ips():
    
    ips = get_proxy_ip_cache()
    if ips is None:
        ips = common_settings.COMMON_PROXY_IPS
    
    return ips

#===============================================================================
# def get_proxy_ip_by_xicidaili():
#    headers = {
#        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#        'Accept-Encoding':'gzip, deflate, sdch',
#        'Accept-Language':'zh-CN,zh;q=0.8',
#        'Cache-Control':'max-age=0',
#        'Connection':'keep-alive',
#        'Cookie':'_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTlmMmE5NWRkZWUyMTc0NzFhZGQxMWQwYzA1MWZjMjJhBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMTVZbnczM1dQejZMTm5GQ3RKbWkrcGdlRFRwTU9pWWdWeDZHQU5vTzJKSVE9BjsARg%3D%3D--e15f200ca900717c254f6c3ceedd6a5fc83d59b6; CNZZDATA4793016=cnzz_eid%3D1279102082-1440902232-%26ntime%3D1447390558',
#        'Host':'www.xicidaili.com',
#        'Upgrade-Insecure-Requests':1,
#        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36'
#    }
#    request = urllib2.Request('http://www.xicidaili.com/', headers=headers)
#    req = urllib2.urlopen(request)
#    html = req.read()
#    req.close()
#    html = gzip_read(html)
#    
#    soup = BeautifulSoup(html.decode('utf-8'))
#    ip_trs = soup.find('table', attrs={"id":"ip_list"}).findAll('tr')[2:22]
#    
#    ips = []
#    for tr in ip_trs:
#        tds = tr.findAll('td')
#        ip = tds[1].text.strip()
#        port = tds[2].text.strip()
#        ips.append('%s:%s' % (ip, port))
#    
#    return ips
#    
# def get_proxy_ip_by_haodailiip():
#    
#    headers = {
#        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#        'Accept-Encoding':'gzip, deflate, sdch',
#        'Accept-Language':'zh-CN,zh;q=0.8',
#        'Cache-Control':'max-age=0',
#        'Connection':'keep-alive',
#        'Cookie':'_um_uuid=ae818596e0764e10a95c64b9035285ca; JSESSIONID=062F4127B2068F6A7644E40F1017C9A9; Hm_lvt_95c1fea0a8f3a2d0ab6485ccc0c52b6d=1445496749; Hm_lpvt_95c1fea0a8f3a2d0ab6485ccc0c52b6d=1447385730; CNZZDATA1253456113=1990763136-1442798605-%7C1447384745',
#        'Host':'www.haodailiip.com',
#        'Upgrade-Insecure-Requests':1,
#        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36'
#    }
#    request = urllib2.Request('http://www.haodailiip.com/', headers=headers)
#    req = urllib2.urlopen(request)
#    html = req.read()
#    req.close()
#    html = gzip_read(html)
#    
#    soup = BeautifulSoup(html.decode('utf-8'))
#    ip_table = soup.findAll("table", attrs={"class":"proxy_table"})[1]
#    ip_trs = ip_table.findAll('tr')[1:]
#    
#    ips = []
#    for tr in ip_trs:
#        tds = tr.findAll('td')
#        ip = tds[0].text.strip()
#        port = tds[1].text.strip()
#        ips.append('%s:%s' % (ip, port))
#    
#    return ips
#===============================================================================
    
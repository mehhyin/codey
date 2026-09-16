"""Offline API transport for WebAssembly, which has no listening TCP sockets.

The learner still uses urllib, JSON, HTTPError, and pagination. Requests to the
practice address are served by this fixture rather than sent to the network.
"""
import io
import json
import urllib.request
from urllib.error import HTTPError
from urllib.parse import urlparse,parse_qs

base_url='https://practice.codey.invalid'
requests=[]

def practice_urlopen(url,timeout=None,**kwargs):
    address=url.full_url if hasattr(url,'full_url') else url
    if not address.startswith(base_url+'/'):
        raise OSError('This exercise supports the offline practice API only.')
    parsed=urlparse(address); path=parsed.path
    requests.append(path+('?' + parsed.query if parsed.query else ''))
    query=parse_qs(parsed.query)
    status=200
    if path=='/status': data={'ok':True}
    elif path=='/search': data={'query':query.get('q',[''])[0]}
    elif path=='/orders':
        data={'items':[{'id':1,'amount':10},{'id':2,'amount':20}],'next':'/orders?page=2'} if query.get('page',['1'])[0]=='1' else {'items':[{'id':3,'amount':5}],'next':None}
    elif path=='/unstable':
        status=503 if requests.count('/unstable')==1 else 200
        data={'ok':status==200}
    else: status,data=404,{'error':'not found'}
    if status!=200: raise HTTPError(address,status,'Practice API response',{},None)
    response=io.BytesIO(json.dumps(data).encode());response.status=200
    return response

urllib.request.urlopen=practice_urlopen

from typing import List
import requests
from structure import File
def GetToken(appkey:str,secretkey:str,code:str):
    paras={'grant_type':'authorization_code','code':code,'client_id':appkey,'client_secret':secretkey,'redirect_uri':'oob'}
    url='https://openapi.baidu.com/oauth/2.0/token'
    try:
        re=requests.get(url=url,params=paras)
    except:
        print('Network error [17]')
        return -1,'',''
    data=re.json()
    if data.get('error')!=None:
        print('Authentication failed:')
        print(data['error'])
        print(data['error_description'])
        return -1,'',''
    return 0,data['access_token'],data['refresh_token']
def RefreshToken(appkey:str,secretkey:str,refresh_token:str):
    paras={'grant_type':'refresh_token','refresh_token':refresh_token,'client_id':appkey,'client_secret':secretkey}
    url='https://openapi.baidu.com/oauth/2.0/token'
    try:
        re=requests.get(url=url,params=paras)
    except:
        print('Network error [17]')
        return -1,'',''
    data=re.json()
    if data.get('error')!=None:
        print('Cannot refresh: ')
        print(+data['error'])
        print(+data['error_description'])
        return -1,'',''
    return 0,data['access_token'],data['refresh_token']
def GetUserInfo(access_token:str):
    url='https://pan.baidu.com/rest/2.0/xpan/nas?method=uinfo'
    paras={'access_token':access_token}
    try:
        re=requests.get(url=url,params=paras)
    except:
        print('Network error')
        return -1,'','',0,0
    data=re.json()
    if data['errno']!=0:
        print('Cannot fetch user info')
        print(data['errno'])
        print(data['errmsg'])
        return -1,'','',0,0
    return 0,data['baidu_name'],data['netdisk_name'],data['uk'],data['vip_type']
def GetDiskInfo(access_token:str):
    url='https://pan.baidu.com/api/quota'
    paras={'access_token':access_token}
    try:
        re=requests.get(url=url,params=paras)
    except:
        print('Network error [17]')
        return -1,0,0
    data=re.json()
    if data['errno']!=0:
        print('Failed to get info: ')
        print(data['errno'])
        return -1,0,0
    return 0,data['used'],data['total']
def GetList(access_token:str,path:str='/'):
    file_list=[]
    url='https://pan.baidu.com/rest/2.0/xpan/file'
    paras={'method':'list','access_token':access_token,'dir':path}
    try:
        re=requests.get(url=url,params=paras)
    except:
        print('Failed to get files list [17]')
        return -1,[]
    data=re.json()
    if data['errno']!=0:
        print('Failed to get files list: ')
        print(data['errno'])
        return -1,[]
    for index in data['list']:
        file=File(index['server_filename'],index['fs_id'],index['path'],index['isdir'],index['size'])
        file_list.append(file)
    return 0,file_list
def GetLink(access_token:str,fs_id:list):
    file_list=[]
    files='['
    for file in fs_id:
        if file.is_dir!=1:
            files+=str(file.fs_id)+','
    if files[0:-1]!='':
        files=files[0:-1]+']'
    else:
        files='[]'
    url='http://pan.baidu.com/rest/2.0/xpan/multimedia'
    paras={'method':'filemetas','access_token':access_token,'fsids':files,'dlink':1}
    try:
        re=requests.get(url=url,params=paras)
    except:
        print('Failed to fetch link [17]')
        return -1,''
    data=re.json()
    if data['errno']!=0:
        print('Failed to fetch link')
        print(data['errno'])
        return -1,''
    for index in data['list']:
        file=File(index['filename'],index['fs_id'],index['path'],index['isdir'],index['size'],index['md5'],index['dlink']+'&access_token=%s'%(access_token))
        file_list.append(file)
    return 0,file_list

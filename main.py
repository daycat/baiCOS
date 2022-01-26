# ------------------------------------------------------
# fetching downloadable links from files in BaiduNetdisk
#
# @daycat 2022
# Released under the MIT license
# Contact me via:
# Telegram: @daycat
# Email: iyasmalan@gmail.com
# Special thanks to: 鹿乃ちゃんの猫
# ------------------------------------------------------


import os
import baidunetdisk
import json
appkey='cEmmwG9POQXvgg2EhZ4LXyXYkOGFuwhW'
secretkey='oIeInf6uOX6xadrCopUKaB5v0KzzrxGv'
access_token=''
path='/'
files=[]
dl_files=[]
url='http://openapi.baidu.com/oauth/2.0/authorize?response_type=code&client_id=cEmmwG9POQXvgg2EhZ4LXyXYkOGFuwhW&redirect_uri=oob&scope=basic,netdisk&qrcode=1'
print('baiCOS | By daycat & 鹿乃ちゃんの猫')
print('release version: 0.1')
print('Attempting to use config.json to login......')
if os.path.exists('config.json'):
    with open('config.json','r',encoding='utf-8') as fp:
        config=json.load(fp)
        refresh_token=config['refresh_token']
    status,access_token,refresh_token=baidunetdisk.RefreshToken(appkey,secretkey,refresh_token)
    if status!=0:
        print('Login failed. Please check your network settings')
        exit()
    with open('config.json','w',encoding='utf-8') as fp:
        data={"refresh_token":refresh_token}
        json.dump(data,fp)
else:
    print("You haven't logged in!")
    print('Please use right click + copy / paste instead of Ctrl + C/V')
    print('Login url: %s'%(url))
    code=input('Please enter your authentication code:')
    status,access_token,refresh_token=baidunetdisk.GetToken(appkey,secretkey,code)
    if status!=0:
        print('Authentication failed. Please retry login.')
        exit()
    with open('config.json','w',encoding='utf-8') as fp:
        data={"refresh_token":refresh_token}
        json.dump(data,fp)
status,baidu_name,netdisk_name,uk,vip_type=baidunetdisk.GetUserInfo(access_token)
if status!=0:
    exit()
print(f'{netdisk_name}({baidu_name}) is now logged in!')
print(f'UserID：%d Status: %s'%(uk,str(vip_type).replace('0','Free').replace('1','VIP').replace('2','VIP2')))
status,used,total=baidunetdisk.GetDiskInfo(access_token)
print('Used storage: %.2fGB Total: %.2fGB'%(used/1073741824.0,total/1073741824.0))
print('To sign out of this account, delete the config.json file and then restart the program.')
while True:
    print('PWD: %s'%(path))
    print('0. cd \n1. ls \n2. get link\n3. output links to file\n4. exit')
    select=int(input(':'))
    if select==0:
        temp=input('Please enter the directory: ')
        status,swap=baidunetdisk.GetList(access_token,temp)
        if status!=0:
            print('Directory does not exist [404]')
            continue
        else:
            path=temp
            files=swap
            print('Success [200]')
    elif select==1:
        status,swap=baidunetdisk.GetList(access_token,path)
        if status!=0:
            print('Network error [17]')
            continue
        else:
            files=swap
            for file in files:
                file.pathmate()
    elif select==2:
        status,dl_files=baidunetdisk.GetLink(access_token,files)
        if status!=0:
            print('Failed. [17]')
        else:
            for file in dl_files:
                file.filemate()
        print("Please set your user-agent to 'pan.baidu.com' when downloading.")
        print('The link will expire in 8 hours')
    elif select==3:
        status,dl_files=baidunetdisk.GetLink(access_token,files)
        if status!=0:
            print('Failed. [17]')
        else:
            name=input('File to save to: ')
            if name=='':
                print('File name cannot be empty [18]')
            else:
                data='Please set your user-agent to "pan.baidu.com" when downloading \n The link will expire in 8 hours'
                for file in dl_files:
                    data+='File: %s ID：%d\nPath: %s\nSize: %.2fMB Hash：%s\nLink: %s\n'%(file.name,file.fs_id,file.path,file.size,file.md5,file.dlink)
                with open(name,'w',encoding='utf-8')as fp:
                    fp.write(data)
                print('Success [200]')
                print("Please set your user-agent to 'pan.baidu.com' when downloading")
                print('The link will expire in 8 hours')
    elif select==4:
        print('Exit [0]')
        exit()
    else:
        print('Unknown operation [19]')

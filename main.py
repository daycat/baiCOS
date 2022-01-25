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
print('欢迎使用百度网盘直链助手！作者：鹿乃ちゃんの猫 版本：v0.1')
print('尝试加载config.json进行登录......')
if os.path.exists('config.json'):
    with open('config.json','r',encoding='utf-8') as fp:
        config=json.load(fp)
        refresh_token=config['refresh_token']
    status,access_token,refresh_token=baidunetdisk.RefreshToken(appkey,secretkey,refresh_token)
    if status!=0:
        print('登陆失败，请检查网络设置！')
        exit()
    with open('config.json','w',encoding='utf-8') as fp:
        data={"refresh_token":refresh_token}
        json.dump(data,fp)
else:
    print('您还没有登录本系统！')
    print('请不要使用ctrl+c/v进行复制粘贴!!!在本程序中选择内容按鼠标右键即可复制，按鼠标右键即可粘贴')
    print('请在浏览器中打开本链接获取授权码：%s'%(url))
    code=input('请输入授权码：')
    status,access_token,refresh_token=baidunetdisk.GetToken(appkey,secretkey,code)
    if status!=0:
        print('获取授权失败，请检查输入是否有误')
        exit()
    with open('config.json','w',encoding='utf-8') as fp:
        data={"refresh_token":refresh_token}
        json.dump(data,fp)
status,baidu_name,netdisk_name,uk,vip_type=baidunetdisk.GetUserInfo(access_token)
if status!=0:
    exit()
print(f'{netdisk_name}({baidu_name})欢迎登陆！')
print(f'您的用户ID为：%d 账号类型为：%s'%(uk,str(vip_type).replace('0','普通用户').replace('1','普通会员').replace('2','超级会员')))
status,used,total=baidunetdisk.GetDiskInfo(access_token)
print('已用空间：%.2fGB 总空间：%.2fGB'%(used/1073741824.0,total/1073741824.0))
print('若需切换账号请删除config.json后重新运行')
while True:
    print('当前工作路径：%s'%(path))
    print('请选择您要执行的操作：\n(0)切换工作路径\n(1)打印文件列表\n(2)获取直链列表\n(3)输出直链列表到文件\n(4)退出系统')
    select=int(input('请输入操作的序号：'))
    if select==0:
        print('请不要使用ctrl+c/v进行复制粘贴!!!在本程序中选择内容按鼠标右键即可复制，按鼠标右键即可粘贴')
        print('请输入要切换到的路径(以/开头中间不要有空格)')
        temp=input('切换到：')
        status,swap=baidunetdisk.GetList(access_token,temp)
        if status!=0:
            print('操作失败！路径不存在或网络错误')
            continue
        else:
            path=temp
            files=swap
            print('操作成功！')
    elif select==1:
        status,swap=baidunetdisk.GetList(access_token,path)
        if status!=0:
            print('操作失败！网络错误')
            continue
        else:
            files=swap
            for file in files:
                file.pathmate()
    elif select==2:
        status,dl_files=baidunetdisk.GetLink(access_token,files)
        if status!=0:
            print('操作失败，请检查网络设置')
        else:
            for file in dl_files:
                file.filemate()
        print("请务必在您的下载工具中将User-Agent设置为pan.baidu.com")
        print('否则无法下载！！！链接将于8小时后失效')
    elif select==3:
        status,dl_files=baidunetdisk.GetLink(access_token,files)
        if status!=0:
            print('操作失败，请检查网络设置')
        else:
            print('请不要使用ctrl+c/v进行复制粘贴!!!在本程序中选择内容按鼠标右键即可复制，按鼠标右键即可粘贴')
            print('请输入要保存的文件名')
            name=input('保存至：')
            if name=='':
                print('文件名不能为空！')
            else:
                data='请务必在您的下载工具中将User-Agent设置为pan.baidu.com\n否则无法下载！！！链接将于8小时后失效\n'
                for file in dl_files:
                    data+='文件名：%s 文件ID：%d\n绝对路径：%s\n文件大小：%.2fMB MD5：%s\n下载地址：%s\n'%(file.name,file.fs_id,file.path,file.size,file.md5,file.dlink)
                with open(name,'w',encoding='utf-8')as fp:
                    fp.write(data)
                print('保存成功！')
                print("请务必在您的下载工具中将User-Agent设置为pan.baidu.com")
                print('否则无法下载！！！链接将于8小时后失效')
    elif select==4:
        print('本程序将退出')
        exit()
    else:
        print('无效的操作！')

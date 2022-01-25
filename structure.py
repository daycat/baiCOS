class File():
    name=''
    fs_id=0
    path=''
    is_dir=0
    size=0.0
    md5=''
    dlink=''
    def __init__(self,name:str,fs_id:int,path:str,is_dir:int=0,size:int=0,md5:str='',dlink:str=''):
        self.name=name
        self.fs_id=fs_id
        self.path=path
        self.is_dir=is_dir
        self.size=size/1048576.0
        self.md5=md5
        self.dlink=dlink
    def pathmate(self):
        print('文件名：%s 文件ID：%d 是否目录：%d\n绝对路径：%s'%(self.name,self.fs_id,self.is_dir,self.path))
        print('-----------------------------------------------------------------------------------------------------------------------')
    def filemate(self):
        print('文件名：%s 文件ID：%d\n绝对路径：%s\n文件大小：%.2fMB MD5：%s\n下载地址：%s'%(self.name,self.fs_id,self.path,self.size,self.md5,self.dlink))
        print('-----------------------------------------------------------------------------------------------------------------------')
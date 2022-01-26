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
        print('Filename: %s ID：%d Directory? %d\nPath: %s'%(self.name,self.fs_id,self.is_dir,self.path))
        print('-----------------------------------------------------------------------------------------------------------------------')
    def filemate(self):
        print('Filename: %s ID：%d\nDirectory? %s\nSize: %.2fMB Hash：%s\nLink: %s'%(self.name,self.fs_id,self.path,self.size,self.md5,self.dlink))
        print('-----------------------------------------------------------------------------------------------------------------------')

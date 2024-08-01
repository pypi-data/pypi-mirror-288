from wata.file.utils import utils, file_tree_utils # 不能去掉
from pathlib import Path
from numpy import ndarray

class FileProcess:

    @staticmethod
    def load_file(path:str|Path):
        '''
        **功能描述**: 读取文件,支持 txt pkl json geojson yaml 格式  
        
        Args:
            path: 加载文件的路径  

        Returns:
            文件内容  
        '''
        return utils.load_file(path)

    @staticmethod
    def save_file(data, save_path):
        '''
        **功能描述**: 保存文件 支持'yaml', 'json', 'pkl', 'txt' 格式  
        
        Args:
            data: 文件内容  
            save_path: 文件保存路径  

        Returns:  
            无  

        '''
        utils.save_file(data, save_path)

    @staticmethod
    def write_file(data, save_path):
        '''
        **功能描述**: 保存文件 支持'yaml', 'json', 'pkl', 'txt' 格式  
        
        Args:
            data: 文件内容  
            save_path: 文件保存路径  

        Returns:
            无

        '''
        utils.save_file(data, save_path)

    @staticmethod
    def file_tree(path, save_txt=None):
        '''
        **功能描述**: 列出文件树  
        
        Args:
            path: 需要列出文件树的路径  
            save_txt: 保存txt时填写为地址,不保存时为None,默认为None  

        Returns:
            无

        '''
        file_tree_utils.file_tree(path, save_txt)

    @staticmethod
    def mkdir(dir_path):
        '''
        **功能描述**: 如果不存在这个目录,则创建  
        
        Args:
            dir_path: 目录地址  

        Returns:
            无
        '''
        utils.mkdir_if_not_exist(dir_path)
    @staticmethod
    def mkdir_if_not_exist(dir_path):
        '''
        **功能描述**: 如果不存在这个目录,则创建  
        
        Args:
            dir_path: 目录地址  

        Returns:
            无  
        '''
        utils.mkdir_if_not_exist(dir_path)

    @staticmethod
    def np2str(arr:ndarray|list, return_type:str|list):
        '''
        **功能描述**: 将numpy 或 list 格式的矩阵转成字符串或者用list存储的字符串  
        
        Args:
            arr: numpy 或者 list 格式的矩阵  
            return_type: 可选"str","list"  

        Returns:  
            list | str  
        '''
        return utils.np2str(arr,return_type)
from wata.pointcloud.utils import utils
from wata.pointcloud.utils import move_pcd
from wata.pointcloud.utils import o3d_visualize_utils
from numpy import ndarray
from pathlib import Path
from typing import Union

class PointCloudProcess:

    @staticmethod
    def cut_pcd(points:ndarray, pcd_range:list, axis:str):
        '''
        **功能描述**: 切割指定范围的点云  
        
        Args:  
            points: numpy格式的点云  
            pcd_range: [x1,y1,z1,x2,y2,z2]  
            axis: 可选 "xy","xz","yz","xz","xyz",默认为"xyz"  

        Returns:  
            返回范围内的点  
        '''
        return utils.cut_pcd(points, pcd_range, axis)

    @staticmethod
    def filter_points(points:ndarray, del_points:ndarray):
        '''
        **功能描述**: 过滤删除部分点,要求del_points是points的子集  
        
        Args:  
            points: numpy格式的点云  
            del_points: 要从points中删除的点,numpy格式的点云  

        Returns:  
            剩余的点,numpy格式  
        '''
        return utils.filter_points(points, del_points)

    @staticmethod
    def show_pcd(path:Union[str, Path], point_size:float=1, background_color:list=None, pcd_range:list=None, bin_num_features:int=None,
                 create_coordinate:bool=True, create_plane:bool=False, type:str='open3d'):
        '''
        **功能描述**: 直接可视化点云文件,目前支持bin pcd npy 格式的点云  
        
        Args:
            path: 点云的路径  
            point_size: 点的大小  
            background_color: 背景颜色  
            pcd_range: 可视化点云的范围  
            bin_num_features: 如果是bin格式的文件,应给出bin格式点云的列数  
            create_coordinate: 是否可视化坐标系  
            create_plane: 是否可视化出一个平面  
            type: 用什么工具可视化, 默认open3d 可选 matplotlib open3d qtopengl mayavi(未开发) vispy(未开发)  

        Returns:  
            直接弹出可视化界面  
        '''
        utils.show_pcd(path, point_size, background_color, pcd_range, bin_num_features,
                       create_coordinate, create_plane, type)

    @staticmethod
    def points_to_o3d_model(points:ndarray, point_colors:Union[None, list]=None):
        '''
        **功能描述**: 将numpy格式的点云转化为open3d模型  
        
        Args:
            points: numpy格式的点云  
            point_colors: 点云的颜色信息,可以为None,可以为长度为3的元素为int类型的RGB列表  

        Returns:  
            open3d模型  
        '''
        return o3d_visualize_utils.points_to_o3d_model(points=points, point_colors=point_colors)

    @staticmethod
    def save_o3d_camera_parameters(points:ndarray, save_file_path:Union[str, Path]='camera_parameters.json', window_size:list=[1200, 800]):
        '''
        **功能描述**:  保存手动调整的open3d的视角  
        
        Args:  
            points: numpy格式的点云  
            save_file_path: open3d 可视化视角文件保存的路径 json  
            window_size: 可视化窗口的大小 list  

        Returns:  
            无  
        '''
        return o3d_visualize_utils.save_o3d_camera_parameters(points, save_file_path, window_size)

    @staticmethod
    def show_pcd_from_points(points:Union[ndarray,list], point_size:float=1, background_color:list=None, colors:Union[list, int]=None, create_coordinate=True,
                             create_plane=False, type='open3d'):
        '''
        **功能描述**: 展示点云  
        
        Args:  
            points: numpy格式的点云;当points为list时代表将list中的numpy格式的点云全部可视化  
            point_size: 可视化点的大小,默认为1  
            background_color: 背景颜色  
            colors: 点云的颜色,当colors为int类型时,为用点云的第几列显色;当colors为list类型时,colors代表[R,G,B]  
            create_coordinate: 是否可视化坐标系  
            create_plane: 是否可视化出一个平面  
            type: 用什么工具可视化, 默认open3d 可选 matplotlib open3d qtopengl mayavi(未开发) vispy(未开发)  

        Returns:  
            无  
        '''
        utils.show_pcd_from_points(points, point_size, background_color, colors, create_coordinate, create_plane, type)

    @staticmethod
    def get_points(path:str, num_features:Union[None, int]=None):
        '''
        **功能描述**: 读取点云文件获取点
        
        Args:
            path: 点云文件的路径支持 pcd npy bin 格式的点云  
            num_features: 当点云文件格式为pcd 或npy时,num_features为加载点的列数; 当点云文件格式为bin时,num_features为bin文件点云的列数  

        Returns:  
            返回numpy格式的点云矩阵  
        '''
        return utils.get_points(path, num_features)

    @staticmethod
    def add_boxes(points:Union[ndarray,list], gt_boxes:Union[ndarray,None]=None, gt_labels:Union[None, list]=None, pred_boxes:Union[ndarray,None]=None, pred_labels:Union[None, list]=None, pred_scores:Union[None, list]=None,
                  point_size:int=1,
                  background_color:list=None, create_plane:bool=False, point_colors:Union[None, list]=None, create_coordinate=True, type='open3d',
                  savepath=None, plot_range=None):
        '''
        **功能描述**: 绘制点云、标注框、预测框  
        
        Args:  
            points: numpy格式的点云;当points为list时代表将list中的numpy格式的点云全部可视化  
            gt_boxes: GT框  
            gt_labels: GT框标签  
            pred_boxes: 预测框  
            pred_labels: 预测框标签  
            pred_scores: 预测框的分数  
            point_size: 可视化点的大小,默认为1  
            background_color: 背景颜色  
            create_plane: 是否创建一个可视化地面  
            point_colors: 对应points为列表时的颜色,当points为numpy格式时不起作用  
            create_coordinate: 是否在原点创建坐标系  
            type: 用什么工具可视化, 默认open3d 可选 matplotlib open3d qtopengl mayavi(未开发) vispy(未开发)  
            savepath: 当type为matplotlib时,保存图像的地址  
            plot_range: 当type为matplotlib时,可视化的范围  

        Returns:  
            可视化界面  
        '''
        utils.add_boxes(points, gt_boxes=gt_boxes, gt_labels=gt_labels, pred_boxes=pred_boxes, pred_labels=pred_labels,
                        pred_scores=pred_scores, point_size=point_size,
                        background_color=background_color, create_plane=create_plane, point_colors=point_colors,
                        create_coordinate=create_coordinate, type=type, savepath=savepath, plot_range=plot_range)

    @staticmethod
    def pcd2bin(pcd_dir:Union[str, Path], bin_dir:Union[str, Path], num_features=4):
        '''
        **功能描述**: pcd格式点云转bin格式  
        
        Args:  
            pcd_dir: pcd格式点云数据的存放目录  
            bin_dir: bin格式点云的数据村帆帆目录  
            num_features: bin格式的点云列数  

        Returns:  
            无  
        '''
        utils.pcd2bin(pcd_dir, bin_dir, num_features)

    @staticmethod
    def xyzrpy2RTmatrix(xyz_rpy, degrees=False):
        '''
        **功能描述**: xyzrpy2RTmatrix  
        
        Args:
            xyz_rpy: list [dx, dy, dz, roll, pitch, yaw]  
            degrees: roll, pitch, yaw 是弧度还是角度 默认为弧度(False)  

        Returns:  
            numpy格式的4x4旋转平移矩阵   
        '''
        return move_pcd.xyzrpy2RTmatrix(xyz_rpy=xyz_rpy, degrees=degrees)

    @staticmethod
    def RTmatrix2xyzrpy(RTmatrix:ndarray):
        '''
        **功能描述**: RTmatrix2xyzrpy  
        
        Args:  
            RTmatrix: numpy格式的4x4旋转平移矩阵  

        Returns:  
            numpy格式1x6矩阵 分别为 dx, dy, dz, roll, pitch, yaw  
        '''
        return move_pcd.RTmatrix2xyzrpy(RTmatrix)

    @staticmethod
    def move_pcd_with_RTmatrix(points:ndarray, RTmatrix:ndarray, inv=False):
        '''
        **功能描述**: 通过旋转平移矩阵移动点云  
        
        Args:
            points: numpy格式的点云  
            RTmatrix: numpy格式的4x4旋转平移矩阵  
            inv: 是否对 RTmatrix 取逆,默认为False  

        Returns:  
            旋转平移后的numpy格式的点云  
        '''
        return move_pcd.move_pcd_with_RTmatrix(points, RTmatrix, inv)

    @staticmethod
    def move_pcd_with_xyzrpy(points:ndarray, xyz_rpy, degrees=False):
        '''
        **功能描述**: 用 dx, dy, dz, roll, pitch, yaw 旋转平移点云  
        
        Args:  
            points: numpy格式的点云,需要有x,y,z维度  
            xyz_rpy: 列表格式[dx, dy, dz, roll, pitch, yaw]  
            degrees: xyz_rpy 中的roll, pitch, yaw是否为角度值,默认为False  

        Returns:  
            返回旋转平移后的点云  
        '''
        return move_pcd.move_pcd_with_xyzrpy(points, xyz_rpy, degrees=degrees)

    @staticmethod
    def cartesian_to_spherical(points:ndarray):
        '''
        **功能描述**: 直角坐标系转笛卡尔坐标系  
        
        Args:  
            points: 直角坐标系点云  

        Returns:
            (r, theta, phi)的numpy格式点云  
        '''
        return utils.cartesian_to_spherical(points=points)

    @staticmethod
    def get_v_channel_from_pcd(points:ndarray, vfov, channel_nums, offset=0.01):
        '''
        **功能描述**: 获取垂直方向的通道  
        
        Args:  
            points: numpy格式的点云,需要有x,y,z维度  
            vfov: 长度为2的列表,代表了垂直视场角的范围,水平方向为0度,低于水平方向为负  
            channel_nums: 垂直通道的线数  
            offset: 偏移量  

        Returns:  
            numpy格式的 nx1 的数组  
        '''
        return utils.get_v_channel_from_pcd(points, vfov, channel_nums, offset)

    @staticmethod
    def get_h_channel_from_pcd(points:ndarray, hfov, channel_nums, offset=0.001):
        '''
        **功能描述**: 获取点云水平方向的通道  
        
        Args:
            points: numpy格式的点云,需要有x,y,z维度  
            hfov: 长度为2的列表,代表了水平视场角的范围,前向120度的视场角可用[30,150]表示  
            channel_nums: 水平通道的线数  
            offset: 偏移量  

        Returns:
            numpy格式的 nx1 的数组  
        '''
        return utils.get_h_channel_from_pcd(points, hfov, channel_nums, offset)

    @staticmethod
    def points_in_boxes(points:ndarray, boxes, type="gpu"):
        '''
        **功能描述**: 此API需要安装pytorch,用于标记和查找点云中在指定框内的点  
        
        Args:
            points: numpy格式的点云,需要有x,y,z维度  
            boxes: nx7的numpy矩阵  
            type: 可选"gpu" "cpu"  

        Returns:
            返回每个点所在框的索引列表  
        '''
        return utils.points_in_boxes(points, boxes, type)

    @staticmethod
    def save_pcd(points:ndarray, save_path, fields=None, npdtype=None, type='binary'):
        '''
        **功能描述**: 保存pcd格式的点云  
        
        Args:
            points: numpy格式的点云  
            save_path: pcd格式的点云文件保存的路径  
            fields: 点云每一列的元信息,当为None时默认为["x","y","z","4","5",....]  
            npdtype: 点云每一列保存的数据类型,支持numpy格式和字符串格式。字符串格式可选 "f32","f64","i8","i16","i32","i64","u8","u16","u32","u64"  
            type: 有两种格式,分别为“binary” 和 “ascii”,默认为“binary”。binary格式保存为二进制文件,ascii保存为普通文件  

        Returns:  
            无  
        '''
        return utils.save_pcd(points, save_path, fields, npdtype, type)

# 计算机登录用户: jk
# 系统日期: 2024/6/25 17:10
# 项目名称: chipeak_cv_data_tool
# 开发者: zhanyong

import os
import shutil
from pathlib import Path
from tqdm import *
from ccdt.dataset import *
import subprocess


class BaseYolo(BaseLabelme):
    def __init__(self, *args, **kwargs):
        self.yolo_path = args[1].output_dir  # 获取yolo数据集输出目录路径
        # 在这里定义labelme数据结构格式初始化
        super(BaseYolo, self).__init__(*args, **kwargs)

    def labelme2yolo(self):
        """
        labelme转yolo数据集
        """
        print("labelme转yolo开始*********************")
        for dataset in tqdm(self.datasets):
            output_dir = dataset.get('output_dir')
            input_dir = dataset.get('input_dir')
            image_file_stem = Path(dataset.get('image_file')).stem  # 获取文件前缀
            class_names = []  # 类别和坐标
            # yolo_txt_dir_path = os.path.join(output_dir, dataset.get('labelme_dir'), "labels")
            # yolo_image_dir_path = os.path.join(output_dir, dataset.get('image_dir'), "images")
            yolo_txt_dir_path = os.path.join(output_dir, "labels")  # 默认开源工程部能够嵌套目录
            yolo_image_dir_path = os.path.join(output_dir, "images")
            yolo_txt_file_path = os.path.join(yolo_txt_dir_path, image_file_stem + ".txt")  # 替换 .replace('\\', '/')
            os.makedirs(yolo_txt_dir_path, exist_ok=True)  # 创建yolo格式标注数据目录
            os.makedirs(yolo_image_dir_path, exist_ok=True)  # 创建yolo格式图片目录
            # # 定义用户和组
            # user = 'scanner'
            # group = 'sambashare'
            # # 修改目录权限
            # # os.chmod(yolo_txt_file_path, 0o775)
            # os.chmod(yolo_image_dir_path, 0o775)
            # # 修改目录所有者和组
            # # subprocess.run(['chown', f'{user}:{group}', yolo_txt_file_path], check=True)
            # subprocess.run(['chown', f'{user}:{group}', yolo_image_dir_path], check=True)
            width = dataset.get('image_width')
            height = dataset.get('image_height')
            if dataset.get('background') is True:
                for index, shape in enumerate(dataset.get('labelme_info').get('shapes')):
                    # 获取边界框坐标
                    points = shape["points"]
                    xmin = min(points[0][0], points[1][0])
                    ymin = min(points[0][1], points[1][1])
                    xmax = max(points[0][0], points[1][0])
                    ymax = max(points[0][1], points[1][1])
                    # 转换为 YOLO 格式 (class, x_center, y_center, width, height)
                    x_center = (xmin + xmax) / 2.0 / width
                    y_center = (ymin + ymax) / 2.0 / height
                    bbox_width = (xmax - xmin) / width
                    bbox_height = (ymax - ymin) / height
                    # print(index, x_center, y_center, bbox_width, bbox_height)
                    class_names.append([index, x_center, y_center, bbox_width, bbox_height])
            # 检查目录写入权限
            # if self.check_write_permission(yolo_txt_file_path):
            #     print(f"目录 {yolo_txt_file_path} 具有写入权限。")
            # else:
            #     print(f"目录 {yolo_txt_file_path} 不具有写入权限。")
            # 保存类别文件
            with open(yolo_txt_file_path, "w") as class_f:
                for class_name in class_names:
                    # 将每个 class_name=[0, 0.5012201365187713, 0.5480937499999999, 0.9975597269624574, 0.8811562500000001] 中的值以 YOLO 格式写入文件
                    class_f.write(" ".join(map(str, class_name)) + "\n")
            # 拷贝图像
            shutil.copy(dataset.get('full_path'), yolo_image_dir_path)

    @staticmethod
    def check_write_permission(directory):
        return os.access(directory, os.W_OK)

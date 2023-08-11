import my_utils
from my_utils.file_operations import *
from my_utils import *
if __name__ == '__main__':
    folder_path = r'D:\Documents\DataSet\RXSK\罂粟数据\labels\val'  # 文件夹路径
    output_file = r'D:\Documents\DataSet\RXSK\罂粟数据\labels\val.txt'  # 输出文件路径
    file_batch_processing.get_file_names(folder_path, output_file)
    my_utils.file_operations.file_check()
    file_batch_processing.get_file_names()
    image_enhancement.retinex
    print("end")

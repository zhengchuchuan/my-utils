import os
import random
import shutil


def check_file_correspondence(folder_1, folder_2):
    """
    检查不同后缀的文件去除文件名后是否一一对应
    :param folder_1: 
    :param folder_2: 
    :return: 
    """
    # 获取文件夹下的所有文件名
    file_list_1 = os.listdir(folder_1)
    file_list_2 = os.listdir(folder_2)
    # 分离文件名(路径名)和拓展名,return [文件名,带点后缀名如.jpg]
    file_name_list_1, file_suffix_list_1 = [os.path.splitext(file) for file in file_list_1]
    file_name_list_2, file_suffix_list_2 = [os.path.splitext(file) for file in file_list_2]
    # 计算补集,即为缺失文件
    missing_list_2_files = set(file_name_list_1) - set(file_name_list_2)
    missing_list_1_files = set(file_name_list_2) - set(file_name_list_1)
    # 有缺失文件
    if missing_list_1_files:
        print("{0}以下的文件缺少对应的文件:".format(folder_1))
        for file in missing_list_1_files:
            print(file + file_suffix_list_1)
    if missing_list_2_files:
        print("{0}以下的文件缺少对应的文件:".format(folder_2))
        for file in missing_list_2_files:
            print(file + file_suffix_list_2)
    # 无缺失文件
    if not missing_list_2_files and not missing_list_1_files:
        print("所有文件一一对应。")


def copy_files_from_folder(src_folder_path, dest_folder_path, file_list):
    """
    将文件夹下的文件,根据一个文件名列表复制到指定目录下
    :param src_folder_path: 待复制的文件夹路径
    :param dest_folder_path: 目标文件夹路径
    :param file_list: 移动的文件名列表
    :return: None
    """
    for file_name in file_list:
        source_file_path = os.path.join(src_folder_path, file_name)

        try:
            # 移动文件袋指定文件夹
            shutil.copy(source_file_path, dest_folder_path)
        except FileNotFoundError:
            print(f"File '{file_name}' not found in the source folder.")
        except FileExistsError:
            print(f"File '{file_name}' already exists in the destination folder.")
        except Exception as e:
            print(f"An error occurred while moving '{file_name}': {e}")


# 划分VOC格式数据集
def voc_dataset_division(voc_root_folder, xml_file_path, train_proportion=0.7, trainval_proportion=0.8):
    """
    划分voc数据集,并将数据保存在voc数据集格式的对应文件夹下
    :param voc_root_folder: voc格式数据集的根目录,07或者12,用于保存文件
    :param xml_file_path: 待划分的xml文件目录
    :param train_proportion: 训练集比例
    :param trainval_proportion: 训练验证集比例
    :return: None
    """
    # 获取xml文件名列表
    total_xml = os.listdir(xml_file_path)
    # 计算划分数据的索引
    file_length = len(total_xml)  # 文件数量
    file_index_list = range(file_length)  # 文件索引列表
    # 计算详细划分的个数
    trainval_index = int(file_length * trainval_proportion)  
    train_index = int(trainval_index * train_proportion)  
    # 返回训练验证集的划分索引
    trainval_index = random.sample(file_index_list, trainval_index)
    # 在训练验证集上继续划分
    train_index = random.sample(trainval_index, train_index)
    # 打开txt文件,没有则创建
    trainval_file = open(voc_root_folder + 'ImageSets\\Main\\trainval.txt', 'w')
    test_file = open(voc_root_folder + 'ImageSets\\Main\\test.txt', 'w')
    train_file = open(voc_root_folder + 'ImageSets\\Main\\train.txt', 'w')
    val_file = open(voc_root_folder + 'ImageSets\\Main\\val.txt', 'w')
    # 划分数据并写入文件
    for i in file_index_list:
        # voc格式保存的标签不带后缀,一行一个内容
        name = total_xml[i][:-4] + '\n'
        # 属于训练验证集
        if i in trainval_index:
            trainval_file.write(name)
            # 属于训练集
            if i in train_index:
                train_file.write(name)
            # 属于验证集
            else:
                val_file.write(name)
        # 测试集
        else:
            test_file.write(name)
    # 关闭文件
    trainval_file.close()
    train_file.close()
    val_file.close()
    test_file.close()


# 将文件夹下的文件名称合并到一个txt文件中
def get_file_names_from_folder(folder_path, txt_save_path):
    """
    将文件夹下的所有文件的名称合并到一个txt文件中,一个文件名占一行
    未处理文件夹嵌套
    :param folder_path:文件夹的路径
    :param txt_save_path:文本文件保存路径
    :return:None
    """
    try:
        # 获取文件夹下的所有文件
        files = os.listdir(folder_path)
    except FileNotFoundError:
        print("文件路径:{}不存在".format(folder_path))
    # 提取文件名（不包括后缀名）
    file_names = [os.path.splitext(file)[0] for file in files]

    # 将文件名保存到txt文件中
    with open(txt_save_path, 'w') as f:
        f.write('\n'.join(file_names))

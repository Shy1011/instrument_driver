import datetime
import os

class TxtFileHandler:
    def __init__(self, file_name, save_path, mode='w', show_content=False, save_file=True, use_timestamp=True):
        """
        初始化TxtFileHandler类

        :param file_name: 指定的文件名（不带后缀）
        :param save_path: 保存文件的绝对路径
        :param mode: 打开模式，'w'为覆盖，'a'为追加
        :param show_content: 是否在写入时显示内容
        :param save_file: 是否保存文件
        :param use_timestamp: 是否使用时间戳（默认True）
        """
        self.file_name = file_name
        self.save_path = save_path
        self.mode = mode
        self.show_content = show_content
        self.save_file = save_file
        self.use_timestamp = use_timestamp
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S") if use_timestamp else ""  # 根据参数决定是否生成时间戳

    def write_to_txt(self, content):
        """
        将内容写入TXT文件

        :param content: 要写入的内容（字符串或字符串列表）
        """
        # 生成完整的文件路径
        if self.use_timestamp:
            full_file_path = os.path.join(self.save_path, f"{self.timestamp}_{self.file_name}.txt")
        else:
            full_file_path = os.path.join(self.save_path, f"{self.file_name}.txt")

        # 如果需要保存文件
        if self.save_file:
            with open(full_file_path, self.mode, encoding='utf-8') as file:
                if isinstance(content, list):  # 如果内容是列表
                    file.writelines(content)
                else:  # 如果内容是字符串
                    file.write(content)

        # 如果需要显示内容
        if self.show_content:
            print("写入的内容：")
            if isinstance(content, list):
                print(''.join(content))
            else:
                print(content)

        if self.save_file:
            # print(f"文件已保存为：{full_file_path}")
            pass
        else:
            print("文件未保存，仅显示内容。")

# 示例用法
if __name__ == "__main__":
    # 指定保存的绝对路径
    save_path = rf"/Excel_Operations_Function"  # 替换为你的实际路径

    # 创建一个实例，指定文件名、保存路径、追加模式、显示内容，并保存文件
    # 使用时间戳
    handler_with_timestamp = TxtFileHandler(file_name="myfile", save_path=save_path, mode='a', show_content=True, save_file=True, use_timestamp=True)

    # 写入内容
    handler_with_timestamp.write_to_txt("这是带时间戳的第一行内容。\n")
    handler_with_timestamp.write_to_txt(["这是带时间戳的第二行内容。\n", "这是带时间戳的第三行内容。\n"])

    # 不使用时间戳
    handler_without_timestamp = TxtFileHandler(file_name="myfile", save_path=save_path, mode='a', show_content=True, save_file=True, use_timestamp=False)

    # 写入内容
    handler_without_timestamp.write_to_txt("这是不带时间戳的第一行内容。\n")
    handler_without_timestamp.write_to_txt(["这是不带时间戳的第二行内容。\n", "这是不带时间戳的第三行内容。\n"])


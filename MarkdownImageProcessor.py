import re
import requests
import os

class MarkdownImageProcessor:
    def __init__(self, upload_url, markdown_dir, obs2md=False, localupload=False):
        self.upload_url = upload_url
        self.markdown_dir = markdown_dir
        self.obs2md = obs2md
        self.localupload = localupload
        
    def read_file(self, file_path):
        """读取文件内容"""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def write_file(self, file_path, content):
        """写入内容到文件"""
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

    def extract_image_paths(self, content):
        """提取Markdown文件中的图片路径"""
        return re.findall(r'!\[.*?\]\((.*?)\)', content)

    def replace_image_links(self, md_file_path):
        """替换Markdown文件中的![[example.png]]为![md_filename](example.png)格式"""
        md_filename = os.path.splitext(os.path.basename(md_file_path))[0]
        content = self.read_file(md_file_path)
        new_content = re.sub(r'!\[\[(.+?)\]\]', rf'![{md_filename}](\1)', content)
        self.write_file(md_file_path, new_content)

    def process_directory(self):
        """遍历目录，处理所有Markdown文件"""
        all_image_paths = []
        for root, _, files in os.walk(self.markdown_dir):
            for file in files:
                if file.endswith('.md'):
                    md_file_path = os.path.join(root, file)
                    if self.obs2md:
                        self.replace_image_links(md_file_path)  # 先替换![[example.png]]格式
                    content = self.read_file(md_file_path)
                    image_paths = self.extract_image_paths(content)
                    if self.localupload:
                        full_image_paths = [os.path.abspath(os.path.join(os.path.dirname(md_file_path), path)) for path in image_paths]
                    else:
                        full_image_paths = image_paths  # 网络链接直接使用
                    all_image_paths.extend(full_image_paths)
        return all_image_paths

    def download_image(self, image_url):
        """下载网络图片并保存到临时文件"""
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            temp_filename = os.path.join('/tmp', os.path.basename(image_url))
            with open(temp_filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            return temp_filename
        except requests.RequestException as e:
            print(f"下载失败: {e}")
            return None

    def upload_image(self, image_path):
        """上传图片并返回新的链接"""
        try:
            with open(image_path, 'rb') as file:
                response = requests.post(self.upload_url, files={'file': file})
                response.raise_for_status()
                response_data = response.json()
                return response_data.get('result', [None])[0]
        except requests.RequestException as e:
            print(f"上传失败: {e}")
            return None

    def replace_link(self, match, convert_dict):
        """替换Markdown文件中的图片链接"""
        description = match.group(1)
        link = match.group(2)
        new_link = convert_dict.get(link)
        return f'![{description}]({new_link})' if new_link else match.group(0)

    def update_markdown_files(self, convert_dict):
        """更新Markdown文件中的图片链接"""
        pattern = r'!\[(.*?)\]\((.*?)\)'
        for root, _, files in os.walk(self.markdown_dir):
            for file in files:
                if file.endswith('.md'):
                    md_file_path = os.path.join(root, file)
                    content = self.read_file(md_file_path)
                    updated_content = re.sub(pattern, lambda m: self.replace_link(m, convert_dict), content)
                    self.write_file(md_file_path, updated_content)

    def main(self):
        image_paths = self.process_directory()
        convert_dict = {}
        
        # 上传图片并生成转换字典
        for path in image_paths:
            if self.localupload:
                if os.path.exists(path):
                    new_path = self.upload_image(path)
                    if new_path:
                        convert_dict[os.path.basename(path)] = new_path
                        print(f"图片上传成功: {path}")
                else:
                    print(f"文件不存在: {path}")
            else:
                local_path = self.download_image(path)
                if local_path:
                    new_path = self.upload_image(local_path)
                    if new_path:
                        convert_dict[os.path.basename(path)] = new_path
                        print(f"图片上传成功: {path}")
                    os.remove(local_path)  # 删除临时文件
                else:
                    print(f"图片下载失败: {path}")

        print("转换字典:", convert_dict)
        
        # 更新Markdown文件中的图片链接
        self.update_markdown_files(convert_dict)

if __name__ == '__main__':
    processor = MarkdownImageProcessor(
        upload_url='http://127.0.0.1:36677/upload',
        markdown_dir='./',
        obs2md=True,
        localupload=False
    )
    processor.main()

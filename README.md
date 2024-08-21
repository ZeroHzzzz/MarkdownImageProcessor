# Markdown Image Processor

`MarkdownImageProcessor` 用于处理 Markdown 文件中的图片链接。该工具支持将本地或网络图片上传到指定的服务器，并更新 Markdown 文件中的图片链接为上传后的新链接。

## 功能

-   **读取和写入文件**: 处理 Markdown 文件的读取和写入操作。
-   **提取图片路径**: 从 Markdown 文件中提取图片链接。
-   **替换图片链接**: 将 Markdown 文件中的 `![[example.png]]` 格式(obsidian 格式)的图片链接替换为 `![md_filename](example.png)` 格式。
-   **上传图片**: 将本地或下载的图片上传到服务器，并获取新链接。
-   **更新 Markdown 文件**: 根据图片上传后的新链接更新 Markdown 文件中的图片链接。

## 使用方法

### 配置参数:

创建 MarkdownImageProcessor 实例时，传入以下参数：

-   upload_url：图片上传的服务器 URL。
-   markdown_dir：包含 Markdown 文件的目录路径。
-   obs2md（可选）：布尔值，是否将 ![[example.png]] 格式替换为 ![md_filename](example.png) 格式。默认为 False。
    -   localupload（可选）：布尔值，是否从本地上传图片。如果为 False，将从网络链接下载图片并上传。默认为 False。

### 运行脚本:

创建 MarkdownImageProcessor 实例并调用 main 方法以处理目录中的 Markdown 文件。

```python
# example
processor = MarkdownImageProcessor(
    upload_url='http://127.0.0.1:36677/upload',
    markdown_dir='./markdown_files',
    obs2md=True,
    localupload=False
)
processor.main()
```

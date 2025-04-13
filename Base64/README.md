# Base64编码/解码 Alfred 插件

## 功能

- 一键进行Base64编码和解码
- 支持多种Base64编码格式：
  - 标准Base64编码
  - URL安全的Base64编码（替换+为-，/为_）
- 自动检测并提供解码选项（当输入已编码文本时）

## 使用方法

1. 在 Alfred 中输入 `base64` 后跟要编码的文本
   例如：`base64 Hello World!`
2. Alfred 将显示多种编码格式的结果
3. 选择您需要的格式，按回车键复制到剪贴板
4. 如果输入的是已编码的文本，将自动显示解码选项

## 示例

### 编码示例
输入：`base64 Hello World!`
输出：
- 标准Base64编码：`SGVsbG8gV29ybGQh`
- URL安全Base64编码：`SGVsbG8gV29ybGQh`

### 解码示例
输入：`base64 SGVsbG8gV29ybGQh`
输出：
- Base64解码：`Hello World!`

## 安装

1. 下载此插件
2. 双击下载的文件以安装到Alfred
3. 在Alfred中使用关键词 `base64` 开始使用

# UUID 生成器 Alfred 插件

这是一个简单而强大的 Alfred 插件，用于生成各种格式的 UUID（通用唯一标识符）。

## 功能

- 一键生成 UUID v4（随机 UUID）
- 支持多种 UUID 格式：
  - 标准格式（8-4-4-4-12）
  - 无连字符格式（32个字符）
  - 大写格式
  - 大写无连字符格式
  - URN 格式

## 使用方法

1. 在 Alfred 中输入 `uuid`
2. Alfred 将显示一个新生成的 UUID 的多种格式
3. 选择您需要的格式，按回车键复制到剪贴板

## 安装

1. 下载此插件
2. 双击 `.alfredworkflow` 文件安装到 Alfred
3. 确保您的系统上安装了 Python 3

## 技术细节

- 使用 Python 的 `uuid` 模块生成 UUID v4
- 支持 Alfred 4 及以上版本

## 作者

如有问题或建议，请联系作者。

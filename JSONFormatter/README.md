# JSON格式化工具

这是一个Alfred工作流插件，用于格式化JSON文本。它可以将JSON文本转换为不同的格式，使其更易于阅读和使用。

## 功能特点

- 支持多种格式化选项：
  - 美化格式：带缩进和换行的格式化输出
  - 紧凑格式：移除所有空格和换行的压缩输出
  - 排序格式：按键名排序的格式化输出

- 实时格式化：输入JSON文本后立即显示不同的格式化选项
- 快速复制：点击选项即可将格式化后的JSON复制到剪贴板
- 错误提示：当输入的JSON格式无效时，会显示友好的错误提示

## 使用方法

1. 在Alfred中输入要格式化的JSON文本
2. 插件会自动识别并格式化JSON
3. 选择需要的格式化选项
4. 点击选项将格式化后的JSON复制到剪贴板

## 示例

输入以下JSON文本：
```json
{"name":"Alfred","version":"1.0","features":["format","beautify","sort"]}
```

插件会提供以下格式化选项：

1. 美化格式：
```json
{
    "name": "Alfred",
    "version": "1.0",
    "features": [
        "format",
        "beautify",
        "sort"
    ]
}
```

2. 紧凑格式：
```json
{"name":"Alfred","version":"1.0","features":["format","beautify","sort"]}
```

3. 排序格式：
```json
{
    "features": [
        "format",
        "beautify",
        "sort"
    ],
    "name": "Alfred",
    "version": "1.0"
}
```

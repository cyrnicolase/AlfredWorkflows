# ChatGPT Alfred 工作流

这是一个Alfred工作流插件，可以让你直接在Alfred中与ChatGPT进行对话。

## 功能特点

- 使用关键字 `gpt` 快速启动对话
- 支持API Key配置
- 自动保存最近100条对话历史
- 支持复制回答到剪贴板
- 优雅的错误处理和提示

## 使用方法

1. 首先在 `config.json` 文件中设置你的OpenAI API Key
2. 在Alfred中输入 `gpt` 后跟随你的问题
3. 等待ChatGPT的回答
4. 按Enter键可以复制回答到剪贴板

## 配置说明

在 `config.json` 文件中可以配置以下参数：

```json
{
    "api_key": "你的OpenAI API Key",
    "model": "gpt-3.5-turbo"
}
```

- `api_key`: 你的OpenAI API密钥
- `model`: 使用的GPT模型，默认为gpt-3.5-turbo

## 注意事项

- 请确保你有可用的OpenAI API Key
- 保持网络连接通畅
- API调用可能会产生费用，请注意使用频率

## 历史记录

对话历史会自动保存在 `history.json` 文件中，最多保存最近的100条对话记录。每条记录包含：

- 对话时间
- 提问内容
- ChatGPT的回答

# AIGC File

## Abstract

File renaming, path acquisition, folder creation, file indexing and other operations


## Installation

```bash 
pip install aigcfile
```

## vscode config

```json
{
    // 粘贴时，规范代码，自动帮你满足autopep8代码规范，需要vscode安装有autopep8插件
    "editor.formatOnPaste": true,
    "editor.multiCursorModifier": "ctrlCmd",
    // python 解释器的路径
    "python.defaultInterpreterPath": "/home/william/.conda/envs/aigcav/bin/python",
    // 字数提示分割线，有多少个数，就有多少条分割线
    "editor.rulers": [
        80,
        120
    ],
    "python.languageServer": "Jedi",
    "python.formatting.provider": "none"
}

```

## build

```bash
python3 -m pip install --upgrade build
python3 -m pip install --upgrade twine
python3 -m build
python3 -m twine upload dist/*
```

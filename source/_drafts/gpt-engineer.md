- 目前的测试结果是写脚本还行，大的工程还是不行，总是出错，出错就停止了，写脚本的话我直接用chatgpt不香吗

## 安装配置

- 注意目前新版本仅支持Python 3.10 - 3.12

```shell
pip install gpt-engineer
```

## 项目结构

```shell
.
├── proj1
│   └── prompt
└── requirements.txt	# gpt-engineer
└── .env # 将OPENAI_API_KEY放在这里即可
```

prompt举例:
```shell
A nodejs script that can listen transform firebase realtime database and then transform it to aws cloudwatch. The firebase realtime database documentation name is logs, it's a array. The cloudwatch log group name is AAA, stream is BBB.
```

## 生成代码

```shell
gpt-engineer proj1 # 默认会使用gpt-4
gpt-engineer proj1 gpt-3.5-turbo # 指定model
```


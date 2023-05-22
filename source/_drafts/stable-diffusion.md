## Troubleshooting

- **Something went wrong Expecting value: line 1 column 1 (char 0)**: [两种解决办法](https://github.com/AUTOMATIC1111/stable-diffusion-webui/issues/9174)
  - 关闭代理
  - 添加`COMMANDLINE_ARGS`参数`--no-gradio-queue`
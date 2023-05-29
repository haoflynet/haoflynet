## 主要功能

### img2img图生图

- 常用参数:
  - Sampling Method: 去噪算法，平衡生成图的速度和质量，常用DPM++ 2M Karras
  - Sampling Steps: 去噪过程的采样步数，越多越好，但也需要更长的时间，常用20-28之间
  - Batch Count: 批次数量，最好用Batch size吧
  - Batch size: 每一批次的数量
  - CFG(Classifier Free Guidance) scale: 提示词相关性，1(基本忽略你的提示)、3(更有创意)、7(比较平衡)、15(更加遵守提示)、30(严格按照提示)
  - Denoising strength: 降噪强度(重绘幅度)，新生成的图片与原图的相似程度，数值越小，采样越少，相似度越高，生成越快
  - Seed: 种子值
  - Script: 自定义脚本

#### SKetch绘图

- 可以给现有的图加东西，然后输入提示词完善
- 也可以完全手绘一张图，让它给你生成一个完整的丰富的图像
- 如果要指定颜色，需要使用笔刷: `./webui.sh --disable-safe-unpickle --gradio-img2img-tool color-sketch`

#### Inpaint局部绘制

- 例如换脸、换衣服、换背景等
- 参数
  - Mask blur: 笔刷毛边柔和程度
  - Mask mode: 让AI填充涂黑区域还是填充未涂黑区域
  - Masked content: 填充的内容的类型，Fill(参考涂黑附近的颜色填满区域)、Original(参考原图内容)、Latent noise(使用潜在空间填满)、latent nothing(使用潜在空间填满但不加入噪声)
  - Inpaint area: 填满增长照片还是只填满涂黑的区域
  - Only masked padding: 像素内距

#### Inpaint sketch局部绘制涂鸦蒙版

#### Inpaint upload局部绘制上传蒙版

## 模型网站

### [Hugging Face](https://huggingface.co/)

### [Civitai](https://civitai.com/)

## Troubleshooting

- **Something went wrong Expecting value: line 1 column 1 (char 0)**: [两种解决办法](https://github.com/AUTOMATIC1111/stable-diffusion-webui/issues/9174)
  - 关闭代理
  - 添加`COMMANDLINE_ARGS`参数`--no-gradio-queue`
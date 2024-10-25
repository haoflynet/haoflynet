## 安装配置


- 除了英伟达和Mac以外，它好像不能在其他显卡上面运行，其他平台默认只能用CPU

```shell
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
cd stable-diffusion-webui
./webui.sh	# 然后访问7860端口即可
```


## 主要功能

### img2img图生图

- 常用参数:
  - Sampling Method: 采样器/采样方法，平衡生成图的速度和质量。Euler最简单最快，Euler a步数超过30效果不会更好，DDIM收敛快效率低，需要更多step才能获得好的结果适合重绘，常用DPM++ 2M Karras、UniPC(速度较快效果较好，对平面、卡通表现较好)
  - Sampling Steps: 采样步数，越多越好，但也需要更长的时间，常用20-30之间
  - Batch Count: 批次数量，最好用Batch size吧
  - Batch size: 每一批次的数量，增加这个值可以提高速度，但是对显存消耗更大，如果显存没有16G，最好保持1
  - CFG(Classifier Free Guidance) scale: 提示词相关性，1(基本忽略你的提示)、3(更有创意)、7(比较平衡)、15(更加遵守提示)、30(严格按照提示)，一般7-11
  - Denoising strength: 降噪强度(重绘幅度)，新生成的图片与原图的相似程度，数值越小，采样越少，相似度越高，生成越快
  - Seed: 种子值
  - Script: 自定义脚本
  - Width / Height：尺寸太宽时，可能会出现多个主体
  - Highres. fix: 高清修复，有时候在高分辨率下会生成混乱的图像，需要使用这个选项

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

## 模型

- 不同的模型需要放入不同的目录，但一般是放在`stable-diffusion-webui/models/Stable-diffusion`目录下

### 模型网站

#### [Hugging Face](https://huggingface.co/)

#### [Civitai](https://civitai.com/)

### 常用模型

#### [Dark Sushi Mix 大颗寿司Mix](https://civitai.com/models/24779/dark-sushi-mix-mix)

- 不错的动漫风格的模型

- 生成示例:

  - 参数:
    - Sampling steps: 60
    - ControNet:
      - Single Image, Enable, Piexel Perfect, Allow Preview
      - Control Type: Canny

  - Prompt:

  ```shell
  (masterpicece:1,2), best quality, masterpiece, highres, original, extremely detailed wallpaper, perfect lighting, (extremely detailed CG:1.2), drawing, paintbrush,
  
  Negative Prompt:
  NSFW, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, age spot, (ugly:1.331), (duplicate:1.331), (morbid:1.21), (mutilated:1.21), (tranny:1.331), mutated hands, (pooorly drawn hands:1.5), blurry, (bad anatomy:1.21), (bad proportions:1.331), extra limbs, (disfigured:1.331), (missing arms:1.331), (extra legs:1.331), (fused fingers:1.61051), (too many fingers:1.61051), (unclear eyes:1.331), lowers, bad hands, missing fingers, extra digit, bad hands, missing fingers, (((extra arms and legs)))
  ```


![](https://haofly.net/uploads/stable-diffusion_01.png)

![](https://haofly.net/uploads/stable-diffusion_02.png)

#### [cartoonish](https://civitai.com/models/18569/cartoonish)

- 卡通人物模型

## 插件/工具

### [Stable DIffusion Prompts](https://stable-diffusion-prompts.com/)

- 提示词参考网站，网站收录了很多精美的图片并提供对应的提示词

### [CLIP Interrogator](https://huggingface.co/spaces/pharmapsychotic/CLIP-Interrogator)

- 提取AI图片的Prompt
- 在线工具，需要排队，但是可能几分钟就好了，生成的prompt质量比较高

### ControlNet

```shell
git clone https://github.com/Mikubill/sd-webui-controlnet.git extensions/sd-webui-controlnet # 安装后重启
```

- 参数
  - Low VRAM: 此选项可以降低VRAM使用量，建议8G以下的显存开启此选项

### [Stable Diffusion Prompt Reader](https://github.com/receyuki/stable-diffusion-prompt-reader/blob/master/README.zh-Hans.md#stable-diffusion-prompt-reader)

- 提取AI图片的Prompt

### [Tagger](https://github.com/picobyte/stable-diffusion-webui-wd14-tagger)

- 提取照片的Prompt，可以直接发送到img2img,txt2img等

## Troubleshooting

- **Something went wrong Expecting value: line 1 column 1 (char 0)**: [两种解决办法](https://github.com/AUTOMATIC1111/stable-diffusion-webui/issues/9174)
  - 关闭代理
  - 添加`COMMANDLINE_ARGS`参数`--no-gradio-queue`

- **RuntimeError: "LayerNormKernelImpl" not implemented for 'Half'**: 运行时添加参数`--no-half`

- **When localhost is not accessible, a shareable link must be created. Please set share=True.**: 关闭代理即可

- **safetensors_rust.SafetensorError: Error while deserializing header: MetadataIncompleteBuffer**: 可能是safetensors模型文件没有下载完整或者已经损坏，尝试重新下载

## 教程

[图生图](https://mp.weixin.qq.com/s/NR1lvG4zzffcIZFjCDo4gA)
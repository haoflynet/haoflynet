## Prompt

### 提示词推荐网站

- [AI Short](https://www.aishort.top/): 比如将文本改写成类似小红书的 Emoji 风格、辅助编程CAN(让AI自动提问引导代码编写)、文章续写、辅助微信小程序开发、提示词修改器、旅游路线规划、海量资料输入、取名字、全栈程序员项目架构、前端开发项目架构、架构师IT、周边旅游推荐、育儿帮手、软件测试清单

## API

- 每个模型都有对应的token数量限制，可以通过[Tokenizer](https://platform.openai.com/tokenizer)来计算
- OpenAI生成的图片默认只有1小时的时间，过期会无法访问

### 常用模型

#### GPT

- 问答功能

#### DALL E

- 根据文字生成图片模型

#### Whisper

- 通过声音转换文本

#### Moderation

- 文本内容识别时候暴力等有害内容

#### Embeddings

- 计算文本关联性，比如搜索、聚类、推荐算法、异常检测、多样性检测、分类等场景
- text-embedding-ada-002

### 常用API

- `/v1/completions`和`/v1/chat/completions`的区别是前者是传入一个字符串作为prompt参数(不过可以追加字符串做上下文），后者是直接传入数组作上下文

### API优化

- API通常返回比较慢，可以尝试流式返回，这样就不用等待所有结果生成完后再返回，只需要在接口中添加参数`stream: true`即可，很多接口都支持
- 不同的模型返回的速度会不一样，通常越高级越慢，但是低级的，比如GTP-3系列的结果基本没法看，取中间值大概也就是`gpt-3.5-turbo`
- 降低temperature的值，这个参数用于控制生成文本的多样性和创造性，越高，则生成的文本就越随机、多样化，约有创造力，相反则越接近训练数据的平均值，更加合理可靠。设置可以设置为0，没准会得到相同的结果
- 减少返回长度，在提问时限制返回长度没准能很大程度减少时间





他居然还能生成随机的图片AI所需要的Promote关键词，例如:

```
请根据下面格式生成3组随机命令，请用英文回答。
一个[16-30] 岁的动漫人物，[随机身材]，穿着[随机]样式的服装，[随机的表情]，黑色头发，[随机场景]，[随机视角]，[随机插画风格] ，[随机照明方式]，高质量作品，全身照，超清细节
```


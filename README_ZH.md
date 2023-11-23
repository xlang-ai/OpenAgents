# [OpenAgents: 现实世界的开放平台的语言智能体](https://arxiv.org/abs/2310.10634)

 <a href="https://arxiv.org/abs/2310.10634" target="_blank">
    <img alt="OpenAgents Paper" src="https://img.shields.io/badge/📑-OpenAgents_论文-blue" />
 </a>
 <a href="https://chat.xlang.ai" target="_blank">
    <img alt="现场演示" src="https://img.shields.io/badge/🥑-现场演示-blue" />
 </a>
 <a href="https://xlang.ai" target="_blank">
    <img alt="XLangNLP实验室" src="https://img.shields.io/badge/🧪-XLANG_NLP_实验室-blue" />
 </a>
 <a href="https://docs.xlang.ai" target="_blank">
    <img alt="用户手册" src="https://img.shields.io/badge/📖-用户手册-blue" />
 </a>
 <a href="https://opensource.org/license/apache-2-0" target="_blank">
      <img alt="许可证: apache-2-0" src="https://img.shields.io/github/license/saltstack/salt" />
   </a>
   <a href="https://github.com/xlang-ai/OpenAgents" target="_blank">
      <img alt="GitHub 星星数" src="https://img.shields.io/github/stars/xlang-ai/OpenAgents?style=social" />
   </a>
   <a href="https://github.com/xlang-ai/OpenAgents/issues" target="_blank">
      <img alt="开放问题" src="https://img.shields.io/github/issues-raw/xlang-ai/OpenAgents" />
   </a>
   <a href="https://twitter.com/XLangNLP" target="_blank">
      <img alt="推特关注" src="https://img.shields.io/twitter/follow/XLANG NLP Lab" />
   </a>
   <a href="https://join.slack.com/t/xlanggroup/shared_invite/zt-20zb8hxas-eKSGJrbzHiPmrADCDX3_rQ" target="_blank">
      <img alt="加入Slack" src="https://img.shields.io/badge/Slack-join-blueviolet?logo=slack&amp" />
   </a>
   <a href="https://discord.gg/4Gnw7eTEZR" target="_blank">
      <img alt="Discord" src="https://dcbadge.vercel.app/api/server/4Gnw7eTEZR?compact=true&style=flat" />
   </a>
<div align="center">
    <img src="pics/openagents_overview.png"/>
</div>

<p align="center">
    <a href="README.md">English</a> •
    <a>中文</a> •
    <a href="README_JA.md">日本語</a> •
    <a href="README_KO.md">한국어</a>
</p>

当前的语言代理框架旨在促进构建概念证明语言智能体（Language Agent）的搭建，但是同时忽视了非专家用户的使用，对应用级设计也关注较少。
我们创建了OpenAgents，一个用于在日常生活中使用和托管语言智能体的开放平台。

我们现在在OpenAgents中实现了三个智能体，并在[demo](https://chat.xlang.ai)上免费托管他们！
1. 数据智能体-用于用Python/SQL和数据工具进行数据分析；
2. 插件智能体-具有200多个日常工具，并且可供拓展；
3. 网络智能体-用于自动上网。

OpenAgents可以分析数据，调用插件，像ChatGPT Plus一样控制浏览器，但完全开源，以：
1. 易于部署
2. 全栈代码
3. 聊天Web UI
4. 代理方法
5. …
   
OpenAgents使普通用户通过为快速响应和常见失败进行优化的web UI与智能体功能进行交互，同时为开发人员和研究人员在本地设置上提供无缝部署体验，为制作创新的语言代理和实现现实世界评估提供了基础。
我们解释了挑战和有前景的机会，希望能为现实世界语言代理的未来研究和开发设置基础。

## 🔫 遇到问题
如果您在我们的[在线演示](https://chat.xlang.ai)或本地部署中遇到任何问题，请加入我们的Discord寻求帮助。或者，如果您在功能或代码上有困难，可以创建一个[问题](https://github.com/xlang-ai/OpenAgents/issues) 。

## 🔥 新闻

- **[2023年, 10月26日]** 我们在线demo现在用户数量达到3000！🚀 衷心感谢所有用户和贡献者！🙏 如遇到任何因为用户过多造成的服务器异常，请耐心等待，我们将会在dsicord和issues中尽快回复，感谢！
- **[2023年，10月18日]** 尝试我们的 [狐猴大模型](https://github.com/OpenLemur/Lemur) ，这是用于语言代理的SOTA和开源基础模型，可以在15个代理任务上匹配ChatGPT！
- **[2023年，10月17日]** [在这里](https://arxiv.org/abs/2310.10634) 查看OpenAgents论文！
- **[2023年，10月13日]** 我们已经释放了所有三个代理、服务器后端和前端的OpenAgents平台代码！随时可以设置本地主机，来试试OpenAgents吧！
- **[2023年，8月17日]** 我们的平台已经正式达到500用户！🚀
- **[2023年，8月8日]** 我们已经发布了OpenAgents演示，包括数据、插件和Web代理！请您查看教程和使用案例！


## 🥑 OpenAgents

我们用基于聊天的web UI构建了三个真实世界的智能体(查看[OpenAgents的demo展示](https://chat.xlang.ai))。以下是我们的OpenAgents框架的简要概览。您可以在我们的[文档](https://docs.xlang.ai)中找到更多关于概念和设计的详细信息。

### 数据智能体（Data Agent）

[数据智能体](https://github.com/xlang-ai/OpenAgents/tree/main/real_agents/data_agent) 是一款设计用于高效数据操作的全面工具包。它提供以下功能：

- 🔍 **搜索**： 快速定位所需的数据。
- 🛠️ **处理**：简化数据获取和处理。
- 🔄 **操作**：按照特定要求修改数据。
- 📊 **可视化**：以清晰且有见解的方式表示数据。

数据智能体高效地写入和执行代码，简化了大范围的数据相关任务。通过各种 [使用案例](https://docs.xlang.ai/use-cases/data-agent) 了解它的潜力。

<div align="center">
    <img src="pics/data_agent.png" width="784"/>
</div>

<details>
  <summary>点击查看更多使用案例的屏幕截图</summary>
<div align="center">
    <img src="pics/data_agent_demo.png" width="784"/>
</div>

</details>

### 插件智能体（Plugins Agent）

[插件智能体](https://github.com/xlang-ai/OpenAgents/tree/main/real_agents/plugins_agent) 无缝地与200多个第三方插件集成，每个插件都是精选的，用于丰富您日常生活的各个方面。有了这些插件，该代理使您能更有效地处理各种任务和活动。

🔌 **插件例子包括**：

- 🛍️ **购物**：Klarna购物
- ☁️ **天气**：XWeather
- 🔬 **科学探索**：Wolfram Alpha

#### 组合插件使用

发挥协同作用的力量！插件代理支持同时使用多个插件。计划旅行？无缝地将Klook、货币转换器和WeatherViz的功能整合。

#### 自动插件选择

我们的**自动插件选择**特性简化了您的选择。让代理直观地搜索并建议最适合您需求的插件。

深入更多 [使用案例](https://docs.xlang.ai/use-cases/plugins-agent) 查看插件智能体的能怎么做。

<div align="center">
  <img src="pics/plugins_agent.png" width="784"/>
</div>

<details>
  <summary>点击查看更多使用案例的屏幕截图</summary>
<div align="center">
    <img src="pics/plugins_agent_demo.png" width="784"/>
</div>

</details>

### 上网智能体（Web Agent）

[上网智能体](https://github.com/xlang-ai/OpenAgents/tree/main/real_agents/web_agent)利用Chrome扩展程序自动浏览和探索网站。这种代理使网络浏览体验更加流畅，使查找相关信息、访问所需资源等变得更加容易。

**上网智能体可以做什么的例子**：

- 📍 **Google地图导航**：规划旅程？只需向上网智能体传达您的出发点和目的地。它将为您导航Google地图并提供最佳路线。
- 🐦 **Twitter发帖**：与上网智能体参与对话，并希望在Twitter上分享一些内容？提及内容，上网智能体将毫不费力地处理您的推文。
- 📝 **Google表单助手**：需要报名参加活动或活动？分享Google表单链接和所需的详细信息。上网智能体将为您填充表单。

在这些[使用案例](https://docs.xlang.ai/use-cases/web-agent)中看到上网智能体的全部潜力。

<div align="center">
  <img src="pics/web_agent.png" width="784"/>
</div>

<details>
  <summary>点击查看更多使用案例的屏幕截图</summary>
<div align="center">
    <img src="pics/web_agent_demo.png" width="784"/>
</div>

</details>

## 💻 本地部署

我们已经发布了OpenAgents平台代码。随时在您的本地主机上进行部署！

以下是OpenAgents的简要系统设计：
<div align="center">
    <img src="pics/system_design.png"/>
</div>

### 源码部署
请查看下面的文件和README文件来设置和启动localhost：

1. [**Backend**](backend/README.md): 我们的三个代理的 Flask 后端。
2. [**Frontend**](frontend/README.md): 前端 UI 和 WeBot Chrome 扩展程序。

P.S.：我们为了提升代码的可读性，对一些参数进行了重命名。如果你在2023年10月26日之前已经拉取了代码，这里提醒你，如果你想拉取最新的代码，由于部分key name的不同，之前的本地聊天记录将会丢失。

### Docker部署
请按照以下步骤使用docker-compose来部署OpenAgents平台。

注意： docker仍在开发中，因此可能会有一些功能无法正常工作，响应也可能较慢。如果您有任何问题，请随时提出issue。如果您需要一个更稳定的版本，我们目前建议您从源代码部署。

1. 如果您想要使用kaggle的数据集，您必须修改Dockerfile中的信息为您的正确信息。
```
ENV KAGGLE_USER="" \
    KAGGLE_KEY="" 
```
2. 如果您不是在本地运行，您需要修改frontend/Dockerfile中的后端服务可访问的IP地址
```
ENV NEXT_PUBLIC_BACKEND_ENDPOINT http://x.x.x.x:8000
```
3. 在项目根目录运行docker compose build命令。
4. 如果您使用openai非官方服务，如FastChat，您需要在docker-compose.yml中修改OPENAI_API_BASE；否则您只需在docker-compose.yml中放置您的OPENAI_API_KEY。
5. 完成以上步骤后，您可以运行docker compose up -d以启动所有服务。

**注意**：
1. 如果你想要使用GPU，你需要先安装[Nvidia Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html),然后去掉[docker-compose.yml](docker-compose.yml#L56-L62)56-62行的注释。
2. 使用Auto plugin 将会从huggingface下载权重文件，在有些地区可能会出现连接超时，请自行解决网络问题。

## 📜 拓展OpenAgents的教程
### 代码结构
在我们深入探讨如何扩展OpenAgents之前，首先让我们简要了解一下代码结构以便更好地理解。
OpenAgents的代码结构如下所示：
```bash
├── backend  # backend code
│   ├── README.md  # backend README for setup
│   ├── api  # RESTful APIs, to be called by the frontend
│   ├── app.py  # main flask app
│   ├── display_streaming.py  # rendering the streaming response
│   ├── kernel_publisher.py  # queue for code execution
│   ├── main.py  # main entry for the backend
│   ├── memory.py  # memory(storage) for the backend
│   ├── schemas.py  # constant definitions
│   ├── setup_script.sh  # one-click setup script for the backend
│   ├── static  # static files, e.g., cache and figs
│   └── utils  # utilities
├── frontend  # frontend code
│   ├── README.md  # frontend README for setup
│   ├── components  # React components
│   ├── hooks  # custom React hooks
│   ├── icons  # icon assets
│   ├── next-env.d.ts  # TypeScript declarations for Next.js environment variables
│   ├── next-i18next.config.js  # configuration settings for internationalization
│   ├── next.config.js  # configuration settings for Next.js
│   ├── package-lock.json  # generated by npm that describes the exact dependency tree
│   ├── package.json  # manifest file that describes the dependencies
│   ├── pages  # Next.js pages
│   ├── postcss.config.js  # configuration settings for PostCSS
│   ├── prettier.config.js  # configuration settings for Prettier
│   ├── public  # static assets
│   ├── styles  # global styles
│   ├── tailwind.config.js  # configuration settings for Tailwind CSS
│   ├── tsconfig.json  # configuration settings for TypeScript
│   ├── types  # type declarations
│   ├── utils  # utilities or helper functions
│   ├── vitest.config.ts  # configuration settings for ViTest
│   └── webot_extension.zip  # Chrome extension for Web Agent
└── real_agents  # language agents
    ├── adapters  # shared components for the three agents to adapt to the backend
    ├── data_agent  # data agent implementation
    ├── plugins_agent  # plugins agent implementation
    └── web_agent  # web agent implementation
```
如所示，`backend/` 和 `frontend/` 是自包含的，并且可以直接部署（参见[这里](#localhost-deployment)）。
这并不意味着它们不能被修改。
相反，您可以按照传统的*客户端-服务器*架构来根据您的需求扩展后端和前端。
对于`real_agents/`，我们设计它为“一个智能体，一个文件夹”的形式，以便于扩展新的代理。
值得注意的是，我们将其命名为“真实代理”，因为这里不仅包括了概念性的语言代理部分，还填补了语言代理和后端之间的空白。
例如，`adapters/` 包含了像流解析（streaming parsing）、数据模型（DataModel）、内存（memory）、回调（callbacks）等共享的适配器组件。
我们推荐感兴趣的读者参考我们的 [论文](https://arxiv.org/abs/2310.10634) 了解概念和实现设计。
我们也感谢 [LangChain](https://github.com/langchain-ai/langchain) ，因为我们基于他们的代码构建真实代理。

### 扩展一个新的智能体
如果您想构建一个新的智能体，超出我们提供的三个智能体，您可以按照以下步骤操作：
- 参考 `real_agents/` 文件夹，查看之前的智能体是如何实现的，并为您的代理创建一个新文件夹。
- 在新文件夹中实现智能体逻辑。在需要时使用 `adapters/` 文件夹下的组件。
- 在 `backend/api/` 文件夹下添加一个 `chat_<new_agent>.py` 文件，以定义新代理的聊天API，该API将由前端调用。
- 在 `backend/schemas.py` 中注册新的常量（如果需要的话）。
- 在 `frontend/types/agent.ts` 中添加一个新的 `OpenAgentID`，并在 `frontend/utils/app/api.ts` 和 `frontend/utils/app/const.ts` 中添加相应的API。
- 在需要时在 `frontend/components/Chat/Chat.tsx` 和 `frontend/components/Chat/ChatMessage.tsx` 中实现代理的UI。
- 运行本地主机脚本并测试您的新智能体。

请注意，如果有新的数据类型，即超出文本、图片、表格和json，您可能需要在 `backend/display_streaming.py` 中实现其解析逻辑，并添加新的数据模型。

### 扩展一个新的LLM
如果LLM已经托管并可以通过API调用，那么将新的LLM作为智能体主干进行扩展会更简单。
只需在 `backend/api/language_model.py` 中注册您的新模型。您可以参考lemur-chat作为模板。

如果LLM还没有被托管，我们有一个教程，教您如何部署一个新的LLM并将其作为API公开[这里]()（LLM托管待办事项）。

### 扩展一个新的工具
如果您想在插件智能体中扩展一个新工具，可以按照以下步骤操作：
- 参考在 `real_agents/plugins_agent/plugins/` 中已经构建的插件，并为您的工具创建一个新文件夹。
- 在新文件夹中实现工具逻辑。请注意，`ai-plugin.json` 和 `openapi.yaml` 对于工具被识别是必要的（可以由LLM生成，跟随其他工具，而不是手动编写）。而 `paths/` 是用于实际的工具API调用。
- 在 `real_agents/plugins_agent/plugins/plugin_names.py` 中注册新工具的名称。


## 👏 贡献
感谢开源社区的努力，如[LangChain](https://github.com/langchain-ai/langchain)、[ChatBot UI](https://github.com/mckaywrigley/chatbot-ui)、[Taxy.ai 浏览器扩展](https://github.com/TaxyAI/browser-extension) 等。我们能够更方便、更高效地构建我们的界面原型。

我们欢迎各种贡献和建议，共同努力，使本项目更上一层楼！麻烦遵循以下步骤：

- **步骤1：** 如果您想添加任何额外的功能、增强功能或在使用过程中遇到任何问题，请发布一个 [问题](https://github.com/xlang-ai/OpenAgents/issues) 。如果您能遵循 [问题模板](https://github.com/xlang-ai/OpenAgents/blob/main/CONTRIBUTING.md) 我们将不胜感激。问题将在那里被讨论和分配。
- **步骤2：** 无论何时，当一个问题被分配后，您都可以按照 [PR模板](https://github.com/xlang-ai/OpenAgents/blob/main/CONTRIBUTING.md) 创建一个 [拉取请求](https://github.com/xlang-ai/OpenAgents/pulls) 进行贡献。您也可以认领任何公开的问题。共同努力，我们可以使OpenAgents变得更好！
- **步骤3：** 在审查和讨论后，PR将被合并或迭代。感谢您的贡献！

在您开始之前，我们强烈建议您花一点时间检查 [这里](https://github.com/xlang-ai/OpenAgents/blob/main/CONTRIBUTING.md) 再进行贡献。


## 📖 文档

请在[这里](https://docs.xlang.ai)查看完整文档，将随着demo更改和代码发布更新。


## 🧙‍ 谁在参与

### 技术领导

<a href="https://github.com/Impavidity"><img src="https://avatars.githubusercontent.com/u/9245607?v=4"  width="50" /></a>

### 共同领导的贡献者

<a href="https://github.com/BlankCheng"><img src="https://avatars.githubusercontent.com/u/34505296?v=4"  width="50" /></a>
<a href="https://github.com/koalazf99"><img src="https://avatars.githubusercontent.com/u/37338733?v=4"  width="50" /></a>
<a href="https://github.com/Timothyxxx"><img src="https://avatars.githubusercontent.com/u/47296835?v=4"  width="50" /></a>

### 关键贡献者

<a href="https://github.com/taogoddd"><img src="https://avatars.githubusercontent.com/u/98326623?v=4"  width="50" /></a>
<a href="https://github.com/WhiteWolf82"><img src="https://avatars.githubusercontent.com/u/48792453?v=4"  width="50" /></a>
<a href="https://github.com/ztjhz"><img src="https://avatars.githubusercontent.com/u/59118459?v=4"  width="50" /></a>

### 宝贵贡献者

<a href="https://github.com/BillStark001"><img src="https://avatars.githubusercontent.com/u/31788509?v=4"  width="50" /></a>
<a href="https://github.com/SivilTaram"><img src="https://avatars.githubusercontent.com/u/10275209?v=4"  width="50" /></a>
<a href="https://github.com/che330"><img src="https://avatars.githubusercontent.com/u/122778503?v=4"  width="50" /></a>
<a href="https://github.com/leo-liuzy"><img src="https://avatars.githubusercontent.com/u/11146950?v=4"  width="50" /></a>
<a href="https://github.com/ranpox"><img src="https://avatars.githubusercontent.com/u/25601999?v=4"  width="50" /></a>
<a href="https://github.com/hongjin-su"><img src="https://avatars.githubusercontent.com/u/114016954?v=4"  width="50" /></a>
<a href="https://github.com/QIN2DIM"><img src="https://avatars.githubusercontent.com/u/62018067?v=4"  width="50" /></a>
<a href="https://github.com/xJQx"><img src="https://avatars.githubusercontent.com/u/47933193?v=4"  width="50" /></a>
<a href="https://github.com/thomasshin"><img src="https://avatars.githubusercontent.com/u/76890354?v=4"  width="50" /></a>

### 衷心感谢 (除代码之外)

我们衷心感谢 [Ziyi Huang](https://www.joanna-ziyi-huang.com/), [Roxy Rong](https://www.linkedin.com/in/roxyrong/), [Haotian Li](https://haotian-li.com/), [Xingbo Wang](https://andy-xingbowang.com/), [Jansen Wong](https://www.linkedin.com/in/jansenwong/), 和 [Chen Henry Wu](https://chenwu.io/) 对OpenAgents的宝贵贡献。他们的专业知识和洞察力对于完成这个项目至关重要！

### 开放源代码贡献者

感谢所有的贡献者们！

<a href="https://github.com/xlang-ai/OpenAgents/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=xlang-ai/OpenAgents" />
</a>

## 引用
如果你觉得我们的工作帮助到了你，请引用我们：
```
@misc{OpenAgents,
      title={OpenAgents: An Open Platform for Language Agents in the Wild}, 
      author={Tianbao Xie and Fan Zhou and Zhoujun Cheng and Peng Shi and Luoxuan Weng and Yitao Liu and Toh Jing Hua and Junning Zhao and Qian Liu and Che Liu and Leo Z. Liu and Yiheng Xu and Hongjin Su and Dongchan Shin and Caiming Xiong and Tao Yu},
      year={2023},
      eprint={2310.10634},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

## 鸣谢

我们想要感谢Google Research，Amazon AWS和Salesforce Research对于这个开源工作的研究基金！

<div align="center">

<img src="pics/transparent.png" width="20" style="pointer-events: none;">

<a href="https://www.salesforceairesearch.com/">
    <img src="pics/salesforce.webp" alt="Salesforce Research" height = 30/>
</a>

<img src="pics/transparent.png" width="20" style="pointer-events: none;">

<a href="https://research.google/">
    <img src="pics/google_research.svg" alt="Google Research" height = 30/>
</a>

<img src="pics/transparent.png" width="25" style="pointer-events: none;">

<a href="https://www.amazon.science/" style="display: inline-block; margin-bottom: -100px;">
    <img src="pics/amazon.svg" alt="Amazon AWS" height = 20 />
</a>


</div>

## ⭐️ 星星历史

[![【Star History Chart】星星历史图](https://api.star-history.com/svg?repos=xlang-ai/OpenAgents&type=Date)](https://github.com/xlang-ai/OpenAgents/stargazers)

<h3 align="center">
给<b>OpenAgents</b>的一个⭐️，能让它传播更广，受益更多的人。
</h3>
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
    <a>中文</a>
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

## 🔥 新闻

- **[2023年，10月18日]** 尝试我们的 [狐猴大模型](https://github.com/OpenLemur/Lemur) ，这是用于语言代理的SOTA和开源基础模型，可以在15个代理任务上匹配ChatGPT！
- **[2023年，10月17日]** [在这里](https://arxiv.org/abs/2310.10634) 查看OpenAgents论文！
- **[2023年，10月13日]** 我们已经释放了所有三个代理、服务器后端和前端的OpenAgents平台代码！随时可以设置本地主机，来试试OpenAgents吧！
- **[2023年，8月17日]** 我们的平台已经正式达到500用户！🚀
- **[2023年，8月8日]** 我们已经发布了OpenAgents演示，包括数据、插件和Web代理！请您查看教程和使用案例！

## 💻 本地部署

我们已经发布了OpenAgents平台代码。随时在您的本地主机上进行部署！

以下是OpenAgents的简要系统设计：
<div align="center">
    <img src="pics/system_design.png"/>
</div>

请查看下面的文件和README文件来设置和启动localhost：

1. [**backend**](backend/README.md): 我们的三个代理的 Flask 后端。
2. [**frontend**](frontend/README.md): 前端 UI 和 WeBot Chrome 扩展程序。

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

## 📖 文档

请在[这里](https://docs.xlang.ai)查看完整文档，将随着demo更改和代码发布更新。

## 👏 贡献

感谢开源社区的努力，如 [LangChain](https://github.com/langchain-ai/langchain) ，[ChatBot UI](https://github.com/mckaywrigley/chatbot-ui) ，[Taxy.ai浏览器扩展](https://github.com/TaxyAI/browser-extension) 等等。我们能够更方便，更有效率地建立我们的界面原型。

我们欢迎贡献和建议，一起让它变得更好！

- 🐛 如果您在使用过程中遇到任何问题，或者想添加任何其他功能，请发布一个 [issue](https://github.com/xlang-ai/OpenAgents/issues) 。
- 🕹 直接向我们的仓库贡献，创建一个 [Pull Request](https://github.com/xlang-ai/OpenAgents/pulls) 。我们一起可以让OpenAgents变得更好！
- ⭐ 点击星星，在推特上跟随我们，分享您自己的例子，和朋友们分享！

有关如何贡献的详细信息，请看 [这里](https://github.com/xlang-ai/OpenAgents/blob/main/CONTRIBUTING.md) 。

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

我们衷心感谢 [Ziyi Huang](https://www.joanna-ziyi-huang.com/) ，[Roxy Rong](https://www.linkedin.com/in/roxyrong/) ，[Haotian Li](https://haotian-li.com/) ，[Xingbo Wang](https://andy-xingbowang.com/) ，[Jansen Wong](https://www.linkedin.com/in/jansenwong/) 和 [Chen Henry Wu](https://chenwu.io/) 对OpenAgents的宝贵贡献。他们的专业知识和洞察力对于完成这个项目至关重要！

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
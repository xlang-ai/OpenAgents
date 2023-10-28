# [OpenAgents: An Open Platform for Language Agents in the Wild](https://arxiv.org/abs/2310.10634)

 <a href="https://arxiv.org/abs/2310.10634" target="_blank">
    <img alt="OpenAgents Paper" src="https://img.shields.io/badge/📑-OpenAgents_Paper-blue" />
 </a>
 <a href="https://chat.xlang.ai" target="_blank">
    <img alt="Online Demos" src="https://img.shields.io/badge/🥑-Online_Demos-blue" />
 </a>
 <a href="https://xlang.ai" target="_blank">
    <img alt="XLangNLPLab" src="https://img.shields.io/badge/🧪-XLANG_NLP_Lab-blue" />
 </a>
 <a href="https://docs.xlang.ai" target="_blank">
    <img alt="User Manual" src="https://img.shields.io/badge/📖-User_Manual-blue" />
 </a>
 <a href="https://opensource.org/license/apache-2-0" target="_blank">
      <img alt="License: apache-2-0" src="https://img.shields.io/github/license/saltstack/salt" />
   </a>
   <a href="https://github.com/xlang-ai/OpenAgents" target="_blank">
      <img alt="GitHub Stars" src="https://img.shields.io/github/stars/xlang-ai/OpenAgents?style=social" />
   </a>
   <a href="https://github.com/xlang-ai/OpenAgents/issues" target="_blank">
      <img alt="Open Issues" src="https://img.shields.io/github/issues-raw/xlang-ai/OpenAgents" />
   </a>
   <a href="https://twitter.com/XLangNLP" target="_blank">
      <img alt="Twitter Follow" src="https://img.shields.io/twitter/follow/XLANG NLP Lab" />
   </a>
   <a href="https://join.slack.com/t/xlanggroup/shared_invite/zt-20zb8hxas-eKSGJrbzHiPmrADCDX3_rQ" target="_blank">
      <img alt="Join Slack" src="https://img.shields.io/badge/Slack-join-blueviolet?logo=slack&amp" />
   </a>
   <a href="https://discord.gg/4Gnw7eTEZR" target="_blank">
      <img alt="Discord" src="https://dcbadge.vercel.app/api/server/4Gnw7eTEZR?compact=true&style=flat" />
   </a>
<div align="center">
    <img src="pics/openagents_overview.png"/>
</div>

<p align="center">
    <a href="README.md">English</a> •
    <a href="README_ZH.md">中文</a> •
    <a href="README_JA.md">日本語</a> •
    <a>한국어</a>
</p>

현재의 언어 에이전트 프레임워크는 개념 증명용 언어 에이전트 구축을 용이하게 하는 것을 목표로 하지만, 일반 사용자의 에이전트 접근성을 간과하며 응용 수준의 설계에는 관심을 덜 두고 있습니다. 우리는 OpenAgents를 구축했으며, 와일드한 일상생활에서 언어 에이전트를 사용하고 호스팅 하기 위한 오픈 플랫폼입니다.

우리는 OpenAgents에 세 가지 에이전트를 구현했으며, 이들을 무료로 제공합니다!
1. 데이터 에이전트는 Python/SQL과 데이터 도구로 데이터 분석을 수행할 수 있습니다.
2. 플러그인 에이전트는 하루에 200개 이상의 일상 도구를 제공합니다.
3. 웹 에이전트는 자율적인 웹 브라우징을 수행합니다.

OpenAgents는 데이터 분석, 플러그인 호출, 브라우저 제어 등을 ChatGPT Plus와 동일하게 수행할 수 있지만, 아래 이유들을 위해 오픈 코드로 이를 구현하였습니다.
1. 쉬운 배포
2. 풀 스택
3. 챗 웹 유저 인터페이스
4. 에이전트 방법
5. …

OpenAgents는 웹 UI를 통해 일반 사용자가 에이전트 기능과 상호 작용할 수 있도록 하여 신속한 응답과 일반적인 오류에 최적화된 환경을 제공합니다. 동시에 개발자와 연구원들에게는 로컬 환경에서의 원활한 배포 경험을 제공하여 혁신적인 언어 에이전트의 개발과 실제 세계에서의 평가를 용이하게 합니다. 또한 우리는 언어 에이전트의 실제 세계에서의 연구와 개발을 위한 기반을 마련하고자 하는 것에 대한 힘든 점과, 기회에 대해 명확히 설명합니다.

우리는 여러분들의 기여를 환영합니다. 시작하기 전에, 이슈와 PR에 대한 [CONTRIBUTING.md](./CONTRIBUTING.md) 가이드라인을 읽어보시기 바랍니다. 이는 기여 과정이 원활하고 프로젝트의 기준과 일관성을 유지할 수 있도록 도움을 줄 것입니다.

## 🔫 트러블 슈팅
만약 [온라인 데모](https://chat.xlang.ai)나 로컬 배포에 문제가 발생하면, 도움을 받기 위해 Discord에 가입해주세요. 또는 기능이나 코드에 문제가 있을 경우, [이슈](https://github.com/xlang-ai/OpenAgents/issues)를 생성해주세요.

## 🔥 뉴스

- **[2023, 10월 26일]** 사용자 3000명에 도달했습니다! 🚀 모든 사용자분들과 기여해 주신 분들에게 진심으로 감사드립니다! 🙏 서버에서 예상치 못한 높은 트래픽으로 인해 어려움을 겪고 있습니다. 여러분의 인내심에 감사드리며, 가능한 빠른 시일 내에 도움을 드릴 수 있게 준비하겠습니다! 
- **[2023, 10월 18일]** 저희가 만든 [Lemur](https://github.com/OpenLemur/Lemur)를 한번 사용해 보세요. Lemur은 최첨단 (SOTA) 언어 에이전트이며 오픈소스 기반 모델로, ChatGPT와 15가지 에이전트 작업에서 매칭됩니다!
- **[2023, 10월 17일]** OpenAgents 논문을 [여기](https://arxiv.org/abs/2310.10634)에서 확인해보세요!
- **[2023, 10월 13일]** 저희는 OpenAgents 플랫폼의 에이전트 세 개, 서버 백엔드 및 프론트엔드의 모든 코드를 공개했습니다! 자유롭게 로컬 환경에 설치하고 OpenAgents를 사용해보세요!
- **[2023, 8월 17일]** 저희 플랫폼은 공식적으로 500명의 사용자에 도달했습니다! 🚀
- **[2023, 8월 8일]** 저희는 데이터, 플러그인 및 웹 에이전트를 포함한 [OpenAgents 데모](https://chat.xlang.ai)를 공개했습니다! [튜토리얼](https://docs.xlang.ai/category/user-manual)과 [사용 사례들](https://docs.xlang.ai/category/use-cases)을 확인해보세요!

## 🥑 OpenAgents

우리는 실제 세계에서 사용되는 인공지능 에이전트를 구축했습니다. ([OpenAgents 데모](https://chat.xlang.ai)를 확인하세요). 다음은 OpenAgents 플랫폼에 대한 간략한 개요입니다. 자세한 개념 및 디자인에 대한 자세한 내용은 [문서](https://docs.xlang.ai)에서 찾아볼 수 있습니다.

### 데이터 에이전트 (Data Agent)

[데이터 에이전트](https://github.com/xlang-ai/OpenAgents/tree/main/real_agents/data_agent)는 효율적인 데이터 작업을 위해 설계된 포괄적인 도구 모음입니다. 데이터 에이전트는 다음과 같은 기능을 제공합니다:

- 🔍 **검색**: 원하는 데이터를 빠르게 찾을 수 있도록 도와드립니다.
- 🛠️ **처리**: 데이터 획득 및 처리를 간소화할 수 있도록 도와드립니다.
- 🔄 **조작**: 특정 요구 사항에 맞게 데이터를 수정할 수 있습니다.
- 📊 **시각화**: 데이터를 명확하고 통찰력 있게 표현하는 방법을 제공합니다. 

데이터 에이전트는 코드를 작성하고 실행하는 능력을 갖추고 있어 다양한 데이터 중심 작업을 간소화합니다. 다양한 [사용 사례들](https://docs.xlang.ai/use-cases/data-agent)을 통해 데이터 에이전트의 잠재력을 발견해보세요.

<div align="center">
    <img src="pics/data_agent.png" width="784"/>
</div>

<details>
  <summary>더 많은 사용 사례 스크린샷을 보고 싶다면 클릭해주세요.</summary>
<div align="center">
    <img src="pics/data_agent_demo.png" width="784"/>
</div>

</details>

### 플러그인 에이전트 (Plugins Agent)

[플러그인 에이전트](https://github.com/xlang-ai/OpenAgents/tree/main/real_agents/plugins_agent)는 200개가 넘는 제3자 플러그인과 원활하게 통합됩니다. 각 플러그인은 일상생활의 다양한 부분을 풍부하게 만들기 위해 선별되었습니다. 이러한 플러그인들을 활용하여 에이전트는 여러분이 다양한 작업과 활동을 더 효율적으로 처리할 수 있도록 도와줍니다.

🔌 **플러그인 예시**:

- 🛍️ **쇼핑**: Klarna 쇼핑
- ☁️ **날씨**: XWeather
- 🔬 **과학 탐구**: Wolfram Alpha

#### 다수의 플러그인을 동시에 사용하기

시너지의 힘을 발휘하세요! 플러그인 에이전트는 여러 플러그인을 동시에 사용할 수 있게 해줍니다. 여행 계획을 세우고 계시나요? Klook, 통화 변환기, WeatherViz의 기능들을 동시에 사용해 보세요.

#### 자동 플러그인 선택 기능

자동 플러그인 선택 기능으로 선택 과정을 간소화하세요. 에이전트에게 필요에 맞는 최상의 플러그인을 직관적으로 검색하고 제안해 주도록 해보세요.

더 많은 [사용 사례](https://docs.xlang.ai/use-cases/plugins-agent)를 통해 플러그인 에이전트의 작동 방식을 확인해보세요.

<div align="center">
  <img src="pics/plugins_agent.png" width="784"/>
</div>

<details>
  <summary>더 많은 사용 사례 스크린샷을 보고 싶다면 클릭해주세요.</summary>
<div align="center">
    <img src="pics/plugins_agent_demo.png" width="784"/>
</div>

</details>

### 웹 에이전트

[웹 에이전트](https://github.com/xlang-ai/OpenAgents/tree/main/real_agents/web_agent)는 크롬 확장 프로그램의 기능을 활용하여 웹 사이트를 자동으로 탐색하고 탐구하는 기능을 제공합니다. 이 에이전트는 웹 브라우징 경험을 간소화하여 관련 정보를 찾고 원하는 자료에 쉽게 액세스할 수 있도록 도와줍니다.

**웹 에이전트가 수행할 수 있는 작업들**:

- 📍 **Google 지도 네비게이션**: 여행을 계획하고 있나요? 웹 에이전트에게 출발지와 목적지를 알려주세요. 웹 에이전트가 Google 지도를 이용하여 최적의 경로를 제시해줄 것입니다.
- 🐦 **Twitter 게시물**: 웹 에이전트와 대화를 나누며 Twitter에 무언가를 공유하고 싶나요? 내용을 말씀해주시면 웹 에이전트가 손쉽게 트윗을 처리해드릴 것입니다.
- 📝 **Google Form 어시스턴스**: 행사나 활동에 등록해야 할 필요가 있나요? Google Form 링크와 필요한 세부 정보를 공유해주세요. 웹 에이전트가 대신 양식을 작성해드릴 것입니다.

이러한 [사용 사례](https://docs.xlang.ai/use-cases/web-agent)에서 웹 에이전트의 잠재력을 확인해보세요.

<div align="center">
  <img src="pics/web_agent.png" width="784"/>
</div>

<details>
  <summary>더 많은 사용 사례 스크린샷을 보고 싶다면 클릭해주세요.</summary>
<div align="center">
    <img src="pics/web_agent_demo.png" width="784"/>
</div>

</details>


## 💻 로컬 호스트에 배포하기

OpenAgents 플랫폼 코드를 배포했습니다. 자유롭게 로컬 호스트에 배포해보세요!

다음은 OpenAgents의 간략한 시스템 디자인입니다:
<div align="center">
    <img src="pics/system_design.png"/>
</div>

로컬 환경 설정 및 로컬 호스트에 배포하기 위해 다음 폴더 및 README 파일을 확인해 주세요:

1. [**백엔드**](backend/README.md): 플라스크(Flask) 백엔드를 사용하여 세 개의 에이전트를 호스팅합니다.
2. [**프론트엔드**](frontend/README.md): 프론트엔드 UI와 WeBot 크롬 익스텐션    

p.s. : 코드의 가독성을 높이기 위해 일부 인수들의 이름이 변경되었습니다. 2023년 10월 26일 이전에 코드를 가져온 경우, 최신 코드를 가져오려면 키 이름이 다르기 때문에 이전 로컬 채팅 기록이 손실된다는 점을 참고하세요.

## 📜 OpenAgents를 확장하기 위한 튜토리얼
### 코드 구조
OpenAgents를 확장하는 방법에 대해 알아보기 전에, OpenAgents의 코드 구조를 간략히 살펴보겠습니다. 
코드 구조는 아래와 같습니다:
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
위의 코드 구조에서는 `backend/`와 `frontend/`가 독립적이고 직접 배포 가능하다는 것을 보여줍니다. ([여기](#localhost-deployment)를 보세요.) 
이는 수정할 수 없다는 의미가 아닌, 전통적인 *클라이언트-서버* 아키텍처를 따라 원하는대로 백엔드와 프론트엔드를 확장할 수 있다는 것을 의미합니다. 
`real_agents/`는 "하나의 에이전트, 하나의 폴더"로 설계되어 새로운 에이전트를 쉽게 확장할 수 있도록 구성되었습니다. 
"real agents"라는 이름을 사용한 이유는 개념적인 언어 에이전트 부분뿐만 아니라 언어 에이전트와 백엔드 간의 간극을 채우기 위한 내용도 포함되어 있기 때문입니다.
예를 들어, `adapters/` 폴더에는 스트림 파싱, 데이터 모델, 메모리, 콜백 등과 같은 공유 어댑터 컴포넌트가 포함되어 있습니다.
개념과 구현 설계에 대한 자세한 내용은 [논문](https://arxiv.org/abs/2310.10634)을 참조하시기 바랍니다. 
또한, 우리는 실제 에이전트를 구축하는데 코드 기반을 제공해 준 [LangChain](https://github.com/langchain-ai/langchain)에게 감사의 말씀을 전합니다.

### 새로운 에이전트를 확장하기
저희가 제공하는 세 가지의 에이전트 말고도 다른 새로운 에이전트를 구축하고 싶으시다면 아래 스텝을 따라 주세요:
- 새로운 에이전트를 구현하기 위해 이전 에이전트가 구현된 `real_agents/` 폴더를 참조하고, 새로운 폴더를 생성하십시오.
- 새로운 폴더에 있는 에이전트 로직을 구현하십시오. 필요한 경우 `adapters/` 폴더 내의 컴포넌트를 사용하십시오.
- 먼저, 새로운 에이전트를 위한 채팅 API를 정의하기 위해 `backend/api/` 폴더에 `chat_<new_agent>.py` 파일을 추가하세요. 이 파일은 프론트엔드에서 호출될 것입니다.
- 필요한 경우, `backend/schemas.py`파일에 새로운 상수를 등록하세요.
- 프론트엔드에서 새로운 OpenAgentID를 추가하고, 이에 해당하는 API를 `frontend/utils/app/api.ts`와 `frontend/utils/app/const.ts`에 추가해주세요.
- 필요한 경우, `frontend/components/Chat/Chat.tsx`와 `frontend/components/Chat/ChatMessage.tsx`에서 에이전트 UI를 구현해주세요.
- 로컬 호스트 스크립트를 실행하고 새로운 에이전트를 테스트해보세요.

참고: 새로운 데이터 유형(예: 텍스트, 이미지, 테이블 및 JSON 이외의 유형)의 경우, 백엔드의 `display_streaming.py`에서 해당 데이터의 구문 분석 로직을 구현하고 새로운 데이터 모델을 추가해야 할 수도 있습니다.

### 새로운 LLM을 확장하기
LLM(Large Language Model)을 에이전트 백본으로 확장하는 것은, LLM이 이미 호스팅되어 API를 통해 호출될 수 있는 경우 더욱 간단해집니다. `backend/api/language_model.py`에서 새로운 모델을 등록하기만 하면 됩니다. lemur-chat을 참고하면 템플릿으로 사용할 수 있습니다.
LLM이 아직 호스팅되지 않은 경우, LLM을 새로 배포하고 API로 노출하는 방법에 대한 튜토리얼이 [여기]()에 있습니다. (LLM 호스팅은 todo).

### 새로운 도구를 확장하기
플러그인 에이전트에 있는 도구를 확장해보고 싶다면, 아래 스텝을 따르세요:
- `real_agents/plugins_agent/plugins/`에 이미 구축된 플러그인들을 참고하고, 도구에 대한 새로운 폴더를 생성해주세요.
- 새로운 폴더에 도구 로직을 구현해주세요. 도구가 인식되기 위해 `ai-plugin.json`과 `openapi.yaml` 파일이 필수적입니다(이는 수동으로 작성하는 대신 다른 예시를 따라서 LLM이 생성할 수 있습니다). 또한 `paths/` 폴더는 실제 도구 API 호출을 위한 경로입니다.
- `real_agents/plugins_agent/plugin_names.py`에 새로운 도구 이름을 등록해주세요.

## 👏 기여하기

감사하게도 오픈 소스 커뮤니티인 [LangChain](https://github.com/langchain-ai/langchain), [ChatBot UI](https://github.com/mckaywrigley/chatbot-ui), [Taxy.ai browser extension](https://github.com/TaxyAI/browser-extension) 등의 노력 덕분에 저희는 인터페이스 프로토타입을 더 편리하고 효율적으로 구축할 수 있었습니다.

저희는 여러분들의 기여와 조언을 환영하며, 함께 더 나은 결과물을 만들어나갈 수 있기를 기대합니다! 기여하고 싶으시다면 다음 단계를 따라주세요:

- **1단계**: 추가적인 기능이나 개선 사항을 추가하고 싶거나 경험 중에 문제를 마주치면 [이슈](https://github.com/xlang-ai/OpenAgents/issues)를 게시해주세요. 또한 [이슈 템플릿](https://github.com/xlang-ai/OpenAgents/blob/main/CONTRIBUTING.md)을 따라주시면 감사하겠습니다. 이슈는 해당 위치에서 논의되고 할당될 것입니다.
- **2단계**: 이슈가 할당되면 [풀 리퀘스트 템플릿](https://github.com/xlang-ai/OpenAgents/blob/main/CONTRIBUTING.md)을 따라 [풀 리퀘스트](https://github.com/xlang-ai/OpenAgents/pulls)를 생성하여 기여할 수 있습니다. 또한 열려있는 이슈를 요청할 수도 있습니다. 우리는 함께 OpenAgents를 더욱 발전시킬 수 있습니다!
- **3단계**: PR은 검토와 논의 이후에 병합되거나 반복될 것입니다. 기여해주셔서 감사합니다!

시작하기 전에, [여기](https://github.com/xlang-ai/OpenAgents/blob/main/CONTRIBUTING.md)를 확인하는 것을 강력히 권장합니다.

## 📖 문서화
전체 문서에 대해서는 [여기](https://docs.xlang.ai)를 확인해주세요. 문서는 데모 변경 및 코드 릴리스와 함께 최신화될 예정입니다.

## 🧙‍어떤 분들이 참여하고 있나요?

### 기술 리드

<a href="https://github.com/Impavidity"><img src="https://avatars.githubusercontent.com/u/9245607?v=4"  width="50" /></a>

### 공동 리드 기여자

<a href="https://github.com/BlankCheng"><img src="https://avatars.githubusercontent.com/u/34505296?v=4"  width="50" /></a>
<a href="https://github.com/koalazf99"><img src="https://avatars.githubusercontent.com/u/37338733?v=4"  width="50" /></a>
<a href="https://github.com/Timothyxxx"><img src="https://avatars.githubusercontent.com/u/47296835?v=4"  width="50" /></a>

### 주요 기여자

<a href="https://github.com/taogoddd"><img src="https://avatars.githubusercontent.com/u/98326623?v=4"  width="50" /></a>
<a href="https://github.com/WhiteWolf82"><img src="https://avatars.githubusercontent.com/u/48792453?v=4"  width="50" /></a>
<a href="https://github.com/ztjhz"><img src="https://avatars.githubusercontent.com/u/59118459?v=4"  width="50" /></a>

### 소중한 기여자

<a href="https://github.com/BillStark001"><img src="https://avatars.githubusercontent.com/u/31788509?v=4"  width="50" /></a>
<a href="https://github.com/SivilTaram"><img src="https://avatars.githubusercontent.com/u/10275209?v=4"  width="50" /></a>
<a href="https://github.com/che330"><img src="https://avatars.githubusercontent.com/u/122778503?v=4"  width="50" /></a>
<a href="https://github.com/leo-liuzy"><img src="https://avatars.githubusercontent.com/u/11146950?v=4"  width="50" /></a>
<a href="https://github.com/ranpox"><img src="https://avatars.githubusercontent.com/u/25601999?v=4"  width="50" /></a>
<a href="https://github.com/hongjin-su"><img src="https://avatars.githubusercontent.com/u/114016954?v=4"  width="50" /></a>
<a href="https://github.com/QIN2DIM"><img src="https://avatars.githubusercontent.com/u/62018067?v=4"  width="50" /></a>
<a href="https://github.com/xJQx"><img src="https://avatars.githubusercontent.com/u/47933193?v=4"  width="50" /></a>
<a href="https://github.com/thomasshin"><img src="https://avatars.githubusercontent.com/u/76890354?v=4"  width="50" /></a>

### 감사의 말 (코드를 넘어서)
OpenAgents에 많은 기여를 해주신 [Ziyi Huang](https://www.joanna-ziyi-huang.com/), [Roxy Rong](https://www.linkedin.com/in/roxyrong/), [Haotian Li](https://haotian-li.com/), [Xingbo Wang](https://andy-xingbowang.com/), [Jansen Wong](https://www.linkedin.com/in/jansenwong/), 그리고 [Chen Henry Wu](https://chenwu.io/) 께 진심으로 감사의 마음을 전합니다. 이분들의 전문성과 통찰력은 이 프로젝트를 완성하는 데 중요한 역할을 했습니다!

### 오픈소스 기여자
기여해 주신 모든 분들께 감사드립니다!

<a href="https://github.com/xlang-ai/OpenAgents/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=xlang-ai/OpenAgents" />
</a>

## 인용
만약 여러분에게 우리의 프로젝트가 도움이 되었다면, 다음과 같이 인용해 주시기 바랍니다:
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

## 감사의 말

저희에게 이 오픈 소스 프로젝트를 위해 연구 기금을 제공해 준 Google Research, Amazon AWS, 그리고 Salesforce Research에게 감사드립니다!

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

## ⭐️ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=xlang-ai/OpenAgents&type=Date)](https://github.com/xlang-ai/OpenAgents/stargazers)

<h3 align="center">
OpenAgents에게 ⭐️를 주는 것은 그것을 더욱 빛나게 만들고 더 많은 사람들에게 혜택을 주는 것입니다.
</h3>
# [OpenAgents: 現実の世界の言語エージェントのためのオープンプラットフォーム](https://arxiv.org/abs/2310.10634)

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
    <a>日本語</a> •
    <a href="README_KO.md">한국어</a>
</p>

現在の言語エージェントのフレームワークは、概念実証の言語エージェントの構築を容易にすることを目的としているが、エージェントへの専門家でないユーザのアクセスを無視し、アプリケーションレベルの設計にはほとんど注意を払っていません。
私たちは、日常生活の中で言語エージェントを使用し、ホスティングするためのオープンプラットフォーム、OpenAgents を構築しました。

現在、3つのエージェントを OpenAgents で実装し、[デモ](https://chat.xlang.ai)でホスティングして自由に使っています！
1. データエージェントは、Python/SQL とデータツールを使ってデータ分析を行います;
2. 200 以上のデイリーツールを備えたプラグインエージェント;
3. 自律的なウェブ閲覧のためのウェブエージェント。

OpenAgents は、ChatGPT Plus と同様に、データ分析、プラグインの呼び出し、ブラウザの制御を行うことができますが、OPEN Code for the OpenAgents では、以下のことが可能です
1. 簡単なデプロイ
2. フルスタック
3. チャット Web UI
4. エージェントメソッド
5. …

OpenAgents は、一般ユーザーが迅速な応答と一般的な障害のために最適化されたウェブUIを通じてエージェント機能と対話することを可能にする一方で、開発者や研究者にローカルセットアップでのシームレスなデプロイ体験を提供し、革新的な言語エージェントを作り、実世界での評価を容易にするための基盤を提供します。
我々は、実世界における言語エージェントの将来的な研究開発のための基礎となることを目指し、課題と有望な機会の両方を明らかにします。

## 🔫 トラブルシューティング
[online demo](https://chat.xlang.ai)やローカルデプロイメントで問題が発生した場合、私たちのDiscordに参加してヘルプを求めてください。また、機能やコードで問題がある場合は、[issue](https://github.com/xlang-ai/OpenAgents/issues) を作成してください。

## 🔥 ニュース

- **[2023, Oct 26]** 私たちのユーザー数が3,000人に達しました！🚀 すべてのユーザーおよび貢献者の皆様に心からの感謝を申し上げます！🙏 サーバー上の予期しない高いトラフィックを処理する中、我慢してください。お客様の忍耐に感謝し、できるだけ早くサポートさせていただきます！
- **[2023, Oct 18]** [私たちの Lemur](https://github.com/OpenLemur/Lemur) を試してみてください。SOTA とオープンソース化された言語エージェントの基礎モデルで、ChatGPT と 15 のエージェントタスクがマッチします！
- **[2023, Oct 17]** [こちら](https://arxiv.org/abs/2310.10634)で OpenAgents の論文をご覧ください！
- **[2023, Oct 13]** サーババックエンドとフロントエンドの3つのエージェントすべてについて、OpenAgents プラットフォームコードをリリースしました！ご自分のローカルホストをセットアップして、OpenAgents で遊んでみてください！
- **[2023, Aug 17]** 私たちのプラットフォームが正式に500ユーザーに達しました！🚀
- **[2023, Aug 8]** データ、プラグイン、ウェブエージェントを含む、[OpenAgents デモ](https://chat.xlang.ai) をリリースしました！[チュートリアル](https://docs.xlang.ai/category/user-manual) と [ユースケース](https://docs.xlang.ai/category/use-cases) をご覧ください！


## 🥑 OpenAgents

私たちは、チャットベースのウェブUIを持つ3つの実世界エージェントを構築しました（[OpenAgents demos](https://chat.xlang.ai)を参照してください）。以下は、OpenAgents フレームワークの簡単な概要です。コンセプトや設計の詳細については、[ドキュメント](https://docs.xlang.ai) を参照してください。

### Data エージェント

[Data エージェント](https://github.com/xlang-ai/OpenAgents/tree/main/real_agents/data_agent)は、効率的なデータ運用のために設計された包括的なツールキットである。以下の機能を提供します:

- 🔍 **検索**: 必要なデータを素早く検索。
- 🛠️ **取り扱い**: データ収集と処理を合理化。
- 🔄 **操作**: 特定の要件に合わせてデータを修正。
- 📊 **可視化**: データを明瞭かつ洞察的に表現。

コードの記述と実行に熟達した Data エージェントは、データ中心の幅広いタスクを簡素化します。様々な[ユースケース](https://docs.xlang.ai/use-cases/data-agent)を通じて、その可能性を発見してください。

<div align="center">
    <img src="pics/data_agent.png" width="784"/>
</div>

<details>
  <summary>その他の使用例のスクリーンショットを見るにはクリックしてください</summary>
<div align="center">
    <img src="pics/data_agent_demo.png" width="784"/>
</div>

</details>

### Plugins エージェント

[Plugins エージェント](https://github.com/xlang-ai/OpenAgents/tree/main/real_agents/plugins_agent)は、あなたの日常生活の様々な側面を豊かにするために厳選された200以上のサードパーティプラグインとシームレスに統合します。これらのプラグインを自由に使用することで、エージェントは、より効率的に幅広いタスクとアクティビティに取り組むことができます。

🔌 **サンプルプラグイン**:

- 🛍️ **ショッピング**: Klarna Shopping
- ☁️ **天気**: XWeather
- 🔬 **科学的探求**: Wolfram Alpha


#### プラグインの併用

相乗効果を利用しましょう！Plugins Agent は複数のプラグインの同時使用をサポートします。旅行の計画ですか？Klook、通貨コンバータ、WeatherViz の機能をシームレスに統合します。

#### 自動プラグイン選択

**自動プラグイン選択** 機能で選択を簡素化します。エージェントが直感的に検索し、あなたのニーズに合わせた最適なプラグインを提案します。

Plugins エージェントが実際に使用されている様子を見るには、さらに多くの[使用例](https://docs.xlang.ai/use-cases/plugins-agent)をご覧ください。

<div align="center">
  <img src="pics/plugins_agent.png" width="784"/>
</div>

<details>
  <summary>その他の使用例のスクリーンショットを見るにはクリックしてください</summary>
<div align="center">
    <img src="pics/plugins_agent_demo.png" width="784"/>
</div>

</details>

### Web エージェント

[Web エージェント](https://github.com/xlang-ai/OpenAgents/tree/main/real_agents/web_agent)は、ウェブサイトを自動的にナビゲートして探索するChrome拡張機能のパワーを利用します。このエージェントは、ウェブ閲覧体験を合理化し、関連情報の検索や目的のリソースへのアクセスなどを容易にします。

**ウェブエージェントができることの例**:

- 📍 **Googleマップ ナビゲーション**: 旅を計画中ですか？出発地と目的地を Web エージェントに伝えるだけです。Google マップをナビゲートし、最適なルートを表示します。
- 🐦 **Twitter投稿**: Web エージェントと会話をしていて、X(Twitter) で何かを共有したいと思いましたか？ウェブエージェントがあなたのツイートを処理します。
- 📝 **Googleフォーム アシスタンス**: イベントやアクティビティの申し込みが必要ですか？Google フォームのリンクと必要な情報を共有します。Web エージェントがフォームに入力します。

これらの[ユースケース](https://docs.xlang.ai/use-cases/web-agent)で、Web エージェントの可能性を存分にご覧ください。

<div align="center">
  <img src="pics/web_agent.png" width="784"/>
</div>

<details>
  <summary>その他の使用例のスクリーンショットを見るにはクリックしてください</summary>
<div align="center">
    <img src="pics/web_agent_demo.png" width="784"/>
</div>

</details>


## 💻 ローカルホストデプロイメント
OpenAgentsプラットフォームのコードをリリースしました。お気軽にご自身のローカルホストでデプロイしてみてください！

こちらがOpenAgentsのシステムデザインの概要です：

<div align="center">
    <img src="pics/system_design.png"/>
</div>

### ソースコードから
セットアップとローカルホストでの使用については、以下のフォルダとREADMEファイルをご確認ください：

1. バックエンド：三つのエージェントをホストするためのflaskバックエンド。
2. フロントエンド：フロントエンドのUIとWeBot Chrome拡張機能。
P.S.：コードの中でいくつかの引数をより読みやすくするためにリネームしました。2023年10月26日以前にコードをプルしていた方へのリマインダーとして、最新のコードをプルしたい場合は、キー名の違いにより以前のローカルチャット履歴が失われることをご注意ください。

### Docker
OpenAgentsプラットフォームをデプロイするためにdocker-composeを使用する手順は以下の通りです。

注意: Dockerは開発中のため、一部の機能が正常に動作しないか、反応が遅い場合があります。何か質問があれば、お気軽にissueをオープンしてください。より安定したバージョンをお求めの方には、現在のところソースコードからデプロイすることをお勧めします。

1. Kaggleのデータセットを使用したい場合は、Dockerfileの情報を正しい情報に変更する必要があります。
```
ENV KAGGLE_USER="" \
    KAGGLE_KEY="" 
```
2. ローカルで実行していない場合は、frontend/Dockerfileのバックエンドサービスへのアクセス可能なIPを変更する必要があります。
```
ENV NEXT_PUBLIC_BACKEND_ENDPOINT http://x.x.x.x:8000
```
3. プロジェクトのルートディレクトリでdocker compose buildコマンドを実行します。
4. Openaiの非公式サービス、例えばFastChatを使用する場合は、docker-compose.ymlのOPENAI_API_BASEを変更する必要があります。それ以外の場合は、docker-compose.ymlにOPENAI_API_KEYを入れるだけです。
5. 上記のステップを完了したら、docker compose up -dを実行してすべてのサービスを開始できます。


## 📜 OpenAgentsを拡張するためのチュートリアル
### コードの構造
OpenAgentsを拡張する方法を深く探る前に、理解を深めるためにまずコードの構造を見てみましょう。
OpenAgentsのコード構造は以下の通りです:
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
示されている通り、`backend/` と `frontend/` は自己完結型であり、直接デプロイ可能です（[こちら](#localhost-deployment)を参照）。
これは、それらが変更できないという意味ではありません。
むしろ、従来の*クライアント-サーバー*アーキテクチャに従って、backendとfrontendをお好みに応じて拡張できます。
`real_agents/` については、「一つのエージェント、一つのフォルダ」という設計にしていますので、新しいエージェントを簡単に拡張できます。
ここでの「実エージェント」という名前は、概念的な言語エージェントの部分だけでなく、言語エージェントとbackendとの間のギャップもここに埋められているためです。
例えば、`adapters/` には、ストリーム解析、データモデル、メモリ、コールバックなどの共有アダプターコンポーネントが含まれています。
関心のある読者は、概念と実装デザインについて、私たちの[論文](https://arxiv.org/abs/2310.10634)を参照してください。
そして、実エージェントを構築するためのベースとして[LangChain](https://github.com/langchain-ai/langchain)のコードを使用していることに感謝します。

### 新しいエージェントを拡張する
私たちが提供する三つのエージェントを超えて新しいエージェントを構築したい場合、以下の手順に従ってください：
- 既存のエージェントがどのように実装されているかを確認するために `real_agents/` フォルダを参照し、エージェント用の新しいフォルダを作成します。
- 新しいフォルダでエージェントのロジックを実装します。必要に応じて `adapters/` フォルダのコンポーネントを使用します。
- 新しいエージェントのチャットAPIを定義するための `chat_<new_agent>.py` ファイルを `backend/api/` フォルダに追加し、これはfrontendから呼び出されます。
- 必要に応じて `backend/schemas.py` に新しい定数を登録します。
- `frontend/types/agent.ts` に新しい `OpenAgentID` を追加し、`frontend/utils/app/api.ts` と `frontend/utils/app/const.ts` に対応するAPIを追加します。
- 必要に応じて `frontend/components/Chat/Chat.tsx` と `frontend/components/Chat/ChatMessage.tsx` でエージェントのUIを実装します。
- localhostのスクリプトを実行し、新しいエージェントをテストします。

注意：新しいデータタイプ、つまり、テキスト、画像、テーブル、およびjsonを超えて、`backend/display_streaming.py` でその解析ロジックを実装し、新しいデータモデルを追加する必要があるかもしれません。

### 新しいLLMを拡張する
LLMがすでにホストされており、API経由で呼び出すことができる場合、エージェントのバックボーンとして新しいLLMを拡張するのは簡単です。
新しいモデルを `backend/api/language_model.py` に

登録するだけです。lemur-chatをテンプレートとして参照してください。

もしLLMがまだホストされていない場合、新しいLLMをデプロイし、APIとして公開する方法についてのチュートリアルが[こちら]() (LLMホスティングはtodo)にあります。

### 新しいツールを拡張する
Plugins Agentで新しいツールを拡張したい場合は、以下の手順に従ってください：
- 既に構築されているプラグインを `real_agents/plugins_agent/plugins/` で参照し、ツールの新しいフォルダを作成します。
- 新しいフォルダでツールのロジックを実装します。ツールが認識されるためには `ai-plugin.json` と `openapi.yaml` が必要であり（これはLLMによって他のものに従って生成されるか、手動で書かれるかのどちらかです）、`paths/` は実際のツールAPIコールのためのものです。
- 新しいツール名を `real_agents/plugins_agent/plugins/plugin_names.py` に登録します。


## 👏 コントリビュート

[LangChain](https://github.com/langchain-ai/langchain)、[ChatBot UI](https://github.com/mckaywrigley/chatbot-ui)、[Taxy.ai ブラウザ拡張機能](https://github.com/TaxyAI/browser-extension)などのオープンソースコミュニティの努力のおかげです。私たちは、インターフェイスのプロトタイプをより便利かつ効率的に構築することができます。

私たちは投稿や提案を歓迎し、共により良いものへと前進していきます！

- 🐛 使用中に何か問題が発生したり、機能を追加したい場合は、[issue](https://github.com/xlang-ai/OpenAgents/issues) を投稿してください。
- 🕹 [プルリクエスト](https://github.com/xlang-ai/OpenAgents/pulls) を作成して、私たちのリポジトリに直接貢献してください。一緒に OpenAgents をより良いものにしましょう！
- ⭐ [X(Twitter)](https://twitter.com/XLangNLP)で私たちをフォローし、あなた自身の例を共有し、お友達とシェアしてください！

寄稿方法の詳細については、[こちら](https://github.com/xlang-ai/OpenAgents/blob/main/CONTRIBUTING.md)を参照のこと。

## 📖 ドキュメント

デモの変更とコードのリリースに合わせて更新されます。完全なドキュメントは[こちら](https://docs.xlang.ai)をご覧ください。


## 🧙 参加メンバー

### テックリード

<a href="https://github.com/Impavidity"><img src="https://avatars.githubusercontent.com/u/9245607?v=4"  width="50" /></a>

### 共同リードコントリビューター

<a href="https://github.com/BlankCheng"><img src="https://avatars.githubusercontent.com/u/34505296?v=4"  width="50" /></a>
<a href="https://github.com/koalazf99"><img src="https://avatars.githubusercontent.com/u/37338733?v=4"  width="50" /></a>
<a href="https://github.com/Timothyxxx"><img src="https://avatars.githubusercontent.com/u/47296835?v=4"  width="50" /></a>

### 主要コントリビューター

<a href="https://github.com/taogoddd"><img src="https://avatars.githubusercontent.com/u/98326623?v=4"  width="50" /></a>
<a href="https://github.com/WhiteWolf82"><img src="https://avatars.githubusercontent.com/u/48792453?v=4"  width="50" /></a>
<a href="https://github.com/ztjhz"><img src="https://avatars.githubusercontent.com/u/59118459?v=4"  width="50" /></a>

### 貴重なコントリビューター

<a href="https://github.com/BillStark001"><img src="https://avatars.githubusercontent.com/u/31788509?v=4"  width="50" /></a>
<a href="https://github.com/SivilTaram"><img src="https://avatars.githubusercontent.com/u/10275209?v=4"  width="50" /></a>
<a href="https://github.com/che330"><img src="https://avatars.githubusercontent.com/u/122778503?v=4"  width="50" /></a>
<a href="https://github.com/leo-liuzy"><img src="https://avatars.githubusercontent.com/u/11146950?v=4"  width="50" /></a>
<a href="https://github.com/ranpox"><img src="https://avatars.githubusercontent.com/u/25601999?v=4"  width="50" /></a>
<a href="https://github.com/hongjin-su"><img src="https://avatars.githubusercontent.com/u/114016954?v=4"  width="50" /></a>
<a href="https://github.com/QIN2DIM"><img src="https://avatars.githubusercontent.com/u/62018067?v=4"  width="50" /></a>
<a href="https://github.com/xJQx"><img src="https://avatars.githubusercontent.com/u/47933193?v=4"  width="50" /></a>
<a href="https://github.com/thomasshin"><img src="https://avatars.githubusercontent.com/u/76890354?v=4"  width="50" /></a>

### 謝辞（コード以外）

[Ziyi Huang](https://www.joanna-ziyi-huang.com/), [Roxy Rong](https://www.linkedin.com/in/roxyrong/), [Haotian Li](https://haotian-li.com/), [Xingbo Wang](https://andy-xingbowang.com/), [Jansen Wong](https://www.linkedin.com/in/jansenwong/), [Chen Henry Wu](https://chenwu.io/) の OpenAgents への貴重な貢献に心から感謝します。彼らの専門知識と洞察力は、このプロジェクトを実現する上で大いに役立ちました！

### オープンソースコントリビューター

すべての貢献者に感謝します！

<a href="https://github.com/xlang-ai/OpenAgents/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=xlang-ai/OpenAgents" />
</a>

## 引用
私たちの仕事が役に立つと思われた場合は、引用してください:
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

## 謝辞

Google Research、Amazon AWS、Salesforce Research から、このオープンソースの取り組みに研究助成金をいただいたことに感謝します！

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
<b>OpenAgents</b> へ ⭐️ を付けることで、より輝かせ、より多くの人々に利益をもたらすことにつながります。
</h3>


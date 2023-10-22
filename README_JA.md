# [OpenAgents: 野生の言語エージェントのためのオープンプラットフォーム](https://arxiv.org/abs/2310.10634)

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
    <a>日本語</a>
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

## 🔥 ニュース

- **[2023, Oct 18]** [私たちの Lemur](https://github.com/OpenLemur/Lemur) を試してみてください。SOTA とオープンソース化された言語エージェントの基礎モデルで、ChatGPT と 15 のエージェントタスクがマッチします！
- **[2023, Oct 17]** [こちら](https://arxiv.org/abs/2310.10634)で OpenAgents の論文をご覧ください！
- **[2023, Oct 13]** サーババックエンドとフロントエンドの3つのエージェントすべてについて、OpenAgents プラットフォームコードをリリースしました！ご自分のローカルホストをセットアップして、OpenAgents で遊んでみてください！
- **[2023, Aug 17]** 私たちのプラットフォームが正式に500ユーザーに達しました！🚀
- **[2023, Aug 8]** データ、プラグイン、ウェブエージェントを含む、[OpenAgents デモ](https://chat.xlang.ai) をリリースしました！[チュートリアル](https://docs.xlang.ai/category/user-manual) と [ユースケース](https://docs.xlang.ai/category/use-cases) をご覧ください！

## 💻 ローカルホストへのデプロイ

OpenAgents プラットフォームのコードをリリースしました。ご自由にローカルホストにデプロイしてください！

以下は、OpenAgents の簡単なシステム設計です:
<div align="center">
    <img src="pics/system_design.png"/>
</div>

以下のフォルダと README ファイルをチェックして、localhost をセットアップしてください:

1. [**backend**](backend/README.md): flask バックエンドは 3 つのエージェントをホストします。
2. [**frontend**](frontend/README.md): フロントエンド UI と WeBot Chrome 拡張機能。

## 🥑 OpenAgents

私たちは、チャットベースのウェブUIを持つ3つの実世界エージェントを構築しました（[OpenAgents demos](https://chat.xlang.ai)を参照してください）。以下は、OpenAgents フレームワークの簡単な概要です。コンセプトや設計の詳細については、[ドキュメント](https://docs.xlang.ai) を参照してください。

### Data エージェント

[Data エージェント](https://github.com/xlang-ai/OpenAgents/tree/main/real_agents/data_agent)は、効率的なデータ運用のために設計された包括的なツールキットである。以下の機能を提供します:

- 🔍 **Search**: 必要なデータを素早く検索。
- 🛠️ **Handle**: データ収集と処理を合理化。
- 🔄 **Manipulate**: 特定の要件に合わせてデータを修正。
- 📊 **Visualize**: データを明瞭かつ洞察的に表現。

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

- 🛍️ **Shopping**: Klarna Shopping
- ☁️ **Weather**: XWeather
- 🔬 **Scientific Exploration**: Wolfram Alpha

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

- 📍 **Google Maps Navigation**: 旅を計画中ですか？出発地と目的地を Web エージェントに伝えるだけです。Google マップをナビゲートし、最適なルートを表示します。
- 🐦 **Twitter Postings**: Web エージェントと会話をしていて、X(Twitter) で何かを共有したいと思いましたか？ウェブエージェントがあなたのツイートを処理します。
- 📝 **Google Form Assistance**: イベントやアクティビティの申し込みが必要ですか？Google フォームのリンクと必要な情報を共有します。Web エージェントがフォームに入力します。

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

## 📖 ドキュメント

デモの変更とコードのリリースに合わせて更新されます。完全なドキュメントは[こちら](https://docs.xlang.ai)をご覧ください。

## 👏 コントリビュート

[LangChain](https://github.com/langchain-ai/langchain)、[ChatBot UI](https://github.com/mckaywrigley/chatbot-ui)、[Taxy.ai ブラウザ拡張機能](https://github.com/TaxyAI/browser-extension)などのオープンソースコミュニティの努力のおかげです。私たちは、インターフェイスのプロトタイプをより便利かつ効率的に構築することができます。

私たちは投稿や提案を歓迎し、共により良いものへと前進していきます！

- 🐛 使用中に何か問題が発生したり、機能を追加したい場合は、[issue](https://github.com/xlang-ai/OpenAgents/issues) を投稿してください。
- 🕹 [プルリクエスト](https://github.com/xlang-ai/OpenAgents/pulls) を作成して、私たちのリポジトリに直接貢献してください。一緒に OpenAgents をより良いものにしましょう！
- ⭐ [X(Twitter)](https://twitter.com/XLangNLP)で私たちをフォローし、あなた自身の例を共有し、お友達とシェアしてください！

寄稿方法の詳細については、[こちら](https://github.com/xlang-ai/OpenAgents/blob/main/CONTRIBUTING.md)を参照のこと。

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

[Ziyi Huang](https://www.joanna-ziyi-huang.com/)、[Roxy Rong](https://www.linkedin.com/in/roxyrong/)、[Haotian Li](https://haotian-li.com/)、[Xingbo Wang](https://andy-xingbowang.com/)、[Jansen Wong](https://www.linkedin.com/in/jansenwong/)、[Chen Henry Wu](https://chenwu.io/)の OpenAgents への貴重な貢献に心から感謝します。彼らの専門知識と洞察力は、このプロジェクトを実現する上で大いに役立ちました！

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


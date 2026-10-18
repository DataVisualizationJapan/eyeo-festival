# 第4回追加記事の資料確認

確認日は2026-10-18。未記事化の5講演を追加し、記事は計18本になった。本文は提供された英文資料を主資料とし、Vimeo oEmbedの公式紹介文で講演題名を確認した。音声・映像全編の独立した再聴取は行っていない。原本は変更していない。

## Mike Bostock、2014年、112319901

主資料は`_documents/2014/Eyeo 2014 - Mike Bostock.mp4.md`。公式講演題名はVisualizing Algorithms。

- 02:14 best-candidate、05:10 比較と再構成、08:16 Bridson、10:19 学習・シャッフル・検査、23:46 アニメーションと静止図、29:34 表示する状態の区別、40:28 条件を探索する住宅比較を確認。
- [作者の講演記事](https://bost.ocks.org/mike/algorithms/)でMitchell、Bridson、Fisher–Yatesなどの名称を確認。記事の長い説明は提供原本を根拠とし、ウェブ記事の翻訳として構成していない。
- 一回の出力と実行分布、経験的な検査と数学的証明を区別。当時のブラウザ挙動を現行仕様として書かない。住宅比較はUIの説明に限定し、購入や投資の助言にしない。

## Taeyoon Choi、2017年、234330230

主資料は`_documents/2017/Eyeo 2017 - Taeyoon Choi.mp4.md`。公式講演題名はAbsence is Presence with Distance。動画原題末尾の`||`はそのまま保持し、登壇者名は確認した表記へ更新。

- 01:40 Handmade Computer、06:25 ビットの回路、09:07 開発を止めた理由、12:09 個人の時計、16:42 時間の主体性、19:28/23:48 Future Proof、26:08 教育、32:20 学びの困難、38:48 支援構造、41:38 ろう学生との学びを確認。
- [作者のGitHub](https://github.com/tchoi8/handmadecomputer)、[LACMAの記事](https://unframed.lacma.org/node/1614)、[SFPCのアーカイブ](https://sfpc.io/projects/)を確認。In Search of Personalized Time、E Roon Kangの名称はLACMAの表記を採用。
- 作品中の参加者の音声をChoi自身の発言としない。標準時刻から外れることを生活上の推奨とはしない。障害やろうの経験を一括りにせず、具体的な道具と場の設計を説明。

## Zach Lieberman、2017年、232656895

主資料は`_documents/2017/Eyeo 2017 - Zach Lieberman.mp4.md`。公式講演題名はPatterns。

- 03:11 働き方への問い、05:26 過去の作品を再構成する授業、11:54/13:46 スケッチの習慣、14:39 余白の円、18:41 反射の展示、23:29/24:40 家族と公開反応、29:26 文字、32:26 身体、34:16 日記、41:19 相談時間を確認。
- [SFPCの当時の記録](https://sfpc.io/projects/)でRecreating the Pastの名称を確認。主要な制作動作は提供原本を根拠に説明。
- インタビュー相手の発言をLieberman自身の助言へ置き換えない。引用された他者の規則や書籍本文は転載しない。不明瞭な作家名・道具名は推測で埋めない。身近な人の病名や詳細は本文の中心から外す。

## Nadieh Bremer、2019年、354276689

主資料は`_documents/2019/Eyeo 2019 - Nadieh Bremer.mp4.md`。公式講演題名はVISUALIZING CONNECTIONS。

- 00:19 星座と王家、14:02/16:44 移動表現、18:47/22:37/23:50 UNESCO、28:11/31:29 検索質問、39:05 計算タスクの依存関係を確認。
- 作者の[Figures in the Sky](https://www.visualcinnamon.com/portfolio/figures-in-the-stars/)と[Intangible Cultural Heritage](https://www.visualcinnamon.com/portfolio/intangible-cultural-heritage/)で名称と題材を確認。
- UNESCOの接続数には紹介文と講演で差があるため、件数は本文に採用していない。王室の肩書や文化遺産数は現在の状況へ外挿しない。Bussed Outは既存Shirley Wu記事と同じ制作を別の担当者の視点から説明する。

## Stefanie Posavec、2022年、777860720

主資料は`_documents/2022/Eyeo 2022 - Stefanie Posavec.mp4.md`。公式講演題名はYOU’RE DOING IT 'WRONG'。

- 主資料は00:24から46:30までが一つの区間。本文の細かな時刻は推定せず、導入に00:24へのリンクを一つ置いた。
- Writing Without Words、Dear Data、National Maritime Museum、Updating Happiness、People Like You、物理的な書籍の順で論旨と説明を照合。
- [作者の作品一覧](https://www.stefanieposavec.com/projects)と[作者サイト](https://www.stefanieposavec.com/)で作品名、Miriam Quick、書名を確認。
- 「間違い」を虚偽の数量表現の推奨にしない。参加型作品の医療的・心理的効能は主張しない。研究過程で確認した情報と数量の推定を区別。書籍にある科学的数値は独立検証していないため転載しない。

## 共通

全記事の「制作へ持ち帰るための視点」は編集上の考察と明示した。原題、年、話者、元資料、編集状態をメタデータに記録した。時刻リンクは原本の開始境界から秒未満を切り捨て、区間内の位置を推測していない。

公開本文には文字起こし処理の説明を含めない。サムネイルは公式Vimeo oEmbedから取得し、取得元・寸法・SHA-256を`data/thumbnails.json`に保存する。

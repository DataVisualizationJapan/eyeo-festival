# eyeoを読む

Eyeo Festivalの講演を日本語で読むための非公式アーカイブ。Hugoの独自テンプレートと、依存ライブラリ不要のPythonスクリプトで構成しています。公開先は`DataVisualizationJapan/eyeo-festival`です。デプロイは手動実行です。

## ローカルで見る

必要環境：Hugo **0.152.0**（ローカルとCIで検証したバージョン）、Python **3.12以上**。npmやGoモジュールのインストールは不要です。

```sh
hugo server --bind 127.0.0.1 --port 1313 --disableFastRender
```

[http://localhost:1313/](http://localhost:1313/) を開きます。通常の閲覧とビルドはネットワーク不要です。動画は再生ボタンを押したときにVimeoへ接続します。

## 現在の収録範囲

公式Vimeoの全37ページを2026-10-17に収集。443本のうち、Eyeoが397本、別イベントのINSTINTが46本です。公開索引はEyeoのみを表示します。動画一覧の件数には講演以外の関連映像も含みます。

| 開催年 | Eyeo動画 | 文字起こしがある動画 | 原本ファイル |
| --- | ---: | ---: | ---: |
| 2011 | 17 | 2 | 3 |
| 2012 | 45 | 4 | 4 |
| 2013 | 47 | 18 | 18 |
| 2014 | 41 | 31 | 31 |
| 2015 | 43 | 2 | 2 |
| 2016 | 45 | 35 | 37 |
| 2017 | 39 | 31 | 34 |
| 2018 | 40 | 30 | 32 |
| 2019 | 40 | 28 | 31 |
| 2022 | 40 | 39 | 42 |
| **計** | **397** | **220** | **234** |

234ファイル中、220件は時刻付きCSV、13件はプレーンテキスト、1件は時刻を含む英日併記です。同じ動画の別形式を14件含みます。タイトルの完全一致で224ファイル、確認済みの表記差によって10ファイルを照合しました。新規の音声文字起こしは行っていません。

初回記事：Ben Fry（2016）、Nervous System（2011）、Casey Reas（2018）。各記事は日本語の解説であり、全文翻訳ではありません。本文・時刻は提供された原本と照合し、固有名詞は記事末の一次資料で確認しました。映像全編の独立した聞き取り確認は行っていません。

追加記事：Nicky Case（2016）、Giorgia Lupi（2018）、Amanda Cox（2018）、Lauren McCarthy（2019）、Shirley Wu（2022）。第2回追加までで計8記事です。追加5本の本文は出典・URLを含め約4,400〜4,900字で、資料確認の記録は`docs/editorial-review-batch-02.md`にまとめています。

さらにAaron Koblin（2011）、Leah Buechley（2014）、Patricio Gonzalez Vivo（2016）、Moritz Stefaner（2016）、Hannah Davis（2018）を追加し、第3回追加までで計13記事です。今回の5本は出典・URLを含め約4,000〜4,200字。確認記録は`docs/editorial-review-batch-03.md`にあります。全記事に公式Vimeoサムネイルを付けています。

Mike Bostock（2014）、Taeyoon Choi（2017）、Zach Lieberman（2017）、Nadieh Bremer（2019）、Stefanie Posavec（2022）を追加し、第4回追加までで計18記事です。第4回の本文は出典・URLを含め約4,100〜4,400字です。確認記録は`docs/editorial-review-batch-04.md`にあります。

Nathan Yau（2019）、Mohit Bhoite（2019）、Daniel Shiffman（2019）、Catherine D’Ignazio（2019）、Ariel Waldman（2022）を追加し、この時点で計23記事です。第5回の本文は出典・URLを含め約4,000〜4,500字です。確認記録は`docs/editorial-review-batch-05.md`にあります。

Helena Sarin（2019）、Nicole Aptekar（2019）、Nadja Popovich（2022）、Sarah Groff Hennigh-Palermo（2019）、Walter Kitundu（2022）を追加し、現在は計28記事です。第6回の本文は出典・URLを含め約3,800〜4,200字です。確認記録は`docs/editorial-review-batch-06.md`にあります。


## ファイルの役割

- `_documents/`：提供された原本。変更しません。Hugoの出力対象には含まれません。
- `data/videos.json`：動画IDを識別子とする台帳。取得時点、ページ別件数・URL・取得HTMLのSHA-256、原題、年、イベント、種別、登壇者、文字起こしの有無、記事の状態を保持。
- `data/transcripts.json`：原本のSHA-256、形式、動画との対応、照合方法。文字起こし本文は格納しません。
- `data/overrides.json`：確認済みメタデータと照合例外。照合理由を必ず記録します。
- `content/talks/{動画ID}.md`：手で編集する記事。URLは `/talks/{動画ID}/` に固定。
- `content/years/`、`content/speakers/`：台帳から生成する索引。`_index.md`以外は直接編集しません。
- `layouts/`、`assets/`：独自テーマのテンプレート、CSS、JavaScript。外部テーマへの依存はありません。
- `docs/`：資料確認と検証の記録。公開ページには出力されません。

`metadata_status: title_only`の登壇者・種別は原題から整理した情報です。パネルの題名を参加者名として推定しません。略称・グループ名・表記違いは現状で統合しきっていないため、登壇者索引は完全な人物名簿ではありません。確認した名前の修正は`overrides.json`へ追加します。

## 動画台帳を更新する

ネットワークが使える環境で実行します。APIキー、動画のダウンロード、文字起こしサービスは不要です。

```sh
python3 scripts/collect_videos.py
python3 scripts/build_inventory.py
python3 scripts/prepare_content.py
python3 scripts/validate.py
```

収集は公式一覧のページ送りに従います。ページが空、重複ID、表示総数との不一致があれば、台帳の書き換え前に停止します。取得には通常数分かかります。ページ別のハッシュは収集時点の証跡であり、HTMLそのものを保存・再配布するものではありません。

`build_inventory.py`はタイトルを正規化し、同年の一致候補を照合します。あいまいな候補は自動確定せず、`unresolved`として上位候補を出力します。本文や公式情報で確認してから、`data/overrides.json`の`transcripts`へ次の形で登録してください。

```json
{
  "_documents/2022/文字起こし名.md": {
    "video_id": "123456789",
    "reason": "照合に使った根拠を記述"
  }
}
```

原本の更新だけなら収集スクリプトは省略し、照合→索引生成→検証を実行します。時刻付きCSV、時刻付きテキスト、プレーンテキストの順に優先します。原本ファイルのSHA-256が変わった場合、検証は再照合を要求します。

## 記事を追加する

1. 対象動画の`preferred_transcript`を読み、必要に応じて別形式も参照します。
2. `content/talks/{動画ID}.md`に記事を作成します。既存3本のJSON front matterを雛形にし、動画ID・原題・年・登壇者・テーマ・概要・原本パス・編集状態・更新日を設定します。`visual`は`tools`、`nature`、`film`から選べます。
3. 章立てで講演を再構成し、補足・考察を明記します。作品名・用語は一次資料で確認し、出典を記事末に置きます。不確かな数値や聞き取りは補いません。時刻リンクは元資料の区切りに合わせて`https://vimeo.com/{ID}#t=12m48s`とします。
4. 下書き中は`"draft": true`、`"editorial_status": "draft"`を設定します。公開原稿にする際は`draft`を`false`にし、`editorial_status`を`published`にします。
5. `python3 scripts/prepare_content.py`を実行し、台帳の記事状態と索引を更新してから、以下の検証を実行します。

記事ごとの原本パスは管理用メタデータです。テンプレートでは公開せず、公開ページには元動画と一次資料のリンクを表示します。

記事の追加後、`python3 scripts/fetch_thumbnails.py`で公式Vimeoのサムネイルを取得します（ネットワーク接続が必要）。画像は`assets/thumbnails/`、取得元とハッシュは`data/thumbnails.json`に保存します。一覧のカードと記事最上部の動画プレビューで使用し、HugoがWebPの大小2サイズを生成します。画像が未登録の記事は従来の図案を表示します。閲覧時に画像取得のためVimeoへ接続することはありません。

読者向けの本文・注記・説明ページには、文字起こしの形式、Speaker分割、誤認識の補正、CSVや時刻の処理などの制作内部の説明を載せません。こうした記録は`docs/`に残し、記事末は「出典・関連資料」として参照先を案内します。

## 検証

```sh
python3 scripts/test_ingestion.py
python3 scripts/validate.py
hugo --minify --baseURL https://example.org/eyeo-test/ --destination /tmp/eyeo-public
python3 scripts/check_output.py /tmp/eyeo-public --base-path /eyeo-test/
```

原本ハッシュ、照合漏れ、重複ID、記事と台帳の整合、時刻リンクの根拠を検査します。出力検査は内部リンク・見出しアンカー・サブパス・公開対象からの原本除外を確認します。外部サイトの稼働状態はオフライン検査の対象外です。

ブラウザでは、キーワード、複合絞り込み、0件表示、条件のリセット、URLからの検索復元、年・登壇者・テーマ索引、キーボード操作、狭い画面、動画のクリック読み込みを確認します。JavaScriptを無効にしても全動画のリンクは読めます。

## GitHub Pagesへの公開

公開URLは **https://eyeo-festival.data-visualization.jp/** です。`hugo.toml`の`baseURL`と`static/CNAME`に設定済みです。公開先は[DataVisualizationJapan/eyeo-festival](https://github.com/DataVisualizationJapan/eyeo-festival)です。DNSの設定値と公開手順は[docs/github-pages.md](docs/github-pages.md)にまとめています。

1. `_documents/`はローカルに保持し、公開リポジトリには含めません（`.gitignore`で除外）。CIは`validate.py --without-sources`で公開メタデータを検証します。原本ハッシュと時刻境界は、記事追加時にローカルで通常の`validate.py`を実行して検証します。
2. リポジトリのSettings → PagesでSourceを **GitHub Actions** にします。
3. リポジトリのPages設定のCustom domainを`eyeo-festival.data-visualization.jp`にし、DNSを公開先に合わせて設定します。`hugo.toml`と`static/CNAME`は同じドメインを維持します。`baseURL`には末尾の`/`を含めます。
4. Actionsの **Build and verify** で検証します。push・PR・手動実行はビルドのみで、公開しません。
5. 公開するときだけ **Deploy to GitHub Pages (manual)** を手動実行します。GitHubのPages設定から取得したURLでビルドし、`public/`のみをデプロイします。独自ドメインもPages設定から解決します。

初回pushとGitHub ActionsのBuild and verifyは成功しています。GitHub PagesはGitHub Actions方式、Custom domainは`eyeo-festival.data-visualization.jp`に設定済みです。DNS設定と手動デプロイは未実施です。Hugoは検証済みバージョンに固定し、Actionsは公式のメジャーバージョンを使用しています。PR操作はユーザーの許可を得てから、最新状態と差分を確認して行います。

参考：[Hugo公式のGitHub Pages公開手順](https://gohugo.io/host-and-deploy/deploy-to-github-pages/)。


## アクセス解析

共通仕様は [docs/analytics.md](docs/analytics.md) を参照してください。測定IDと本番ホスト名は analytics.json に集約しています。GA管理画面の履歴変更による自動ページビューとサイト内検索の自動収集を無効にしてから公開してください。検索語を含むURLパラメータのデータ編集設定も必要です。

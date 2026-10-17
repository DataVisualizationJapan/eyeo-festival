# GitHub Pages 公開設定

- リポジトリ：https://github.com/DataVisualizationJapan/eyeo-festival
- 公開URL：https://eyeo-festival.data-visualization.jp/
- GitHub PagesのSource：GitHub Actions（APIでは`build_type: workflow`）
- Custom domain：`eyeo-festival.data-visualization.jp`

## DNS

`data-visualization.jp`のDNSゾーンに次を追加する。TTLは3600秒またはDNSサービスの既定値。

| 種別 | ホスト名 | 値 |
| --- | --- | --- |
| CNAME | eyeo-festival | datavisualizationjapan.github.io. |

完全なホスト名を求めるサービスでは`eyeo-festival.data-visualization.jp`を入力。値には`https://`やリポジトリ名`/eyeo-festival/`を付けない。今回のサブドメイン用にルートドメインのレコードを変更する必要はない。

GitHub側のCustom domainを登録してからDNSを追加する。DNS反映後にPages設定の確認結果を見て、証明書が利用可能になったらEnforce HTTPSを有効にする。

```sh
dig +short CNAME eyeo-festival.data-visualization.jp
```

期待値：`datavisualizationjapan.github.io.`。反映には最大24時間程度かかる場合がある。

## ビルドと初回公開

pushでは`Build and verify`だけを実行する。サイトを公開するときに、Actionsの`Deploy to GitHub Pages (manual)`を手動実行する。Pages設定から取得したURLでビルドするため、Custom domainを先に登録する。

`static/CNAME`は出力にも含めるが、GitHub Actionsによる公開ではこのファイルだけで独自ドメインは設定されない。リポジトリのPages設定が必要。

## 文字起こし原本の取り扱い

`_documents/`はローカルに保持し、`.gitignore`で公開リポジトリへの追加を除外する。GitHub CIでは`validate.py --without-sources`により公開メタデータを検査する。このモードでは原本ハッシュ・時刻境界の検証は省略されるため、記事追加時には原本のあるローカルで通常の`python3 scripts/validate.py`を必ず実行する。デプロイ対象はHugoの生成した`public/`のみ。

## 公式資料

- https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site

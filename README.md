# G検定 模擬試験アプリケーション

このプロジェクトは、Gradio を活用して G検定の模擬試験を行うアプリケーションです。  
CSV ファイル（`data/g_exam_questions.csv`）に325問分の問題、選択肢、回答が格納されており、これを読み込んでユーザーに出題します。

## 構成

```
g_exam_mock/
├── app.py                # メインのアプリケーションコード
├── requirements.txt      # 必要なパッケージ情報
├── README.md             # このファイル
└── data/
    └── g_exam_questions.csv  # 問題データ（CSV形式）
```

## 使い方

1. リポジトリをクローン

   ```bash
   git clone <repository_url>
   cd g_exam_mock
   ```

2. 必要なパッケージのインストール

   ```bash
   pip install -r requirements.txt
   ```

3. アプリケーションの起動

   ```bash
   python app.py
   ```

4. 表示された URL にアクセスして模擬試験を開始してください。

## CSVファイルについて

CSV ファイルは以下のカラムを想定しています：

- **問題**: 問題文  
- **選択肢**: カンマ区切りで記述された複数の選択肢  
- **回答**: 正解の選択肢

必要に応じて、`app.py` 内の CSV 読み込み処理やオプションのパース方法を修正してください。

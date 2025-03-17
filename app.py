import pandas as pd
import gradio as gr

# === CSVファイルの読み込み ===
df = pd.read_csv("data/g_exam_questions.csv").sample(frac=1)

# CSV のカラム例:
# カテゴリ, サブカテゴリ, 問題番号, 問題, 選択肢A, 選択肢B, 選択肢C, 選択肢D, 正解
questions_list = []
for _, row in df.iterrows():
    question_text = row["問題"]
    options = [
        row["選択肢A"],
        row["選択肢B"],
        row["選択肢C"],
        row["選択肢D"]
    ]
    correct_letter = row["正解"]  # "A" / "B" / "C" / "D"
    questions_list.append({
        "question": question_text,
        "options": options,
        "answer": correct_letter
    })

# "A" "B" "C" "D" をインデックスに変換するマップ
answer_map = {"A": 0, "B": 1, "C": 2, "D": 3}

def submit_answer(selected, current_index, score):
    """
    ユーザーが選択したテキストと、CSV で指定された「A/B/C/D」に対応するテキストを比較。
    """
    if current_index < len(questions_list):
        correct_letter = questions_list[current_index]["answer"]  # 例: "B"
        correct_index = answer_map[correct_letter]                # 例: 1
        correct_text = questions_list[current_index]["options"][correct_index]

        if selected == correct_text:
            score += 1
            feedback = "正解！"
        else:
            feedback = f"不正解。正しい答えは: {correct_text}"
    else:
        feedback = "試験は終了しています。"
    return feedback, score

def next_question(current_index):
    """
    現在の問題インデックスを 1 進めて次の問題を取得し、
    Radio と Markdown を更新するための値を返す。
    """
    new_index = current_index + 1
    if new_index < len(questions_list):
        q = questions_list[new_index]
        question_text = f"Q{new_index + 1}: {q['question']}"
        options = q["options"]
    else:
        question_text = "試験終了！お疲れさまでした。"
        options = []

    # Radio の選択肢を置き換え、選択をクリア (value=None)
    return [
        new_index,                       # current_index の更新
        question_text,                  # Markdown 用のテキスト
        gr.update(choices=options, value=None),  # Radio を新しい選択肢に更新
        ""                              # フィードバックをリセット
    ]

# --- カスタム CSS で Radio を縦に並べる ---
css_code = """
/* Radioコンポーネントを縦並びにする */
#my_radio .gr-radio-group {
  display: flex;
  flex-direction: column;
}
"""

with gr.Blocks(css=css_code) as demo:
    gr.Markdown("# G検定 模擬試験")

    # === 状態を保持する変数 ===
    current_index = gr.State(0)
    score = gr.State(0)

    # === 初期値設定 ===
    initial_question = f"Q1: {questions_list[0]['question']}"
    initial_options = questions_list[0]["options"]

    # === UIコンポーネント定義 ===
    question_text = gr.Markdown(value=initial_question)
    # elem_id="my_radio" を指定してカスタムCSSを当てる
    radio = gr.Radio(
        choices=initial_options,
        label="選択肢",
        value=None,
        elem_id="my_radio"
    )
    feedback_text = gr.Markdown()
    score_text = gr.Markdown("Score: 0")

    with gr.Row():
        submit_btn = gr.Button("回答を送信")
        next_btn = gr.Button("次の問題")

    # --- 回答送信ボタン ---
    def on_submit(selected, current_index, score):
        feedback, new_score = submit_answer(selected, current_index, score)
        return feedback, new_score, f"Score: {new_score}"

    submit_btn.click(
        fn=on_submit,
        inputs=[radio, current_index, score],
        outputs=[feedback_text, score, score_text]
    )

    # --- 次の問題ボタン ---
    def on_next(current_index):
        return next_question(current_index)

    # on_next の戻り値は [new_index, question_text, radio_update, feedback_reset]
    next_btn.click(
        fn=on_next,
        inputs=[current_index],
        outputs=[current_index, question_text, radio, feedback_text]
    )

    demo.launch()

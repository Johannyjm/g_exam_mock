import pandas as pd
import gradio as gr

# CSVファイルの読み込み
# ※ CSVファイルは data/ フォルダ内に配置してください
df = pd.read_csv("data/g_exam_questions.csv")

# CSVのカラム名に合わせて調整してください
# ここでは "問題", "選択肢", "回答" というカラム名を仮定
def process_options(options_str):
    # 選択肢がカンマ区切りの場合にリストへ変換（前後の空白も除去）
    return [opt.strip() for opt in options_str.split(",")]

# 各行のデータを辞書形式に変換し、リストに格納
questions_list = []
for _, row in df.iterrows():
    question = row["問題"]
    options = process_options(row["選択肢"])
    answer = row["回答"]
    questions_list.append({
        "question": question,
        "options": options,
        "answer": answer
    })

def submit_answer(selected, current_index, score):
    """
    ユーザーが選択した回答と正解を比較し、
    フィードバックメッセージとスコアを更新する。
    """
    if current_index < len(questions_list):
        correct = questions_list[current_index]["answer"]
        if selected == correct:
            score += 1
            feedback = "正解！"
        else:
            feedback = f"不正解。正しい答えは: {correct}"
    else:
        feedback = "試験は終了しています。"
    return feedback, score

def next_question(current_index):
    """
    現在の問題インデックスをインクリメントし、
    次の問題のテキストと選択肢を返す。
    """
    current_index += 1
    if current_index < len(questions_list):
        q = questions_list[current_index]
        question_text = f"Q{current_index+1}: {q['question']}"
        options = q["options"]
    else:
        question_text = "試験終了！お疲れさまでした。"
        options = []
    # 第4要素はラジオボタンの初期値（None）を返すためのもの
    return current_index, question_text, options, None

# Gradio インターフェース作成
with gr.Blocks() as demo:
    gr.Markdown("# G検定 模擬試験")
    
    # 状態を保持する変数：現在の問題番号、スコア
    current_index = gr.State(0)
    score = gr.State(0)
    
    # UIコンポーネントの定義
    question_text = gr.Markdown()
    radio = gr.Radio(choices=[], label="選択肢")
    feedback_text = gr.Markdown()
    score_text = gr.Markdown("Score: 0")
    
    with gr.Row():
        submit_btn = gr.Button("回答を送信")
        next_btn = gr.Button("次の問題")
    
    # 初回の問題を読み込み
    def load_first_question():
        q = questions_list[0]
        return f"Q1: {q['question']}", q["options"], None
    init_q, init_options, init_val = load_first_question()
    question_text.update(value=init_q)
    radio.update(choices=init_options, value=init_val)
    
    # 回答送信時の処理
    def on_submit(selected, current_index, score):
        feedback, new_score = submit_answer(selected, current_index, score)
        return feedback, new_score, f"Score: {new_score}"
    
    submit_btn.click(
        on_submit,
        inputs=[radio, current_index, score],
        outputs=[feedback_text, score, score_text]
    )
    
    # 次の問題へ進む処理
    def on_next(current_index):
        new_index, q_text, options, new_radio_val = next_question(current_index)
        return new_index, q_text, options, new_radio_val, ""
    
    next_btn.click(
        on_next,
        inputs=[current_index],
        outputs=[current_index, question_text, radio, radio, feedback_text]
    )
    
demo.launch()

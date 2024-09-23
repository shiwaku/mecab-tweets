import MeCab
from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt
import csv

# MeCabの辞書パスを指定
mecab = MeCab.Tagger('-d "C:/Program Files (x86)/MeCab/dic/ipadic"')

# 除外したい単語（ストップワード）のリスト
stop_words = {"RT", ":", "@", "#", "よう", "さん", "そう", "こと", "ん", "これ", "ため", "の", "中", "明日", "今日", 
              "人", "日本", "日", "目", "令", "和", "さ", "久しぶり", "お", "もの", "あと", "ところ", "楽しみ", "こちら", "とき", "どこ", "感じ", "ほう"}

# 相対パスでのファイルの指定（例: ./input.txt, ./output/output.png）
input_file = 'tweets_text.txt'
wordcloud_output = 'tweets_text.png'
csv_output = 'tweets_text.csv'

# テキストファイルを相対パスで読み込む
with open(input_file, 'r', encoding='utf-8') as file:
    text = file.read()

# 形態素解析を実行
parsed_text = mecab.parse(text)

# 名詞だけを抽出し、ストップワードを除外
words = []
for line in parsed_text.splitlines():
    if "名詞" in line:
        word = line.split("\t")[0]
        if word not in stop_words:  # ストップワードを除外
            words.append(word)

# スペースで区切った形で単語を結合
word_chain = " ".join(words)

# ワードクラウドを生成（wordsが空でない場合にのみ実行）
if words:
    wordcloud = WordCloud(font_path="C:/Windows/Fonts/msgothic.ttc", background_color="white", width=800, height=400).generate(word_chain)

    # ワードクラウドを相対パスで保存
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(wordcloud_output, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"ワードクラウド画像を '{wordcloud_output}' に保存しました。")
else:
    print("名詞が抽出されず、ワードクラウドを生成できませんでした。")

# キーワードの出現回数を集計し、出現回数でソート
word_counts = Counter(words)
sorted_word_counts = word_counts.most_common()  # 出現回数でソート

# キーワードと出現回数をCSVに保存（相対パスで保存）
with open(csv_output, "w", newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["キーワード", "出現回数"])  # ヘッダー行の書き込み
    writer.writerows(sorted_word_counts)  # 出現回数でソートされたキーワードを保存

print(f"キーワードの頻度を '{csv_output}' に保存しました。")

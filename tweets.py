import json
import re

# tweets.js ファイルを読み込み
with open('tweets.js', 'r', encoding='utf-8') as file:
    # 'window.YTD.tweets.part0 = ' の部分を削除し、JSONデータのみを取得
    data = file.read().strip().replace('window.YTD.tweets.part0 = ', '')

    # JSONデータをパース
    try:
        tweets = json.loads(data)
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        print("tweets.js ファイルの内容を確認してください。")
        exit()

# ツイート内容をテキストファイルに書き込む
with open('tweets_text.txt', 'w', encoding='utf-8') as output_file:
    for tweet in tweets:
        # 返信ツイートは除外する
        if 'in_reply_to_status_id' not in tweet['tweet'] or tweet['tweet']['in_reply_to_status_id'] is None:
            # 各ツイートの本文を取得
            tweet_text = tweet['tweet']['full_text']

            # URLを正規表現で除外
            tweet_text = re.sub(r'http[s]?://\S+', '', tweet_text)

            output_file.write(tweet_text + '\n\n')  # 各ツイートを改行して区切る

print("返信とURLを除外したツイート内容をテキストファイルに出力しました。")

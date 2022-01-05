import pandas as pd
import numpy as np
from mlp_lib import MLP


def read_vaccine(file):
    df = pd.read_csv('vaccinations_in_the_us.csv', header=2, usecols=['Date Type', 'Date', 'Daily Count People Receiving Dose 1', 'People Receiving 1 or More Doses Cumulative'])
    df = df[df['Date Type'] == "Admin"]
    # all date   2020 12 14 to 2021 10 31   
    return df["Daily Count People Receiving Dose 1"], df['People Receiving 1 or More Doses Cumulative']

def read_twitter_features(file):
    df = pd.read_csv(file, header=0)
    sentiment140 =  df[['sentiment140','n', 'retweet', 'favorite', 'followers', 'friends', 'user_favorite']][13:]
    textblob2 = df[['textblob2','n', 'retweet', 'favorite', 'followers', 'friends', 'user_favorite']][13:]
    vader = df[['vader','n', 'retweet', 'favorite', 'followers', 'friends', 'user_favorite']][13:]
    return sentiment140, textblob2, vader

def predict(model, sentiment140, textblob2, vader, result, result_type_str, percent_str):
    # sentiment 140
    model.predict(sentiment140, result, percent_str + result_type_str + "_sentiment140")
    model.predict(textblob2, result,  percent_str + result_type_str + "_textblob2")
    model.predict(vader, result,  percent_str + result_type_str + "_vader")


if __name__ == "__main__":
    daily_count_df, cumulative_count_df = read_vaccine('vaccinations_in_the_us.csv')
    daily_result = np.array(daily_count_df)
    cumulative_result = np.array(cumulative_count_df)


    # 10% twitter feature
    twitter_feature_file = "twitterfeatures_10.csv"
    percent_str = "10percent_"
    # 5% twitter feature
    # twitter_feature_file = "twitterfeatures_5.csv"
    # percent_str = "5percent_"
    sentiment140, textblob2, vader = read_twitter_features(twitter_feature_file)
    mlp = MLP()
    predict(mlp, sentiment140, textblob2, vader, daily_result, "daily_result", percent_str)
    predict(mlp, sentiment140, textblob2, vader, cumulative_result, "cumulative_result", percent_str)



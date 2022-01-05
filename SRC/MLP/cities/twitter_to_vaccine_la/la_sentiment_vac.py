import numpy as np
import pandas as pd
from mlp_lib import MLP

def read_vaccine(file):
    df = pd.read_csv(file, header=0, usecols=['Series_Complete_Yes', 'Series_Complete_12Plus', 'Series_Complete_18Plus', 'Series_Complete_65Plus','sentiment140', 'n'])
    return df['Series_Complete_Yes'][13:335], df[['sentiment140','n']][13:335]


if __name__ == "__main__":
    city = "la_city_features.csv"
    vaccine_df, sentiment_df = read_vaccine(city)
    #print(vaccine_df)
    result_vaccine = np.array(vaccine_df)
    mlp = MLP()
    mlp.predict(sentiment_df, result_vaccine, "_la_sentiment140_to_vaccine")


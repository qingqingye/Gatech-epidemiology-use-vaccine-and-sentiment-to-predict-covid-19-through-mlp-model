import numpy as np
import pandas as pd
from mlp_lib import MLP

def read_vaccine(file):
    df = pd.read_csv(file, header=0, usecols=['Series_Complete_Yes', 'Series_Complete_12Plus', 'Series_Complete_18Plus', 'Series_Complete_65Plus'])
    return df[13:335]

def read_death_cases(death_file, case_file):
    df_death = pd.read_csv("data_table_for_daily_death_trends__the_united_states.csv", header=2, usecols=["New Deaths", "Date"])
    # choose data from 2020 12 14 to 2021 10 31
    df_death_new = df_death["New Deaths"][:322][::-1]
    result_death = np.array(df_death_new)

    df_case = pd.read_csv("data_table_for_daily_case_trends__the_united_states.csv", header=2,
                           usecols=["New Cases", "Date"])
    df_case_new = df_case["New Cases"][:322][::-1]
    result_cases = np.array(df_case_new)
    return result_death, result_cases


if __name__ == "__main__":
    cities_files = ["la_city_features.csv", "ny_city_features.csv", "pho_city_features.csv"]
    for city in cities_files:
        vaccine_df = read_vaccine(city)
        #print(vaccine_df)
        result_death, result_cases = read_death_cases("data_table_for_daily_death_trends__the_united_states.csv", "data_table_for_daily_case_trends__the_united_states.csv")
        mlp = MLP()
        mlp.predict(vaccine_df, result_death, city + "_vaccine_to_death")
        mlp.predict(vaccine_df, result_cases, city + "_vaccine_to_cases")



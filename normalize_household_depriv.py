import pandas as pd

import plotly.express as px
import sys



def read_csv(data_file):

    df = pd.read_csv(data_file, header=[0])
    # Flatten the multi-index columns into year-yes, year-no, year-total

    print("---- dataframe loaded:")

    print(df.head())
    
    return df


def cal_pct(df):
    # Calculate total count for all groups and the households having 3 or more dimensions of deprivation.
    df2 = df[(df['Household deprivation (6 categories) Code'] >= 3)] # depriv in at least 2 dimension 
    
    
    all_counts = df.groupby('Lower layer Super Output Areas Code')['Observation'].sum().reset_index()
    all_counts.rename(columns={'Observation': 'Total'}, inplace=True)
    print(all_counts)
    df2_counts = df2.groupby('Lower layer Super Output Areas Code')['Observation'].sum().reset_index()
    print(df2_counts)
    # Merge total counts back to the combined DataFrame
    all_counts = all_counts.merge(df2_counts, on='Lower layer Super Output Areas Code')
    print(all_counts)

    # Calculate percentage
    all_counts['Percentage'] = (all_counts['Observation'] / all_counts['Total']) * 100


    # Sort the final DataFrame for better readability
    all_counts = all_counts.sort_values(by=['Lower layer Super Output Areas Code']).reset_index(drop=True)

    return all_counts


if __name__ == "__main__":
    DATA_FILE='./TS011-2021-6-filtered-2024-12-13T13_41_01Z.csv'

    df = read_csv(DATA_FILE)

    filtered_df = df[(df['Household deprivation (6 categories) Code'] == -8) & (df['Observation'] != 0)]
    print("----")
    print(filtered_df)
    

    df = df[(df['Household deprivation (6 categories) Code'] != -8)]

    df = cal_pct(df)
    print("Percentage of household deprived in 3 or more dimensions")
    print(df)
    df.to_csv("./pct_household_depriv_3_or_more_dimension.csv")


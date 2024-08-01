"""Python script with functions for data exploration"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List

def explore_cardinality(df:pd.DataFrame, categorical_columns:List, unique_value_threshold = 10):
    
    """Docstring: Perform data exploration for categorical columns.This function will return the unique values, number of unique values, and frequency of unique values in each column.
    It will also return the countplot and value_counts plot of each column 

    Parameters:
            df: pandas dataframe
            categorical_columns: list of categorical columns
            unique_value_threshold: set the number of values to show, it will only return the plots and unique values of columns with nunique less than this value         
    """

    for column in categorical_columns:

        plt.figure()

        print(column)

        num_unique = df[column].nunique()

        print(f'Number of unique values in {column}: {num_unique}')

        if num_unique <= unique_value_threshold:

            print(f'Unique values in {column}: {df[column].unique().tolist()}')
            print(f'Frequency of values in {column}: {df[column].value_counts(normalize = True)}')

            _, ax = plt.subplots(1,2)

            sns.countplot(data = df, y = column, ax = ax[0], palette = 'coolwarm')

            df[column].value_counts(normalize = True).plot.barh(color = ['blue', 'red'])

            plt.tight_layout();  

        print('_________________________________________________________________________________')


def explore_distribution(df:pd.DataFrame, numerical_columns:List):
    
    """Docstring: Perform data exploration for numerical columns.
    It will also return the histogram, kde and box plot of each column 

    Parameters:
            df: pandas dataframe
            numerical_columns: list of numerical columns
    """
    
    for column in numerical_columns:
    
        _, ax = plt.subplots(1,2)

        sns.histplot(data = df, x = column, color = 'purple', kde = True, ax = ax[0])

        sns.boxplot(y = df[column], ax = ax[1], color = 'purple')

        plt.tight_layout()

def bivariate_date_num(df:pd.DataFrame, time_type:str, date_columns:List, numerical_columns:List):
        
    """Docstring: Perform bivariate data exploration between numerical and date columns.
    It will also return the median and mean lineplot each column 

    Parameters:
            df: pandas dataframe
            time_type: values over time, e.g, hourly,daily, monthly,etc, valid values are ['h', 'm', 'd', 'y']
            date_columns: list of date columns
            numerical_columns: list of numerical columns
    """

    for date_column in date_columns:
        
        df[date_column] = pd.to_datetime(df[date_column])
        
        df_temp = df.set_index(date_column)
        
        resampled_data = df_temp.resample(time_type)
        
        for num_column in numerical_columns:
            
            mean_resampled = resampled_data[[num_column]].mean()
            median_resampled = resampled_data[[num_column]].median()
            
            plt.figure()
            
            sns.lineplot(data = mean_resampled, x = date_column, y = num_column)
            plt.title(f'Mean {num_column} over time')
            plt.xticks(rotation = 90)
            
            plt.figure()
            sns.lineplot(data = median_resampled, x = date_column, y = num_column)
            plt.title(f'Median {num_column} over time')
            plt.xticks(rotation = 90);


def correlation(df:pd.DataFrame, method:str='pearson'):
    
    """Docstring: Plot correlation between columns

    Parameters:
            df: pandas dataframe
            method: values are pearson, spearman
    """

    corr = df.corr(method = method)

    plt.figure(figsize = (7,7))

    sns.heatmap(corr, annot = True)
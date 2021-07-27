import pandas as pd
import re


# Find a pattern in the lines of a big text file and counts them
def count_pattern_bigfile(path, pattern):
    """
    This function read line by line the document in path (therefore is suitable for big documents),
    finds the string in the variable pattern and counts show many times it appears.

    Args:
        path (str): document's path
        pattern(str or regex): pattern that wants to be counted

    Returns:
        String describing the times that the pattern has been found
    """
    # Opening the file for read
    with open(path, 'r') as f:

        # Setting the counter to 0
        counter = 0
        pattern_com = re.compile(pattern)

        # reading every line and if it finds the pattern add 1 to the counter
        for line in f:
            if re.search(pattern_com, line):
                counter += 1

    # returning the count of the pattern
    return "The pattern {} appears {} times.".format(pattern, counter)


# Inner join with df_ratings
def join_df(df_left, df_right, column_to_add, left_key='pollster', rating_key='Pollster'):
    """This function, makes an inner join between a dataframe left
     and df_right an only adds 1 column from the right dataframe

    Args:
        df_left (dataframe): dataframe in the left (the one that will keep all the columns)
        df_right (dataframe): dataframe on the right (the one that will only keep 1 column)
        left_key (str): key of dataframe join
        rating_key (str): key to join df_ratings with
        column_to_add (str): column to add from df_ratings

    Returns:
        dataframe with inner join between both dataframes and all the columns from the left dataframe
         and 1 only form the right one
         """
    # pd.merge takes to dataframe and make an inner join by default
    df_new = pd.merge(df_left, df_right[[rating_key, column_to_add]],
                      left_on=left_key, right_on=rating_key)
    # Dropping the key column
    del df_new[rating_key]
    return df_new


def get_percentage(df, column_population, column_percentage):
    """This function takes a dataframe and calculates the number of individuals from a population, given
    a percentage

    Args:
        df (dataframe): the dataframe that contains the information
        column_population (str): the column that contains the population
        column_percentage (str): the column that contains the percentage

    Returns:
        Dataframe with the number of people of the population in the percentage column

    """
    total = df[column_population] * df[column_percentage] / 100
    return total


def col_sum(df, table_name, column):
    """This function takes as argument one dataframe and returns the sum of the column in column. It also needs
    the name for this table or dataframe

    Args:
        df: input dataframe
        table_name: name of the table
        column: column you want to add

    Returns:
        string with indicating the name of teh column added  up, the name of the dataframe and the total of that column
    """
    # Adding the column up
    total = df[column].sum()
    return 'The sum of the column {} for the table {} is: {}'.format(column, table_name, total)


def replace_regex(df, column, pattern, replace_with=''):
    """
    This function takes a df as arguments and replaces with the regex expression in pattern the column defined
    in the variable column with the string defined in replace_with
    Args:
        df (dataframe): a dataframe
        column (str): a column with string
        pattern (str): regex expression
        replace_with (str): what do you want to replace it with (by default nothing)

    Returns:
        pandas series with the column with character replaced

    """
    new_col = df[column].str.replace(pattern, replace_with, regex=True)
    return new_col


def num_grades(row):
    """
    This function get as input the letters A, B, C , D or F and it returns
    1, 0.5, 0, -0.5 or -1 respectively
    Args:
        row (str): letters A, B, C , D or F

    Returns:
        1, 0.5, 0, -0.5 or -1

    """
    if row == 'A':
        return 1
    if row == 'B':
        return 0.5
    if row == 'C':
        return 0
    if row == 'D':
        return -0.5
    if row == 'F':
        return -1

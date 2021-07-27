import pandas as pd
from exploration_manipulation import join_df, replace_regex, num_grades

# Defining paths to data files
path_approval = "data/covid_approval_polls.csv"
path_concern = "data/covid_concern_polls.csv"
path_ratings = "data/pollster_ratings.xlsx"

# Loading in dataframes
df_ratings = pd.read_excel(path_ratings)
df_approval = pd.read_csv(path_approval)
df_concern = pd.read_csv(path_concern, engine='openpyxl')

# CREATION OF APPROVAL POLLS AND CONCERN POLLS
# Joining with df_rating first
approval_polls = join_df(df_left=df_approval, df_right=df_ratings,column_to_add='Banned by 538')
concern_polls = join_df(df_left=df_concern, df_right=df_ratings, column_to_add='Banned by 538')

# Filtering by the required criteria
approval_polls = approval_polls[(approval_polls['tracking'] == False) & (approval_polls['Banned by 538'] == 'no')]
concern_polls = concern_polls[(concern_polls['tracking'] == False) & (concern_polls['Banned by 538'] == 'no')]

# Concern with grades
concern_grade = join_df(df_left=concern_polls, df_right=df_ratings, column_to_add='538 Grade')
concern_grade['538 Grade'] = replace_regex(df=concern_grade, column='538 Grade', pattern='(.)/|-')

# Concern with numeric grades
# First we need to add the column from rating 'Predictive    Plus-Minus'
concern_numgrade = join_df(df_left=concern_grade, df_right=df_ratings, column_to_add='Predictive    Plus-Minus')

# Now with the function num_grades, we get teh numeric value of the the column 538 Grade and we
# add Predictive    Plus-Minus to create the column num_grade (numeric grade)
concern_numgrade['num_grade'] = concern_numgrade['538 Grade'].apply(num_grades) + concern_numgrade[
    'Predictive    Plus-Minus']

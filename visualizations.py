import matplotlib.pyplot as plt
from exploration_manipulation import get_percentage


def graph_approve_party(df):
    """
    This function takes the table approval_polls and represents how many people of each party has approved
    or disapprove to the questions that contains "Trump" and "coronavirus", in a staked bar plot

   Args:
       df (dataframe): dataframe containing the information from covid_approval_polls.csv

   """
    # First we filter approval_polls
    df_trcor = df[
        (df['text'].str.contains('Trump')) & (df['text'].str.contains('coronavirus'))]

    # Generating the number of persons that approved or disapproved by multiplying sample_size with the percentage of
    # people that approved / disapproved
    df_trcor['num_approve'] = get_percentage(df_trcor, column_population='sample_size',
                                             column_percentage='approve')
    df_trcor['num_disapprove'] = get_percentage(df_trcor, column_population='sample_size',
                                                column_percentage='disapprove')

    # Now we group by party and sum to get the total of people that approved or disapproved
    df_trcor_sum = df_trcor.groupby('party').sum().reset_index()

    # Setting fig and ax, and defining size
    fig, ax = plt.subplots(figsize=(14, 8))

    # This line will prevent matplotlib to show data in scientific notation
    plt.ticklabel_format(style='plain')

    # Approve barplot
    plt.bar(df_trcor_sum['party'], df_trcor_sum['num_approve'], color='mediumpurple', label='Approve')

    # Disapprove barplot. Note bottom=df_trcor_sum['num_approve'] to define the stacked barplot format
    plt.bar(df_trcor_sum['party'], df_trcor_sum['num_disapprove'], bottom=df_trcor_sum['num_approve'], color='coral',
            label='Disapprove')

    # Setting labels up
    ax.set_xlabel('Party')
    ax.set_ylabel('Number of people')

    # Showing legends
    ax.legend()
    plt.show()


def concern_plot(df, df_filter, columns_concern, title='', percen=False, column_population='sample_size'):
    """
    This function plots bar plots based on a series of columns that contains data in percentage of a population
    that need to be defined in another column. The bars represent the total amount of people (count or percentage) of
    that column in relation to the population
    Args:
        df (dataframe): dataframe that contains at least a column with the population and other columns with
        the percentages of that population
        df_filter (panda dataframe filter): a filter for a dataframe in pandas for exampl df[df[column1] == 1].
        columns_concern (list): list with the name of the columns with the percentages
        title (str): title of teh chart
        percen (boolean): If True results are represented in percentage format
        column_population (string): the column that  contains the population


    """
    # Filtering the dataframe by subject
    df_filtered = df[df_filter]

    fig, ax = plt.subplots(figsize=(14, 8))

    for i in columns_concern:
        total_columns = get_percentage(df_filtered, column_population=column_population, column_percentage=i).sum()
        if percen:
            total_columns = total_columns / df_filtered[column_population].sum()

        plt.bar(x=i, height=total_columns)

    # This loop below add labels on top of teh bars, if percen is true shows it in percentage
    for p in ax.patches:
        width = p.get_width()
        height = p.get_height()
        x, y = p.get_xy()
        if percen:
            ax.annotate(f'{height:.0%}', (x + width / 2, y + height * 1.02), ha='center')
        else:
            ax.annotate(f'{height:0}', (x + width / 2, y + height * 1.02), ha='center')
    # Setting labels up
    ax.set_xlabel('How concern people are')

    if percen:
        ax.set_ylabel('Percentage of people %')
    else:
        ax.set_ylabel('Number of people')

    plt.title(title)
    plt.show()


def concern_grades(df):
    """
    This function represents the count by grades of the dataframe concern_grades
    Args:
        df (dataframe): dataframe concern_grades

    """
    # Grouping by and counting
    bar_size = df.groupby('538 Grade').size().reset_index()

    # Defining fig. ax and size
    fig, ax = plt.subplots(figsize=(14, 8))

    # Bar plot for first column of how concern people are
    plt.bar(x=bar_size['538 Grade'], height=bar_size[0])

    # Setting labels up
    ax.set_xlabel('Grade of interviews')
    ax.set_ylabel('Count')
    plt.show()


def interviews_high_rating(df):
    """
    This function takes a dataframe as argument (in this case should be concern_numgrade or a dataframe with the same
    format) and returns an histogram with the numeric grades higher or equal to 1.5
    Args:
        df (dataframe):concern_numgrade or a dataframe with the same format

    """
    # filtering dataframe by grades equal or higher than 1.5
    df_filtered = df[df['num_grade'] >= 1.5]

    fig, ax = plt.subplots(figsize=(8, 8))

    # Bar plot for first column of how concern people are
    plt.hist(df_filtered['num_grade'])

    # Setting labels up
    ax.set_xlabel('Numeric grade of interviews bigger or equal to 1.5')
    ax.set_ylabel('Count')
    plt.show()

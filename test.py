import unittest
import pandas as pd
from exploration_manipulation import count_pattern_bigfile, join_df, get_percentage, col_sum, replace_regex, num_grades


# Testing functions in the exploration_manipulation module


class TestExpMan(unittest.TestCase):

    # Setting ups variables and dataframes
    @classmethod
    def setUpClass(cls):
        print("Loading path")
        cls._path_approval = "data/covid_approval_polls.csv"
        cls._path_concern = "data/covid_concern_polls.csv"
        cls._path_ratings = "data/pollster_ratings.xlsx"

        cls._test_approval = pd.read_csv('data/test_approval.csv')
        cls._test_concern = pd.read_csv('data/test_concern.csv')
        cls._test_ratings = pd.read_excel("data/pollster_ratings.xlsx")

        cls._test_concern_grade = pd.read_csv('data/test_concern_grade.csv')
        cls._test_concern_numgrade = pd.read_csv('data/test_concern_numgrade.csv')

    # Testing count_pattern_bigfile
    def test_count_pattern(self):
        print("Starting test_unique_counts")
        self.assertEqual(count_pattern_bigfile(path=self._path_approval, pattern="Huffington Post"),
                         'The pattern Huffington Post appears 112 times.')
        self.assertEqual(count_pattern_bigfile(path=self._path_approval,
                                               pattern="https?:\/\/.*\.pdf[\s]"),
                         'The pattern https?:\\/\\/.*\\.pdf[\\s] appears 1304 times.')
        self.assertEqual(count_pattern_bigfile(path=self._path_concern, pattern="Huffington Post"),
                         'The pattern Huffington Post appears 29 times.')
        self.assertEqual(count_pattern_bigfile(path=self._path_concern, pattern="https?:\/\/.*\.pdf[\s]"),
                         'The pattern https?:\\/\\/.*\\.pdf[\\s] appears 461 times.')

    # As I am not sure how to test a dataframe output I am just going to compare a random line
    def test_join_df(self):
        print("Starting test_join_df")
        # Loading info from original csv files
        df_approval = pd.read_csv(self._path_approval)
        df_concern = pd.read_csv(self._path_concern)
        df_ratings = pd.read_excel(self._path_ratings)

        # Joining and filtering, to transform them
        approval_polls = join_df(df_left=df_approval, df_right=df_ratings, column_to_add='Banned by 538')
        approval_polls = approval_polls[
            (approval_polls['tracking'] == False) & (approval_polls['Banned by 538'] == 'no')]
        concern_polls = join_df(df_left=df_concern, df_right=df_ratings, column_to_add='Banned by 538')
        concern_polls = concern_polls[(concern_polls['tracking'] == False) & (concern_polls['Banned by 538'] == 'no')]

        # Testing the line 47
        self.assertEqual(approval_polls.iloc[47, ].tolist(), self._test_approval.iloc[47, ].tolist())
        self.assertEqual(concern_polls.iloc[47, ].tolist(), self._test_concern.iloc[47, ].tolist())

        # Testing first line
        self.assertEqual(approval_polls.iloc[0, ].tolist(), self._test_approval.iloc[0, ].tolist())
        self.assertEqual(concern_polls.iloc[0, ].tolist(), self._test_concern.iloc[0, ].tolist())

    # Testing first 100 element of get_percentage output
    def test_get_percentage(self):
        print("Starting test_get_percentage")
        # Loading test data and converting it to pandas series
        test_percentage = pd.read_csv('data/test_percentage.csv')
        test_percentage = test_percentage.squeeze()
        # Getting function output
        percentage1 = get_percentage(self._test_approval, column_population='sample_size', column_percentage='approve')
        self.assertEqual(test_percentage.values.tolist()[0:100], percentage1.values.tolist()[0:100])

    # Testing col_sums
    def test_col_sum(self):
        test_output = 'The sum of the column sample_size for the table concern_polls is: 1342211'
        col_sum_output = col_sum(df=self._test_concern, table_name='concern_polls', column='sample_size')
        self.assertEqual(col_sum_output, test_output)

    # Testing test_replace
    def test_replace(self):
        print("Starting test_replace")
        # Loading test data and converting it to pandas series
        test_replace = pd.read_csv('data/test_replace.csv')
        test_replace = test_replace.squeeze()
        # Getting function output
        output_replace = replace_regex(df=self._test_concern_grade, column='538 Grade', pattern='(.)/|-')
        self.assertEqual(test_replace.values.tolist(), output_replace.values.tolist())

    def test_num_grades(self):
        print("Starting test_num_grades")
        # Loading test data and converting it to pandas series
        test_num_grades = pd.read_csv('data/test_num_grades.csv')
        test_num_grades = test_num_grades.squeeze()
        # Getting function output
        numgrade_output = self._test_concern_numgrade['538 Grade'].apply(num_grades)
        self.assertEqual(test_num_grades.values.tolist(), numgrade_output.values.tolist())


class TestVisualizations(unittest.TestCase):

    # Setting ups variables and dataframes
    @classmethod
    def setUpClass(cls):
        print("Loading path")
        cls._path_approval = "data/covid_approval_polls.csv"
        cls._path_concern = "data/covid_concern_polls.csv"
        cls._path_ratings = "data/pollster_ratings.xlsx"

        cls._test_approval = pd.read_csv('data/test_approval.csv')
        cls._test_concern = pd.read_csv('data/test_concern.csv')
        cls._test_ratings = pd.read_excel("data/pollster_ratings.xlsx")

        cls._test_concern_grade = pd.read_csv('data/test_concern_grade.csv')
        cls._test_concern_numgrade = pd.read_csv('data/test_concern_numgrade.csv')


if __name__ == '__main__':
    unittest.main()

from cse163_utils import assert_equals
import data_cleaning as dc
import pandas as pd


def test_get_school_names():
    """
    This function tests the get_school_names function for correct output.
    """
    print("Testing get_school_names")
    test_df = pd.read_csv("test.csv")
    received = dc.get_school_names(test_df, 1, 1)
    expected = ["School 1", "School 2", "School 3"]
    assert_equals(expected, received)

    test_df2 = pd.read_csv("test2.csv")
    received = dc.get_school_names(test_df2, 2, 3)
    assert_equals(expected, received)


def test_get_school_data():
    """
    This function tests the get_school_data function for correct output.
    """
    print("Testing get_school_data")
    test_df = pd.read_csv("test3.csv")
    names = dc.get_school_names(test_df, 1, 1)
    stat = "test_stat"
    received = dc.get_school_data(test_df, names, stat)
    expected = [{"Year": 1, "School": "School 1", stat: 5}]
    assert_equals(expected, received)

    test_df2 = pd.read_csv("test.csv")
    names2 = dc.get_school_names(test_df, 1, 1)
    stat = "test_stat"
    received = dc.get_school_data(test_df2, names2, stat)
    expected = [{"Year": 1, "School": "School 1", stat: 5},
                {"Year": 2, "School": "School 1", stat: 7},
                {"Year": 3, "School": "School 1", stat: 6},
                {"Year": 1, "School": "School 2", stat: 4},
                {"Year": 2, "School": "School 2", stat: 5},
                {"Year": 3, "School": "School 2", stat: 2},
                {"Year": 1, "School": "School 3", stat: 3},
                {"Year": 2, "School": "School 3", stat: 4},
                {"Year": 3, "School": "School 3", stat: 1}]


def main():
    """
    This function calls all test functions.
    """
    test_get_school_names()
    test_get_school_data()


if __name__ == "__main__":
    main()

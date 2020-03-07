import pandas as pd
import numpy as np


def get_all_names(applicants_names, admitted_names, grad_rate_names,
                  private_names):
    """
    Requires the list of applicant, admitted, grad_rate, and private fin_aid
    data names. Returns a list of all of the names of the schools we have
    data for.
    """
    all_names = set()
    for name in applicants_names:
        all_names.add(name)
    for name in admitted_names:
        all_names.add(name)
    for name in grad_rate_names:
        all_names.add(name)
    for name in private_names:
        all_names.add(name)
    all_names = sorted(all_names)
    return all_names


def create_dataframe(all_names):
    """
    Takes the list of all of the school names. Creates and returns the
    DataFrame with the MultiIndex. DataFrame is initialized with values
    being all zeros. Columns are the school (full) names. Row indexes are
    Year and Statistic.
    """
    years = [i for i in range(2001, 2019)]
    stats = ["admitted", "applicants", "grad_rate", "population", 
             "financial_aid", "public", "private"]
    pairs = list()
    for year in years:
        for stat in stats:
            pairs.append((year, stat))
    index = pd.MultiIndex.from_tuples(pairs, names=["Year", "Stat"])
    df = pd.DataFrame(np.zeros((126, 32)), index=index, columns=all_names)
    return df


def fill_in_table(df, data, name_of_stat):
    """
    Takes in the empty MultiIndex DataFrame, the statistic data dictionary and
    the name of the statistic that corresponds to the row index name in the
    DataFrame. Fills the DataFrame with the values from the dictionary.

    After running this function with all datasets, include
    < df.replace(0, np.nan, inplace=True) >
    to fill the remaining zeros with NaN.
    """
    for school in data:
        for year, stat in data[school]:
            df.loc[(year, name_of_stat), school] = stat


def is_public_or_private(df, all_names, public_names, private_names):
    """
    Takes the DataFrame, and the list of all school names, public school names,
    and private school names. Flags the school in the DataFrame according to
    its type. Creates 2 new row indexers to denote this.
    """
    for name in all_names:
        if name in public_names:
            df.loc["public", name] = 1
        else:
            df.loc["public", name] = 0
        if name in private_names:
            df.loc["private", name] = 1
        else:
            df.loc["private", name] = 0

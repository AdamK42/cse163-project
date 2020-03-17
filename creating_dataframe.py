# Name: Adam Klingler and Kayla Perez
# Description: Helper functions for creating our main dataframe.
import pandas as pd
import data_cleaning as dc


def read_data():
    """
    Reads all of the datasets into Pandas DataFrames and returns them all
    as a tuple.
    """
    applicants = pd.read_excel("datasets/total_applicants.xlsx", header=2)
    admitted = pd.read_excel("datasets/total_admitted.xlsx", header=2)
    grad_rate = pd.read_excel("datasets/graduation_rates.xlsx", header=2)
    student_pop = pd.read_excel("datasets/student_population.xlsx", header=2)
    public_fin = pd.read_excel("datasets/financial_aid_public.xlsx", header=2)
    private_fin = pd.read_excel("datasets/financial_aid_private.xlsx",
                                header=2)
    return (applicants, admitted, grad_rate, student_pop, public_fin,
            private_fin)


def get_names(dataframes):
    """
    Takes in the tuple of raw DataFrames. Returns a new tuple with each list of
    schools retrieved from the raw DataFrames.
    """
    applicants = dc.get_school_names(dataframes[0], 3, 2)
    admitted = dc.get_school_names(dataframes[1], 3, 2)
    grad_rate = dc.get_school_names(dataframes[2], 2, 6)
    student_pop = dc.get_school_names(dataframes[3], 2, 6)
    public_fin = dc.get_school_names(dataframes[4], 8, 33)
    private_fin = dc.get_school_names(dataframes[5], 8, 21)
    return (applicants, admitted, grad_rate, student_pop, public_fin,
            private_fin)


def get_dictionaries(dataframes, names):
    """
    Takes in the tuple of raw DataFrames and the tuple of school names. Returns
    a tuple of dictionaries for each DataFrame.
    """
    applicants = dc.get_school_data(dataframes[0], names[0], "applicants")
    admitted = dc.get_school_data(dataframes[1], names[1], "admitted")
    grad_rate = dc.get_school_data(dataframes[2], names[2], "grad_rate")
    student_pop = dc.get_school_data(dataframes[3], names[3], "population")
    public_fin = dc.get_school_data(dataframes[4], names[4], "fin_aid")
    private_fin = dc.get_school_data(dataframes[5], names[5], "fin_aid")
    return (applicants, admitted, grad_rate, student_pop, public_fin,
            private_fin)


def create_dataframe():
    """
    Creates and returns a new DataFrame consisting of all of our orignial
    datasets.
    """
    raw_dataframes = read_data()
    school_names = get_names(raw_dataframes)
    dictionaries = get_dictionaries(raw_dataframes, school_names)

    applicant_df = pd.DataFrame(dictionaries[0])
    admitted_df = pd.DataFrame(dictionaries[1])
    grad_df = pd.DataFrame(dictionaries[2])
    pop_df = pd.DataFrame(dictionaries[3])
    public_df = pd.DataFrame(dictionaries[4])
    private_df = pd.DataFrame(dictionaries[5])

    df = applicant_df.copy()
    df = df.merge(grad_df, how="outer", on=["School", "Year"])
    df = df.merge(pop_df, how="outer", on=["School", "Year"])
    df = df.merge(admitted_df, how="outer", on=["School", "Year"])
    df = df.merge(private_df, how="outer", on=["School", "Year"])
    df = df.merge(public_df, how="outer", on=["School", "Year"],
                  suffixes=["_private", "_public"])
    df["percent_accepted"] = (df["admitted"] / df["applicants"]) * 100
    return df

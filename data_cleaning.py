def get_school_names(df):
    """
    Takes a school data DataFrame. Returns a list of the schools in the DataFrame.
    """
    col_names = list(df.columns)
    schools = list()
    for name in col_names[1:]:
        words = name.split()
        school_list = words[3:len(words) - 2]
        school = " ".join(school_list)
        schools.append(school)
    return schools


def get_school_data(df, school_names):
    """
    Takes a school data dataframe and a list of school names. Returns a
    dictionary where the keys are school names and the values are lists of
    tuples (year, data number)
    """
    statistic_data = dict()
    for i in range(1, len(school_names)):
        numbers = df.loc[:, df.columns[i]]
        years = df.loc[:, "Time"]
        school_data = list(zip(years, numbers))
        statistic_data[school_names[i]] = school_data
    return statistic_data

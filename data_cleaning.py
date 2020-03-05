def get_school_names(df):
    """
    Takes a dataframe. Returns a list of the schools in the dataframe.
    """
    col_names = list(df.columns)
    schools = list()
    for name in col_names[1:]:
        # so we don't even need regexes???
        # name = re.sub(r"#+", "", name) # removes tag
        words = name.split()  # splits into individual words
        school_list = words[3:len(words) - 2]  # gets a list of the school name
        school = " ".join(school_list)  # gets a string of the school name
        schools.append(school)
    return schools


def get_school_data(df, school_names):
    """
    Takes a school data dataframe and a list of school names. Returns a
    dictionary where the keys are school names and the values are lists of
    tuples (year, data number)
    """
    admitted_data = dict()
    for i in range(1, len(school_names)):
        numbers = df.loc[:, df.columns[i]]
        years = df.loc[:, "Time"]
        school_data = list(zip(years, numbers))
        admitted_data[school_names[i]] = school_data
    return admitted_data

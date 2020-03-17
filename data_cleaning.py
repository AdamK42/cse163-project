# Name: Adam Klingler and Kayla Perez
# Description: Helper functions for cleaning the data for the main dataframe.


def get_school_names(df, prefix_len, suffix_len):
    """
    Takes a school data DataFrame, prefix length, and suffix length.
    Returns a list of the schools in the DataFrame.
    """
    col_names = list(df.columns)
    schools = list()
    for name in col_names[1:]:
        words = name.split()
        school_list = words[prefix_len:len(words) - suffix_len]
        school = " ".join(school_list)
        schools.append(school)
    return schools


def get_school_data(df, school_names, stat_name):
    """
    Takes the raw DataFrame, the list of school names, and the name of the
    statistic. Returns a list of dictionaries with keys "School", "Year", and
    the given statistic name.
    """
    all_data = list()
    for i in range(len(df)):
        year = df.loc[i, "Time"]
        for j in range(len(school_names)):
            row = dict()
            row["Year"] = year
            row["School"] = school_names[j]
            row[stat_name] = df.loc[i, df.columns[j + 1]]
            all_data.append(row)
    return all_data

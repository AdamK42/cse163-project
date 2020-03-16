import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from creating_dataframe import create_dataframe, get_names, read_data


def plot_fit_line(data, ax, column, plot_title):
    """
    This takes in a dataframe data, plot axis ax, y-axis column, and plot title
    and plots a best fit line for data on ax, with x-axis of graduation rate
    and y-axis of column, and prints out the Pearson R coefficient for the
    plot.
    """
    xs = data["grad_rate"]
    ys = data[column]
    fit = np.polyfit(xs, ys, 1)

    x = np.arange(0, 100, 0.1)
    ax.plot(x, fit[0] * x + fit[1], color="#000000")
    ax.set_xbound(0, 100)
    ax.set_ybound(0, 100)
    r_coeff = pearsonr(xs, ys)[0]

    print(plot_title + " Pearson R: " + str(r_coeff))


def filter_schools(data, school_names):
    """
    This function takes in a dataframe data and a list of school names
    and returns a filtered dataframe with those schools.
    """
    is_school_type = data["School"].isin(school_names)
    bothell = "University of Washington-Bothell Campus"
    tacoma = "University of Washington-Tacoma Campus"
    not_satillite = (data["School"] != bothell) & (data["School"] != tacoma)
    filtered_school_data = data[is_school_type & not_satillite]
    return filtered_school_data


def filter_sufficient_data(data, column, threshold):
    """
    This function takes in a dataframe data, a filter column, and a threshold
    for their being enough data and returns a filtered dataframe with at least
    threshold number of datapoints in column.
    """
    filtered_data = data[["Year", "School", "grad_rate", column]]
    column_count = filtered_data.groupby("School")[column].count()
    # Number of data points for column by school
    has_enough_data_s = column_count >= threshold
    names_with_data = column_count[has_enough_data_s].index
    has_enough_data = filtered_data["School"].isin(names_with_data)
    filtered_data = filtered_data[has_enough_data]
    return filtered_data.dropna()


def get_names_lists():
    """
    Returns a tuple which contains the list of public schools (index 0) and
    the list of private schools (index 1).
    """
    data = read_data()
    names = get_names(data)
    return (names[4], names[5])


def get_mean_data(data, column):
    """
    Takes in a dataframe data and a column and returns a dataframe of schools
    with the mean value of that column and graduation rate.
    """
    return data.groupby("School")[column, "grad_rate"].mean().reset_index()


# Question 0: Competitiveness
def plot_grad_rate_vs_percent_accepted(data):
    """
    This function takes in the relavent dataframe data and produces a plot
    of graduation rate and percent accepted, along with printing the pearson
    R coefficient to the console.
    """
    filtered_data = filter_sufficient_data(data, "percent_accepted", 15)
    title = "Graduation Rate VS Percent Accepted- All Universites"
    ylabel = "Percent Accepted"
    save_file = "grad_rate_v_compet_all.png"

    plot_generic_graph(filtered_data, "percent_accepted", (title, ylabel),
                       (10, 10), save_file)


def plot_grad_rate_vs_percent_accepted_public(public_data):
    """
    This function takes in the relavent dataframe public_data and produces a
    plot of graduation rate and percent accepted for public schools, along with
    printing the pearson R coefficient to the console.
    """
    filtered_data = filter_sufficient_data(public_data, "percent_accepted", 15)
    title = "Graduation Rate VS Percent Accepted- Public Universites"
    ylabel = "Percent Accepted"
    save_file = "grad_rate_v_compet_pub.png"

    plot_generic_graph(filtered_data, "percent_accepted", (title, ylabel),
                       (8, 8), save_file)


def plot_grad_rate_vs_percent_accepted_private(private_data):
    """
    This function takes in the relavent dataframe private_data and produces a
    plot of graduation rate and percent accepted for private schools, along
    with printing the pearson R coefficient to the console.
    """
    filtered_data = filter_sufficient_data(private_data, "percent_accepted",
                                           15)
    title = "Graduation Rate VS Percent Accepted- Private Universites"
    ylabel = "Percent Accepted"
    save_file = "grad_rate_v_compet_priv.png"

    plot_generic_graph(filtered_data, "percent_accepted", (title, ylabel),
                       (8, 8), save_file)


def plot_average_grad_rate_vs_percent_accepted(data):
    """
    This function takes in the relavent dataframe data and produces a plot
    of average graduation rate and average percent accepted, along with
    printing the pearson R coefficient to the console.
    """
    filtered_data = filter_sufficient_data(data, "percent_accepted", 15)
    means = get_mean_data(filtered_data, "percent_accepted")

    # needed to drop a row that had a tiny grad rate due to missing data
    means = means.drop(0)
    means = means.dropna()
    title = "Average Graduation Rate vs Average Percent Accepted- All"\
            + " Universities"
    ylabel = "Percent Accepted"
    save_file = "av_grad_rate_v_compet_all"

    plot_generic_graph(means, "percent_accepted", (title, ylabel),
                       (8, 8), save_file)


def plot_average_grad_rate_vs_percent_accepted_public(public_data):
    """
    This function takes in the relavent dataframe public_data and produces a
    plot of average graduation rate and average percent accepted, along with
    printing the pearson R coefficient to the console.
    """
    filtered_data = filter_sufficient_data(public_data, "percent_accepted", 15)
    new_data = filtered_data[["Year", "School", "percent_accepted",
                              "grad_rate"]]
    means = get_mean_data(new_data, "percent_accepted")
    title = "Average Graduation Rate vs Average Percent Accepted- Public"\
            + " Universities"
    ylabel = "Percent Accepted"
    save_file = "av_grad_rate_v_compet_pub.png"

    plot_generic_graph(means, "percent_accepted", (title, ylabel),
                       (8, 8), save_file)


def plot_average_grad_rate_vs_percent_accepted_private(private_data):
    """
    This function takes in the relavent dataframe private_data and produces a
    plot of average graduation rate and average percent accepted, along with
    printing the pearson R coefficient to the console.
    """
    filtered_data = filter_sufficient_data(private_data, "percent_accepted",
                                           15)
    means = get_mean_data(filtered_data, "percent_accepted")
    title = "Average Graduation Rate vs Average Percent Accepted- Private"\
            + " Universities"
    ylabel = "Percent Accepted"
    save_file = "av_grad_rate_v_compet_priv.png"

    plot_generic_graph(means, "percent_accepted", (title, ylabel),
                       (8, 8), save_file)


# Question 1: Financial Aid
def get_fin_aid_data(data):
    """
    This function takes in the data and calculates the subset of data for
    the financial aid plotting.
    """
    short_df = data[["Year", "School", "population", "fin_aid_private",
                     "fin_aid_public", "grad_rate"]]
    short_df = short_df.dropna(thresh=5)
    short_df.fillna(0, inplace=True)
    short_df["fin_aid"] = np.abs(short_df["fin_aid_private"]
                                 - short_df["fin_aid_public"])
    short_df["fin_aid_ratio"] = (short_df["fin_aid"] /
                                 short_df["population"] * 100)

    # Some fin_aid_ratios higher than 100, doesn't make sense
    is_valid_fin_aid_ratio = short_df["fin_aid_ratio"] < 100
    short_df = short_df[is_valid_fin_aid_ratio]
    filtered = filter_sufficient_data(short_df, "fin_aid_ratio", 7)
    return filtered


def plot_grad_rate_vs_financial(data):
    """
    This function takes in the relavent dataframe data and produces a plot
    of graduation rate and financial aid ratio, along with printing the pearson
    R coefficient to the console.
    """
    title = "Graduation Rate VS Percentage of Students With Financial Aid- "\
            + "All Universities"
    ylabel = "Percentage of Students with Financial Aid"
    save_file = "grad_rate_v_fin_all.png"

    plot_generic_graph(data, "fin_aid_ratio", (title, ylabel), (10, 10),
                       save_file)


def plot_grad_rate_vs_financial_public(public_data):
    """
    This function takes in the relavent dataframe public_data and produces a
    plot of graduation rate and financial aid ratio for public schools, along
    with printing the pearson R coefficient to the console.
    """
    title = "Graduation Rate VS Percentage of Students With Financial Aid- "\
            + "Public Universities"
    ylabel = "Percentage of Students with Financial Aid"
    save_file = "grad_rate_v_fin_pub.png"

    plot_generic_graph(public_data, "fin_aid_ratio", (title, ylabel), (10, 10),
                       save_file)


def plot_grad_rate_vs_financial_private(private_data):
    """
    This function takes in the relavent dataframe private_data and produces a
    plot of graduation rate and financial aid ratio for private schools, along
    with printing the pearson R coefficient to the console.
    """
    title = "Graduation Rate VS Percentage of Students With Financial Aid- "\
            + "Private Universities"
    ylabel = "Percentage of Students with Financial Aid"
    save_file = "grad_rate_v_fin_priv.png"

    plot_generic_graph(private_data, "fin_aid_ratio", (title, ylabel),
                       (10, 10), save_file)


def plot_average_grad_rate_vs_financial(data):
    """
    This function takes in the relavent dataframe data and produces a plot
    of average graduation rate and average financial aid ratio, along with
    printing the pearson R coefficient to the console.
    """
    means = get_mean_data(data, "fin_aid_ratio")
    title = "Average Graduation Rate VS Average Percentage of Students With "\
            + "Financial Aid- All Universities"
    ylabel = "Percentage of Students with Financial Aid"
    save_file = "av_grad_rate_v_fin_all.png"

    plot_generic_graph(means, "fin_aid_ratio", (title, ylabel), (10, 10),
                       save_file)


def plot_average_grad_rate_vs_financial_public(public_data):
    """
    This function takes in the relavent dataframe public_data and produces a
    plot of average graduation rate and average financial aid ratio, along
    with printing the pearson R coefficient to the console.
    """
    means = get_mean_data(public_data, "fin_aid_ratio")
    title = "Average Graduation Rate VS Average Percentage of Students With "\
            + "Financial Aid- Public Universities"
    ylabel = "Percentage of Studentss with Financial Aid"
    save_file = "av_grad_rate_v_fin_pub.png"

    plot_generic_graph(means, "fin_aid_ratio", (title, ylabel), (10, 10),
                       save_file)


def plot_average_grad_rate_vs_financial_private(private_data):
    """
    This function takes in the relavent dataframe private_data and produces a
    plot of average graduation rate and average financial aid ratio, along with
    printing the pearson R coefficient to the console.
    """
    means = get_mean_data(private_data, "fin_aid_ratio")
    title = "Average Graduation Rate VS Average Percentage of Students With "\
            + "Financial Aid- Private Universities"
    ylabel = "Percentage of Students with Financial Aid"
    save_file = "av_grad_rate_v_fin_priv.png"

    plot_generic_graph(means, "fin_aid_ratio", (title, ylabel), (10, 10),
                       save_file)


def plot_generic_graph(data, column, labels, figsize, save_file):
    """
    This function takes in a dataframe data, y-axis column, a tuple labels
    with the format (title, ylabel), a size for the plot figsize, and
    a file name save_file, and creates a png of a plot called save_file for
    the data and column given, with the correct labels and size.
    """
    fig, ax = plt.subplots(1, figsize=figsize)

    sns.scatterplot(x="grad_rate", y=column, data=data, hue="School", ax=ax)
    plot_fit_line(data, ax, column, labels[0])

    plt.title(labels[0])
    plt.xlabel("Graduation Rate")
    plt.ylabel(labels[1])

    fig.savefig(save_file)


def main():
    """
    This function calls all the functions to create our dataframe and to
    generate our plots.
    """
    sns.set()
    # Getting all of the data
    data = create_dataframe()
    names = get_names_lists()
    public_data = filter_schools(data, names[0])
    private_data = filter_schools(data, names[1])
    fin_aid_data = get_fin_aid_data(data)
    public_fin_aid_data = get_fin_aid_data(public_data)
    private_fin_aid_data = get_fin_aid_data(private_data)

    # Plots for Question 0
    plot_grad_rate_vs_percent_accepted(data)
    plot_grad_rate_vs_percent_accepted_public(public_data)
    plot_grad_rate_vs_percent_accepted_private(private_data)
    plot_average_grad_rate_vs_percent_accepted(data)
    plot_average_grad_rate_vs_percent_accepted_public(public_data)
    plot_average_grad_rate_vs_percent_accepted_private(private_data)

    # Plots for Question 1
    plot_grad_rate_vs_financial(fin_aid_data)
    plot_grad_rate_vs_financial_public(public_fin_aid_data)
    plot_grad_rate_vs_financial_private(private_fin_aid_data)
    plot_average_grad_rate_vs_financial(fin_aid_data)
    plot_average_grad_rate_vs_financial_public(public_fin_aid_data)
    plot_average_grad_rate_vs_financial_private(private_fin_aid_data)


if __name__ == "__main__":
    main()

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from creating_dataframe import create_dataframe, get_names, read_data

sns.set()


def plot_fit_line(data, ax, column, plot_title):
    xs = data["grad_rate"]
    ys = data[column]
    fit = np.polyfit(xs, ys, 1)

    x = np.arange(0, 100, 0.1)
    ax.plot(x, fit[0] * x + fit[1], color="#000000")
    ax.set_xbound(0, 100)
    ax.set_ybound(0, 100)
    r_coeff = pearsonr(xs, ys)[0]

    print(plot_title + " Pearson R: " + str(r_coeff))


def filter_public_schools(data, public_names):
    is_public = data["School"].isin(public_names)
    bothell = "University of Washington-Bothell Campus"
    tacoma = "University of Washington-Tacoma Campus"
    not_satillite = (data["School"] != bothell) & (data["School"] != tacoma)
    public_data = data[is_public & not_satillite]
    return public_data


def filter_private_schools(data, private_names):
    is_private = data["School"].isin(private_names)
    private_data = data[is_private]
    return private_data


def filter_sufficient_data(data, column, threshold):
    filtered_data = data[["Year", "School", "grad_rate", column]]
    grad_rate_series = filtered_data.groupby("School")["grad_rate"].count()
    has_enough_data_s = grad_rate_series >= threshold
    names_with_data = grad_rate_series[has_enough_data_s].index
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
    return data.groupby("School")[column, "grad_rate"].mean().reset_index()


# Question 0: Competitiveness
def plot_grad_rate_vs_competitiveness(data):
    filtered_data = filter_sufficient_data(data, "percent_accepted", 15)

    fig, ax = plt.subplots(1, figsize=(10, 10))
    sns.scatterplot(x="grad_rate", y="percent_accepted", hue="School",
                    data=filtered_data, ax=ax)
    plt.xlabel("Graduation Rate")
    plt.ylabel("Competitiveness")
    title = "Graduation Rate VS Competitiveness- All Universites"
    plt.title(title)
    plot_fit_line(filtered_data, ax, "percent_accepted", title)
    fig.savefig("grad_rate_v_compet_all.png")


def plot_grad_rate_vs_competitiveness_public(public_data):
    filtered_data = filter_sufficient_data(public_data, "percent_accepted", 15)
    fig, ax = plt.subplots(1, figsize=(8, 8))
    sns.scatterplot(x="grad_rate", y="percent_accepted", hue="School",
                    data=filtered_data, ax=ax)
    plt.xlabel("Graduation Rate")
    plt.ylabel("Competitiveness")
    title = "Graduation Rate VS Competitiveness- Public Universites"
    plt.title(title)

    plot_fit_line(filtered_data, ax, "percent_accepted", title)
    fig.savefig("grad_rate_v_compet_pub.png")


def plot_grad_rate_vs_competitiveness_private(private_data):
    filtered_data = filter_sufficient_data(private_data, "percent_accepted",
                                           15)
    fig, ax = plt.subplots(1, figsize=(8, 8))
    sns.scatterplot(x="grad_rate", y="percent_accepted", hue="School",
                    data=filtered_data, ax=ax)
    plt.xlabel("Graduation Rate")
    plt.ylabel("Competitiveness")
    title = "Graduation Rate VS Competitiveness- Private Universites"
    plt.title(title)

    plot_fit_line(filtered_data, ax, "percent_accepted", title)
    fig.savefig("grad_rate_v_compet_priv.png")


def plot_average_grad_rate_vs_competitive(data):
    filtered_data = filter_sufficient_data(data, "percent_accepted", 15)
    means = get_mean_data(filtered_data, "percent_accepted")

    # needed to drop a row that had a tiny grad rate due to missing data
    means = means.drop(0)
    means = means.dropna()

    fig, ax = plt.subplots(1, figsize=(8, 8))
    sns.scatterplot(x="grad_rate", y="percent_accepted", hue="School",
                    data=means, ax=ax)
    plt.xlabel("Graduation Rate")
    plt.ylabel("Competitiveness")
    title = "Average Graduation Rate vs Average Competitiveness- All"\
            + "Universities"
    plt.title(title)

    plot_fit_line(means, ax, "percent_accepted", title)
    fig.savefig("av_grad_rate_v_compet_all")


def plot_average_grad_rate_vs_competitive_public(public_data):
    filtered_data = filter_sufficient_data(public_data, "percent_accepted", 15)
    new_data = filtered_data[["Year", "School", "percent_accepted",
                              "grad_rate"]]
    means = get_mean_data(new_data, "percent_accepted")

    fig, ax = plt.subplots(1, figsize=(8, 8))
    sns.scatterplot(x="grad_rate", y="percent_accepted", hue="School",
                    data=means, ax=ax)
    plt.xlabel("Graduation Rate")
    plt.ylabel("Competitiveness")
    title = "Average Graduation Rate vs Average Competitiveness- Public"\
            + "Universities"
    plt.title(title)

    plot_fit_line(means, ax, "percent_accepted", title)
    fig.savefig("av_grad_rate_v_compet_pub.png")


def plot_average_grad_rate_vs_competitive_private(private_data):
    filtered_data = filter_sufficient_data(private_data, "percent_accepted",
                                           15)
    means = get_mean_data(filtered_data, "percent_accepted")

    fig, ax = plt.subplots(1, figsize=(8, 8))
    sns.scatterplot(x="grad_rate", y="percent_accepted", hue="School",
                    data=means, ax=ax)
    plt.xlabel("Graduation Rate")
    plt.ylabel("Competitiveness")
    title = "Average Graduation Rate vs Average Competitiveness- Private"\
            + "Universities"
    plt.title(title)

    plot_fit_line(means, ax, "percent_accepted", title)
    fig.savefig("av_grad_rate_v_compet_priv.png")


# Question 1: Financial Aid
def get_fin_aid_data(data):
    short_df = data[['Year', 'School', 'population', 'fin_aid_private',
                     'fin_aid_public', 'grad_rate']]
    short_df = short_df.dropna(thresh=5)
    short_df.fillna(0, inplace=True)
    short_df['fin_aid'] = np.abs(short_df['fin_aid_private']
                                 - short_df['fin_aid_public'])
    short_df['fin_aid_ratio'] = (short_df['fin_aid'] /
                                 short_df['population'] * 100)

    # Some fin_aid_ratios higher than 100, doesn't make sense
    is_valid_fin_aid_ratio = short_df['fin_aid_ratio'] < 100
    short_df = short_df[is_valid_fin_aid_ratio]
    filtered = filter_sufficient_data(short_df, "fin_aid_ratio", 7)
    return filtered


def plot_grad_rate_vs_financial(data):
    fig, ax = plt.subplots(1, figsize=(10, 10))
    sns.scatterplot(x='grad_rate', y='fin_aid_ratio', data=data, hue='School',
                    ax=ax)
    plt.xlabel("Graduation Rate")
    plt.ylabel("Percentage of Students with Financial Aid")
    title = "Graduation Rate VS Percentage of Students With Financial Aid- "\
            + "All Universities"
    plt.title(title)
    plot_fit_line(data, ax, "fin_aid_ratio", title)
    fig.savefig("grad_rate_v_fin_all.png")


def plot_grad_rate_vs_financial_public(public_data):
    fig, ax = plt.subplots(1, figsize=(10, 10))
    sns.scatterplot(x='grad_rate', y='fin_aid_ratio', data=public_data,
                    hue='School', ax=ax)
    plt.xlabel("Graduation Rate")
    plt.ylabel("Percentage of Students with Financial Aid")
    title = "Graduation Rate VS Percentage of Students With Financial Aid- "\
            + "Public Universities"
    plt.title(title)
    plot_fit_line(public_data, ax, "fin_aid_ratio", title)
    fig.savefig("grad_rate_v_fin_pub.png")


def plot_grad_rate_vs_financial_private(private_data):
    fig, ax = plt.subplots(1, figsize=(10, 10))
    sns.scatterplot(x='grad_rate', y='fin_aid_ratio', data=private_data,
                    hue='School', ax=ax)
    plt.xlabel("Graduation Rate")
    plt.ylabel("Percentage of Students with Financial Aid")
    title = "Graduation Rate VS Percentage of Students With Financial Aid- "\
            + "Private Universities"
    plt.title(title)
    plot_fit_line(private_data, ax, "fin_aid_ratio", title)
    fig.savefig("grad_rate_v_fin_priv.png")


def plot_average_grad_rate_vs_financial(data):
    means = get_mean_data(data, "fin_aid_ratio")
    fig, ax = plt.subplots(1, figsize=(10, 10))
    sns.scatterplot(x='grad_rate', y='fin_aid_ratio', data=means, hue='School',
                    ax=ax)
    plt.xlabel("Graduation Rate")
    plt.ylabel("Percentage of Students with Financial Aid")
    title = "Average Graduation Rate VS Average Percentage of Students With "\
            + "Financial Aid- All Universities"
    plt.title(title)
    plot_fit_line(means, ax, "fin_aid_ratio", title)
    fig.savefig("av_grad_rate_v_fin_all.png")


def plot_average_grad_rate_vs_financial_public(public_data):
    means = get_mean_data(public_data, "fin_aid_ratio")
    fig, ax = plt.subplots(1, figsize=(10, 10))
    sns.scatterplot(x='grad_rate', y='fin_aid_ratio', data=means, hue='School',
                    ax=ax)
    plt.xlabel("Graduation Rate")
    plt.ylabel("Percentage of Students with Financial Aid")
    title = "Average Graduation Rate VS Average Percentage of Students With "\
            + "Financial Aid- Public Universities"
    plt.title(title)
    plot_fit_line(public_data, ax, "fin_aid_ratio", title)
    fig.savefig("av_grad_rate_v_fin_pub.png")


def plot_average_grad_rate_vs_financial_private(private_data):
    means = get_mean_data(private_data, "fin_aid_ratio")
    fig, ax = plt.subplots(1, figsize=(10, 10))
    sns.scatterplot(x='grad_rate', y='fin_aid_ratio', data=means, hue='School',
                    ax=ax)
    plt.xlabel("Graduation Rate")
    plt.ylabel("Percentage of Students with Financial Aid")
    title = "Average Graduation Rate VS Average Percentage of Students With "\
            + "Financial Aid- Private Universities"
    plt.title(title)
    plot_fit_line(means, ax, "fin_aid_ratio", title)
    fig.savefig("av_grad_rate_v_fin_priv.png")


def main():
    # Getting all of the data
    data = create_dataframe()
    names = get_names_lists()
    public_data = filter_public_schools(data, names[0])
    private_data = filter_private_schools(data, names[1])
    fin_aid_data = get_fin_aid_data(data)
    public_fin_aid_data = get_fin_aid_data(public_data)
    private_fin_aid_data = get_fin_aid_data(private_data)

    # Plots for Question 0
    plot_grad_rate_vs_competitiveness(data)
    plot_grad_rate_vs_competitiveness_public(public_data)
    plot_grad_rate_vs_competitiveness_private(private_data)
    plot_average_grad_rate_vs_competitive(data)
    plot_average_grad_rate_vs_competitive_public(public_data)
    plot_average_grad_rate_vs_competitive_private(private_data)

    # Plots for Question 1
    plot_grad_rate_vs_financial(fin_aid_data)
    plot_grad_rate_vs_financial_public(public_fin_aid_data)
    plot_grad_rate_vs_financial_private(private_fin_aid_data)
    plot_average_grad_rate_vs_financial(fin_aid_data)
    plot_average_grad_rate_vs_financial_public(public_fin_aid_data)
    plot_average_grad_rate_vs_financial_private(private_fin_aid_data)


if __name__ == "__main__":
    main()

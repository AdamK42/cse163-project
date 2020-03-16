import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from creating_dataframe import create_dataframe, get_names, read_data

sns.set()


def plot_fit_line(data, ax):
    xs = data["grad_rate"]
    ys = data["percent_accepted"]
    fit = np.polyfit(xs, ys, 1)

    x = np.arange(0, 100, 0.1)
    ax.plot(x, fit[0] * x + fit[1], color="#000000")
    ax.set_xbound(0, 100)
    ax.set_ybound(0, 100)
    
    print(pearsonr(xs, ys))


def filter_public_schools(data, public_names):
    is_public = data["School"].isin(public_names)
    not_satillite = (data["School"] != "University of Washington-Bothell Campus") &\
                    (data["School"] != "University of Washington-Tacoma Campus")
    public_data = data[is_public & not_satillite]
    public_data = filter_sufficient_data(public_data)
    return public_data


def filter_private_schools(data, private_names):
    is_private = data["School"].isin(private_names)
    private_data = data[is_private]
    private_data = filter_sufficient_data(private_data)
    return private_data


def filter_sufficient_data(data):
    filtered_data = data[["Year", "School", "grad_rate", "percent_accepted"]]
    grad_rate_series = filtered_data.groupby("School")["grad_rate"].count()
    has_enough_data_s = grad_rate_series >= 15
    names_with_data = grad_rate_series[has_enough_data_s].index
    has_enough_data = filtered_data["School"].isin(names_with_data)
    filtered_data = filtered_data[has_enough_data]
    return filtered_data.dropna()

def get_names_lists():
    """
    Returns a tuple which contains the list of public schools (index 0) and the list of private schools (index 1).
    """
    data = read_data()
    names = get_names(data)
    return (names[4], names[5])


# Question 0: Competitiveness
def plot_grad_rate_vs_competitiveness(data):
    data["percent_accepted"] = (data["admitted"] / data["applicants"]) * 100

    filtered_data = filter_sufficient_data(data)
    # new_data = data[["Year", "School", "percent_accepted",
    #                  "grad_rate"]].dropna()
    # series = new_data.groupby("School")["grad_rate"].count()
    # has_data_s = series >= 15
    # names_with_data = series[has_data_s].index
    # has_data = new_data["School"].isin(names_with_data)
    # new_data = new_data[has_data]

    fig, ax = plt.subplots(1, figsize=(10, 10))
    sns.scatterplot(x="grad_rate", y="percent_accepted", hue="School",
                    data=filtered_data, ax=ax)
    plt.xlabel("Graduation Rate")
    plt.ylabel("Competitiveness")
    plt.title("Graduation Rate VS Competitiveness- All Universites")

    # getting fit line
    plot_fit_line(filtered_data, ax)
    # xs = new_data["grad_rate"]
    # ys = new_data["percent_accepted"]
    # fit = np.polyfit(xs, ys, 1)

    # x = np.arange(0, 100, 0.1)
    # ax.plot(x, fit[0] * x + fit[1], color="#000000")
    # ax.set_xbound(0, 100)
    # ax.set_ybound(0, 100)



def plot_grad_rate_vs_competitiveness_public(public_data):
    #public_data = filter_public_schools(data, public_names)

    #filtered_data = public_data[["Year", "School", "percent_accepted", "grad_rate"]]

    fig, ax = plt.subplots(1, figsize=(10, 10))
    sns.scatterplot(x="grad_rate", y="percent_accepted", hue="School", data=public_data, ax=ax)
    plt.xlabel("Graduation Rate")
    plt.ylabel("Competitiveness")
    plt.title("Graduation Rate VS Competitiveness- Public Universites")

    # getting fit line
    xs = public_data["grad_rate"]
    ys = public_data["percent_accepted"]
    #plot_fit_line(public_data, ax)
    fit = np.polyfit(xs, ys, 1)

    x = np.arange(0, 100, 0.1)
    ax.plot(x, fit[0] * x + fit[1], color="#000000")
    ax.set_xbound(0, 100)
    ax.set_ybound(0, 100)
    fig.savefig("test.png")



def plot_grad_rate_vs_competitiveness_private(private_data):
    # private_data = filter_private_schools(data, private_names)
    # filtered_data = filter_sufficient_data(private_data)

    fig, ax = plt.subplots(1, figsize=(8,8))
    sns.scatterplot(x="grad_rate", y="percent_accepted", hue="School",
                    data=private_data, ax=ax)
    plt.xlabel("Graduation Rate")
    plt.ylabel("Competitiveness")
    plt.title("Graduation Rate VS Competitiveness- Private Universites")

    # getting fit line
    plot_fit_line(private_data, ax)
    # xs = filtered_data["grad_rate"]
    # ys = filtered_data["percent_accepted"]
    # fit = np.polyfit(xs, ys, 1)

    # x = np.arange(0, 100, 0.1)
    # ax.plot(x, fit[0] * x + fit[1], color="#000000")
    # ax.set_xbound(0, 100)
    # ax.set_ybound(0, 100)



def plot_average_grad_rate_vs_competitive(data):
    #new_data = data[["Year", "School", "percent_accepted", "grad_rate"]].dropna()
    filtered_data = filter_sufficient_data(data)

    means = filtered_data.groupby("School")["percent_accepted", "grad_rate"].mean().reset_index().dropna()
    means = means.drop(0)

    fig, ax = plt.subplots(1, figsize=(8,8))
    sns.scatterplot(x="grad_rate", y="percent_accepted", hue="School", data=means, ax=ax)
    plt.xlabel("Graduation Rate")
    plt.ylabel("Competitiveness")
    plt.title("Average Graduation Rate vs Average Competitiveness")

    plot_fit_line(means, ax)
    # getting fit line
    # xs = means["grad_rate"]
    # ys = means["percent_accepted"]
    # fit = np.polyfit(xs, ys, 1)

    # x = np.arange(0, 100, 0.1)
    # ax.plot(x, fit[0] * x + fit[1], color="#000000")
    # ax.set_xbound(0, 100)
    # ax.set_ybound(0, 100)

    # print(pearsonr(xs, ys))


# you can factor this even more by creating a public_data and 
# private_data in main, and pass that to this function
def plot_average_grad_rate_vs_competitive_public(public_data):
    # public_data = filter_public_schools(data, public_names)

    new_data = public_data[["Year", "School", "percent_accepted", "grad_rate"]]
    means = new_data.groupby("School")["percent_accepted", "grad_rate"].mean().reset_index()
    
    fig, ax = plt.subplots(1, figsize=(8,8))
    sns.scatterplot(x="grad_rate", y="percent_accepted", hue="School", data=means, ax=ax)
    plt.xlabel("Graduation Rate")
    plt.ylabel("Competitiveness")
    plt.title("Average Graduation Rate vs Average Competitiveness- Public Universities")

    # getting fit line
    xs = means["grad_rate"]
    ys = means["percent_accepted"]
    fit = np.polyfit(xs, ys, 1)

    x = np.arange(0, 100, 0.1)
    ax.plot(x, fit[0] * x + fit[1], color="#000000")
    ax.set_xbound(0, 100)
    ax.set_ybound(0, 100)

    print(pearsonr(xs, ys))


def plot_average_grad_rate_vs_competitive_private(private_data):
    means = private_data.groupby("School")["percent_accepted", "grad_rate"].mean().reset_index()
    fig, ax = plt.subplots(1, figsize=(8,8))
    sns.scatterplot(x="grad_rate", y="percent_accepted", hue="School", data=means, ax=ax)
    plt.xlabel("Graduation Rate")
    plt.ylabel("Competitiveness")
    plt.title("Average Graduation Rate vs Average Competitiveness for Private Universities")

    # getting fit line
    plot_fit_line(means, ax)
    # xs = means["grad_rate"]
    # ys = means["percent_accepted"]
    # fit = np.polyfit(xs, ys, 1)

    # x = np.arange(0, 100, 0.1)
    # ax.plot(x, fit[0] * x + fit[1], color="#000000")
    # ax.set_xbound(0, 100)
    # ax.set_ybound(0, 100)

    # print(pearsonr(xs, ys))







# Question 1: Financial Aid




def main():
    data = create_dataframe()
    names = get_names_lists()
    public_data = filter_public_schools(data, names[0])
    #private_data = filter_private_schools(data)
    plot_grad_rate_vs_competitiveness_public(public_data)


if __name__ == "__main__":
    main()
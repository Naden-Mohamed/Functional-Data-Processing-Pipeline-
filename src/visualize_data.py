import matplotlib.pyplot as plt

# ================================
# Pure Visualization Functions
# ================================

def create_line_plot(df, x, y):
    fig, ax = plt.subplots()
    ax.plot(df[x], df[y])
    ax.set_title(f"Line Plot: {y} vs {x}")
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    return fig

def create_bar_plot(df, column):
    fig, ax = plt.subplots()
    df[column].value_counts().plot(kind="bar", ax=ax)
    ax.set_title(f"Bar Plot of {column}")
    ax.set_xlabel(column)
    ax.set_ylabel("Count")
    return fig

def create_hist_plot(df, column):
    fig, ax = plt.subplots()
    ax.hist(df[column], bins=20)
    ax.set_title(f"Histogram of {column}")
    ax.set_xlabel(column)
    ax.set_ylabel("Frequency")
    return fig

def create_scatter_plot(df, x, y):
    fig, ax = plt.subplots()
    ax.scatter(df[x], df[y])
    ax.set_title(f"Scatter Plot: {y} vs {x}")
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    return fig


# ==================================
# Display / Saving
# ==================================


def show_plot(fig):
    fig.show()

def save_plot(fig, filename):
    fig.savefig(filename)

def build_visuals(tasks, df, acc=None):
    if acc is None:
        acc = []

    if not tasks:     # Base case
        return acc    # Return accumulative results

    task = tasks[0]
    rest = tasks[1:]

    plot_type = task["type"]

    if plot_type == "line":
        fig = create_line_plot(df, task["x"], task["y"])
    elif plot_type == "bar":
        fig = create_bar_plot(df, task["column"])
    elif plot_type == "hist":
        fig = create_hist_plot(df, task["column"])
    elif plot_type == "scatter":
        fig = create_scatter_plot(df, task["x"], task["y"])
    else:
        fig = None   # unknown

    acc.append(fig)

    # Tail recursion ↓ (call is last thing)
    return build_visuals(rest, df, acc)



def show_and_save_plots(figs, acc=0):
    if not figs:  # Base case: 
        return
    fig = figs[0]
    show_plot(fig)
    save_plot(fig, f"plots/plot_{acc}.png")
    show_and_save_plots(figs[1:], acc + 1)

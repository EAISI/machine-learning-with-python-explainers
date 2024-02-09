# Import module.
import pandas as pd

from collections import Counter


# Define function.
def f_freq(df_input, c_col, n_top = 10):

    """
    Gives information on a categorical variable in a data frame. Although, this function works on any variable,
    it is in particular useful in case of a categorical variable.

    Parameters
    ----------
    <name> : <type>
        <short description>.
    <name> : <type>
        <short description>.

    Returns
    -------
    <type>
        <short description>.
    """

    # Do not calculate the frequency table in case the feature has unique values.
    #if (len(set(df_input[c_col])) == len(df_input[c_col])):
    if (df_input[c_col]).is_unique:

      print("Column '" + c_col + "' consists of unique values.\n")

    if (len(set(df_input[c_col])) == 1):
      print("Column '" + c_col + "' consists of the same value.\n")

    # Bereken frequenties.
    c = Counter(df_input[c_col])

    # Converteer naar data frame.
    df_output         = pd.DataFrame(list(c.items())).reset_index(drop=True)

    # Hernoem kolomnamen.
    df_output.columns = ["level", "n"]

    # Bereken percentage.
    df_output["perc"] = round(100 * df_output["n"] / df_input.shape[0], 1).astype(str) + "%"

    # Sorteer data frame op frequentie.
    df_output         = df_output.sort_values(by = "n", ascending = False)

    if(df_output.shape[0] <= n_top):
            c_message = "we show all " + str(df_output.shape[0]) + " levels:"
            n_top     = df_output.shape[0]
            
    else:
            c_message = "we show the Top-" + str(n_top) + " of the " + str(df_output.shape[0]) + " levels:"
        
    # Print header
    print("Frequency of values in colum '" + c_col + "', " + c_message + "\n")

    #print(f"Number of NA: {df_input[c_col].isna().sum()} ({round(100 * df_input[c_col].isna().sum() / df_input.shape[0], 1)}%)\n")
            
    display(df_output.head(n_top))

    print("\n")

    # Plot frequency n_top elements.
    ax = df_input[c_col].value_counts(sort = True, ascending = False)[0:n_top].plot(kind='barh')
    ax.invert_yaxis()
    ax.set_ylabel(c_col)

    # https://stackoverflow.com/questions/3899980/how-to-change-the-font-size-on-a-matplotlib-plot
    for item in (ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(20)

    for item in [ax.xaxis.label, ax.yaxis.label]:
        item.set_fontsize(20 + 4)

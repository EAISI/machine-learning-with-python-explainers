# Import module.
import pandas as pd


# Define function.
def f_info(

    x,
    n_top       = 10,
    n_width     = 29,
    b_show_plot = False,
):

    """
    Get frequency information on column in data frame.

    Parameters
    ----------
    x               : Pandas Series
        Column in data frame you want to analyse.
    n_top           : int
        Maximum number of items to show. In case you want to see all items,
        enter None.
    n_width         : int
        Maximum number of characters to show of the values.
        This is useful in case the values consist of (long) sentences.
    b_show_plot     : bool
        Whether to show a bar chart of the frequency distribution.

    Returns
    -------
    -
        Printed output.

    Testing
    -------
    x = [4, 4, 4, 5, 5, 6, 7, 7, 7, 7, np.nan]
    x = ["abcdef", "abcdef", "abcdef", "abcdefghi", "abcdefghi", "abcdefghi", "abcdefghi", ""]
    x = pd.Series(x)

    df_ames = pd.read_csv('https://raw.githubusercontent.com/jads-nl/discover-projects/main/ames-housing/AmesHousing.csv')
    x = df_ames['Pool QC']
    x = df_ames['Lot Frontage']
    x = df_files_subset['file_name']

    x = df_data.competentie
    n_top   = 50
    n_width = 50
    """


#----------------------------------------------------------------------------------------------------------------------
# ERROR CHECK
#----------------------------------------------------------------------------------------------------------------------

    if not isinstance(x, pd.Series) and not isinstance(x, list):
        raise TypeError(f"You provided an invalid type for 'x'; it must be a pandas series or a list.")

    if not isinstance(n_top, int) and n_top is not None:
        raise TypeError(f"You provided an invalid value for 'n_top' ('{n_top}'); it must be an integer.")


#----------------------------------------------------------------------------------------------------------------------
# INITIALIZATION
#----------------------------------------------------------------------------------------------------------------------

    if isinstance(x, list) :
        l_input = pd.Series(x.copy())
    else:
        l_input = x.copy()

    # Number of elements.
    n_len = len(l_input)

    # Number of unique elements.
    n_unique = len(set(l_input))

    # Number to show.
    if n_top is None:        
        n_top = n_unique

    # We take max of length and 3 to prevent count errors below. Width is at least 3.
    n_char_count = max(3, len(f"{n_len:,}"))


#----------------------------------------------------------------------------------------------------------------------
# MAIN
#----------------------------------------------------------------------------------------------------------------------

    # Calculate basic info.
    df_basic_info = pd.DataFrame({

        'x': [

            "Total elements:",
            "Unique elements:",
            "empty:",
            "pd.isna():"
        ],

        'y': [                

            f"{len(l_input):,}".rjust(n_char_count),
            f"{n_unique:,}".rjust(n_char_count),
            f"{pd.Series(l_input=='').sum():,}".rjust(n_char_count),
            f"{sum(pd.isna(x) for x in l_input):,}".rjust(n_char_count)
        ],

        'z': [
            
            "",
            "",
            f"{round(pd.Series(l_input=='').sum() / n_len * 100, 1)}%".rjust(4),
            f"{round(sum(pd.isna(x) for x in l_input) / n_len * 100, 1)}%".rjust(4)
        ]
    })

    # Append numerical statistics in case x contains numerical data.
    if isinstance(l_input.values[0], (int, float, complex)):

        df_basic_info = pd.concat(

            [
                df_basic_info,
            
                pd.DataFrame({

                    'x': [

                        "0:",
                        "Inf(-):",
                        "Inf(+):"
                    ],

                    'y': [                

                        f"{sum(l_input==0):,}".rjust(n_char_count),
                        f"{sum((x is float('-inf') for x in l_input)):,}".rjust(n_char_count),
                        f"{sum((x is float('inf')  for x in l_input)):,}".rjust(n_char_count)
                    ],

                    'z': [

                        f"{round(sum(l_input==0) / n_len * 100, 1)}%".rjust(4),
                        f"{round(sum((x == float('-inf') for x in l_input)) / n_len * 100, 1)}%".rjust(4),
                        f"{round(sum((x == float('inf') for x in l_input)) / n_len * 100, 1)}%".rjust(4)
                    ]
                })
            ]
        )

    # Show in console, left align.
    c_0 = f"{0}".rjust(n_char_count)

    df_basic_info = df_basic_info.query("y != @c_0")
    df_basic_info.columns = ["="*(n_width-1), "="*n_char_count, "="*5]
    df_basic_info.index = [' ']*len(df_basic_info)

    # Replace any NaN and/or None by "None".
    l_input = l_input.fillna("NA")
    l_input = l_input.replace(float('-inf'), "-Inf ")
    l_input = l_input.replace(float('inf'), "Inf ")

    # Frequency table
    ps_freq = l_input.value_counts()

    # Calculate frequency of levels in vector.
    df_freq_source = pd.DataFrame({

        'value': ps_freq.index,
        'freq':  ps_freq.values
    })

    # Sort.
    df_freq_source = df_freq_source.sort_values(by=['freq', 'value'], ascending=[False, True])

    # Reduce length if len(x) > n_width.
    df_freq_source.value = [

        str(x)[0:(n_width)] + "..." if len(str(x)) >= (n_width - 0) else str(x)
        
        for x in df_freq_source.value # x = df_freq_source.value[0]
    ]

    # Define df_freq.
    df_freq_source['freq2'] = [f"{x}".rjust(n_char_count) for x in df_freq_source.freq]
    df_freq_source['perc']  =  df_freq_source.freq / sum(df_freq_source.freq) * 100
    df_freq_source['perc2'] = [f"{round(x,1)}%".rjust(4) for x in df_freq_source.perc]

    # Define df_dots.
    df_dots = pd.DataFrame({
        
        'value': "...",
        'freq': " "*(n_char_count - 3) + "...",
        'perc': " "*2                  + "..."
        },
        index = [0]
    )

    # Define df_total.
    df_total = pd.DataFrame({

            'value': ["-"*(n_width-1),  "TOTAL"],
            'freq':  ["-"*n_char_count, f"{n_len:,}"],
            'perc':  ["-"*5,            " 100%"]
    })

    # Update frequency section.
    df_freq = df_freq_source.drop(['freq', 'perc'], axis=1)
    df_freq = df_freq.rename(columns={'freq2':'freq', 'perc2':'perc'})
    df_freq = df_freq.head(n_top)

    # Puntjes toevoegen als n.top een getal is.
    if isinstance(n_top, int) and n_top < n_unique:
        df_freq = pd.concat([df_freq, df_dots])

    # Total toevoegen.
    df_freq         = pd.concat([df_freq, df_total])
    df_freq.columns = df_basic_info.columns
    df_freq.index   = ['']*len(df_freq)

    # Table strings.
    #c_type_table = "Type: " + type(l_input[0]).__name__

    c_freq_table = (

        (
            "All items:" if n_unique <= n_top else "Top-" + str(n_top)
        )

        if isinstance(n_top, int) else "All items:"

    ) + " (type: '" + type(l_input.values[0]).__name__ + "')"
    
    # Header frequency table.
    
    print("\n  " + " "*(n_width + n_char_count) + "n  perc")
    print(df_basic_info)
    print("\n  " + c_freq_table + " "*(n_width + n_char_count - len(c_freq_table)) + "n  perc")
    print(df_freq)


    ###########################################################################
    # Show frequency plot.
    ###########################################################################

    if b_show_plot:

        # Plot frequency n_top elements.
        ax = l_input.value_counts(sort = True, ascending = False)[0:n_top].plot(kind='barh')
        ax.invert_yaxis()

        # https://stackoverflow.com/questions/3899980/how-to-change-the-font-size-on-a-matplotlib-plot
        for item in (ax.get_xticklabels() + ax.get_yticklabels()):
            item.set_fontsize(20)

        for item in [ax.xaxis.label, ax.yaxis.label]:
            item.set_fontsize(20 + 4)

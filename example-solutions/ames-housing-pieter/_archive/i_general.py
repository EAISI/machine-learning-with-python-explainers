#######################################################################################################################
# Name:         INITIALIZATION - GENERAL.
# Date:         April 2023
# Description:  These functions support Jupyter Notebook 'ames-housing-pieter.ipynb' (JADS PE Foundation),
#               among many others projects.
# type: ignore
#######################################################################################################################

# The term '# type: ignore' above turns off error messages due to unknown variables even though they get assigned.
# https://github.com/microsoft/pylance-release/issues/929


#######################################################################################################################
# SYSTEM MODULES
#######################################################################################################################

# Load packages as a whole and as-is.
import re
import inspect
import os
import time
# import sys

# Load packages as a whole under an alias.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load selected functions from packages.
from collections import Counter
from scipy.stats import pearsonr
from sklearn.model_selection import train_test_split
from datetime import datetime

# Load function families from packages.
from sklearn import metrics


#######################################################################################################################
# PARAMETERS
#######################################################################################################################

# Path to code folder of this project.
C_PATH_CODE = os.getcwd()

# Paths to project root folder and sub-folders.
C_PATH_PROJECT_ROOT = re.sub("Code", "", C_PATH_CODE)
C_PATH_DATA         = C_PATH_PROJECT_ROOT + "Data/"
C_PATH_DELIVERABLES = C_PATH_PROJECT_ROOT + "Deliverables/"
C_PATH_DOCUMENTS    = C_PATH_PROJECT_ROOT + "Documents/"
C_PATH_IMAGES       = C_PATH_PROJECT_ROOT + "Images/"


#######################################################################################################################
# DEVELOPED FUNCTIONS
#######################################################################################################################

def f_who_am_i():

    """
    Get name and root folder of this computer.

    Parameters
    ----------
    -

    Returns
    -------
    str
        Computer name.
    str
        Root folder.
    """

    # Machine name of computer.
    C_MACHINE_NAME = os.uname().nodename
    

    # Computer name.
    if C_MACHINE_NAME in ['Pieters-Mac-Studio.local']:
        C_COMPUTER_NAME = 'macstudio'
    
    elif C_MACHINE_NAME in ['Pieters-MacBook-Pro.local']:
        C_COMPUTER_NAME = 'macbookpro'

    else:
        raise ValueError('Unknown machine name, cannot determine C_COMPUTER_NAME')
        
        
    # Root folder (Partner folder).
    C_ROOT = re.search(r'.+/Partners/', os.getcwd()).group()
    
    return C_COMPUTER_NAME, C_ROOT


#######################################################################################################################


def f_info(

    x,
    n_top   = 10,
    n_width = 29
):

    """
    Get frequency information on column in data frame.

    Parameters
    ----------
    x: Pandas Series
        Column in data frame you want to analyse.
    n_top: int / str
        Maximum number of items to show. In case you want to see all items, enter 'all'.
    n_width: int
        Maximum number of characters to show of the values. This is useful in case the values consist of (long) sentences.

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

    n_top   = 10
    n_width = 18
    """


#----------------------------------------------------------------------------------------------------------------------
# ERROR CHECK
#----------------------------------------------------------------------------------------------------------------------

    if(not isinstance(x, pd.Series) and not isinstance(x, list)):
        raise TypeError(f"You provided an invalid type for 'x'; it must be a pandas series or a list.")


    if(not isinstance(n_top, int) and n_top != "all"):
        raise TypeError(f"You provided an invalid type for 'n_top' ('{n_top}'); it must be 'all' or an integer.")


#----------------------------------------------------------------------------------------------------------------------
# INITIALIZATION
#----------------------------------------------------------------------------------------------------------------------

    if(isinstance(x, list)):
        l_input = pd.Series(x.copy())
    else:
        l_input = x.copy()

    # Number of elements.
    n_len = len(l_input)

    # Number of unique elements.
    n_unique = len(set(l_input))

    # Number to show.
    if(n_top == "all"):
        
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
            f"{sum(l_input==''):,}".rjust(n_char_count),
            f"{sum(pd.isna(x) for x in l_input):,}".rjust(n_char_count)
        ],

        'z': [
            
            "",
            "",
            f"{round(sum(l_input=='') / n_len * 100, 1)}%".rjust(4),
            f"{round(sum(pd.isna(x) for x in l_input) / n_len * 100, 1)}%".rjust(4)
        ]
    })

    # Append numerical statistics in case x contains numerical data.
    if isinstance(l_input[0], (int, float, complex)):

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

    c_freq_table = f_ifelse(
        
        isinstance(n_top, int),

        f_ifelse(

            n_unique <= n_top,
            "All items:",
            "Top-" + str(n_top)
        ),

        "All items:"

    ) + " (type: '" + type(l_input[0]).__name__ + "')"

    # Header frequency table.
    
    print("\n  " + " "*(n_width + n_char_count) + "n  perc")
    print(df_basic_info)
    print("\n  " + c_freq_table + " "*(n_width + n_char_count - len(c_freq_table)) + "n  perc")
    print(df_freq)


#######################################################################################################################

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


#######################################################################################################################

def f_var_name(var):

    """
    Get argument name of variable assigned to function parameter. It is used in 'f_describe()' for example.

    Parameters
    ----------
    var : any
        Parameter name to which an object is assigned to, and of which we want the name.

    Returns
    -------
    str
        Name of object assigned to parameter, i.e., the argument name.
    """

    lcls = inspect.stack()[2][0].f_locals

    for name in lcls:        
        if id(var) == id(lcls[name]):
            return name

    return None


#######################################################################################################################

def f_collapse(l_input):

    """
    Collapse list of items separated by ','.

    Parameters
    ----------
    l_input : list
        List of items to collapse.

    Returns
    -------
    str
        The collapsed string.
    """  

    # Return result.
    return ', '.join("'" + item + "'" for item in map(str, l_input))


#######################################################################################################################

def f_describe(df_input, n_top = 10):

    """
    An extended version of Python's describe() function.

    Parameters
    ----------
    df_input : Pandas Data Frame
        Data frame to apply descriptive statistics on.
    
    n_top : Integer
        Number of rows to show of the head of the data frame.

    Returns
    -------
    Printed output to the user.

    """  
    
    # Determine columns of the same data type.
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.select_dtypes.html
    # https://numpy.org/doc/stable/reference/arrays.scalars.html
    df_integer  = df_input.select_dtypes(include = np.integer)
    df_floating = df_input.select_dtypes(include = np.floating)
    df_category = df_input.select_dtypes(include = 'category')
    df_string   = df_input.select_dtypes(include = object)
    df_other    = df_input.select_dtypes(exclude = [np.integer, np.floating, 'category', object])

    # Overall stats
    print("The data:\n")
    print(f"-> Name:            '{f_var_name(df_input)}'\n")
    print(f"-> Dimension:        {df_input.shape[0]} rows and {df_input.shape[1]} columns.\n")
    print(f"-> Size:             {round(df_input.memory_usage(deep=True).sum()/1024/1024, 1)} MB.\n")

    if len(df_integer.columns):
        print(f"-> Integer columns:  {f_collapse(np.sort(df_integer.columns))}.\n")
    
    if len(df_floating.columns):
        print(f"-> Floating columns: {f_collapse(np.sort(df_floating.columns))}.\n")
    
    if len(df_category.columns):
        print(f"-> Category columns: {f_collapse(np.sort(df_category.columns))}.\n\n")
    
    if len(df_string.columns):
        print(f"-> String columns:   {f_collapse(np.sort(df_string.columns))}.\n\n")
    
    if len(df_other.columns):
        print(f"-> Other columns:    {f_collapse(np.sort(df_other.columns))}.\n\n")

    # Show first 'n_top' rows of the data.
    print("Show data (first " + str(n_top) + " rows, this number can be altered through 'n_top' in the function call):\n")
    display(df_input.head(n_top))
  
    # Describe integer columns
    if len(df_integer.columns):
        print(f"\n\nDescribe integer data ({len(df_integer.columns)} columns):")
        display(df_integer.describe())

    # Describe floating columns
    if len(df_floating.columns):
        print(f"\n\nDescribe floating data ({len(df_floating.columns)} columns):")
        display(df_floating.describe())

    # Describe category columns
    if len(df_category.columns):
        print(f"\n\nDescribe category data ({len(df_category.columns)} columns):")
        display(df_category.describe())

    # Describe string columns
    if len(df_string.columns):
        print(f"\n\nDescribe string data ({len(df_string.columns)} columns):")
        display(df_string.describe())

    # Describe other columns
    if len(df_other.columns):
        print(f"\n\nDescribe other data ({len(df_other.columns)} columns):")
        display(df_other.describe())

    # Show columns with missing data.
    ps_missing_total   = df_input.isnull().sum()
    ps_missing_percent = round(ps_missing_total / df_input.shape[0] * 100, 1)
    ps_missing_type    = df_input.dtypes

    df_missing_data = pd.DataFrame({'type': ps_missing_type, 'total': ps_missing_total, 'percent': ps_missing_percent})
    df_missing_data = df_missing_data.sort_values(by='total', ascending = False)
    df_missing_data = df_missing_data[df_missing_data.total > 0]

    if(df_missing_data.shape[0] == 0):
      print("")
      print("None of the columns have missing data!")
    else:
      print("\n\nShow missing data:")
      display(df_missing_data)



#######################################################################################################################

def f_grepl(pattern, l_str):

    """
    Searches for matches to argument 'pattern' within each element of a character list, 'l_str'.
    The Python equivalent of 'grepl' in R.

    Parameters
    ----------
    pattern : 'str'
        Regex pattern.
    l_str : 'list'
        Character list.

    Returns
    -------
    list
        Boolean list, True in case of a match and False in case of a non-match.

    Testing
    -------
    f_grepl("^P", ["Pieter", "Bart", "Theo", "aPieter"])
    """

    return [bool(re.search(pattern, x)) for x in l_str]


#######################################################################################################################

def f_find_str(pattern, l_str):

    """
    Searches for matches to argument 'pattern' within each element of a character list, 'l_str'.

    Parameters
    ----------
    pattern : 'str'
        Regex pattern.
    l_str : 'list'
        Character list.

    Returns
    -------
    list
        String list, including the items matching the pattern.

    Testing
    -------
    f_find_str("P$", ["Pieter", "BartP", "Theo", "aPieter"])
    """

    reg = re.compile(pattern)

    return list(filter(reg.search, l_str)) 



#######################################################################################################################

# Ifelse
def f_ifelse(b_eval, true, false):

    """
    <short description>.

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

    if b_eval:
        output = true
    else:
        output = false

    return output


#######################################################################################################################

def f_clean_up_header_names(l_input):

    """
    Clean up header names of data frame: (1) set names to lower case, and (2) replace spaces by '_'.

    Parameters
    ----------
    l_input : list
        Column names.


    Returns
    -------
    list
        Cleaned up column names.
    """

    return [

        # Put in lower case:
        y.lower() for y in [

        # Replace space by '_':
        re.sub(" ", "_", x) for x in

        l_input

        ]
    ]


#######################################################################################################################

def f_check_nonnumeric_in_df(
    
    df_input,
    l_exclude_columns = [],
    l_include_columns = []
    ):

    """
    Check on non-numeric in data frame.
    """

    """
    <short description>.

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

    Testing
    -------
    df_input          = df_nline_w_source
    l_exclude_columns = ['product']
    l_include_columns = []
    """

        
    # Error check - Are all column names in 'l_exclude_column' and 'l_include_column' present in df_input?
    l_exclude_columns_not_in_df_input = [x for x in l_exclude_columns if x not in  df_input.columns]
    l_include_columns_not_in_df_input = [x for x in l_include_columns if x not in  df_input.columns]

    if len(l_exclude_columns_not_in_df_input) > 0:

        c_temp = ', '.join(f"'{x}'" for x in l_exclude_columns_not_in_df_input)
        
        raise ValueError(
            f"The following column name(s) in 'l_exclude_columns' are not present in the column names of 'df_input': {c_temp}"
        )

    if len(l_include_columns_not_in_df_input) > 0:

        c_temp = ', '.join(f"'{x}'" for x in l_include_columns_not_in_df_input)
        
        raise ValueError(
            f"The following column name(s) in 'l_include_columns' are not present in the column names of 'df_input': {c_temp}"
        )


    # Error check - Are the same column names present in both 'l_exclude_column' and 'l_include_column'?
    l_overlap_include_exclude_columns = set(l_include_columns).intersection(set(l_exclude_columns))

    if len(l_overlap_include_exclude_columns) > 0:

        c_temp = ', '.join(f"'{x}'" for x in l_overlap_include_exclude_columns)
        
        raise ValueError(
            f"The following column name(s) are present in both 'l_exclude_columns' and 'l_include_columns': {c_temp}"
        )


    # Initialization.
    if l_include_columns == []:
        l_include_columns = df_input.columns


    # Main.
    df_to_check = df_input[[x for x in df_input.columns if x in l_include_columns and x not in l_exclude_columns]]
    df_eval     = df_to_check[~df_to_check.applymap(np.isreal).all(axis = 1)]

    if df_eval.shape[0] > 0:

        print(
            f"\nWARNING - '{f_var_name(df_input)}' contains non-numerical. We observe {df_eval.shape[0]} row(s) with at "
            f"least one non-numerical, below we show the first 5 rows (at max):\n"
        )

        print(df_eval.head(5))

        print("\nFor reference, the full data frame, incl. those columns that were not evaluated:\n")

        print(df_input.filter(items = df_eval.index, axis=0).head(5))

        print("\n")

    else:

        print(f"\nOK - '{f_var_name(df_input)}' contains numericals only.\n")


#######################################################################################################################

def f_check_na_in_df(
    
    df_input,
    l_exclude_columns = [],
    l_include_columns = []
    ):

    """
    Check on empty cells in data frame.

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

    Testing
    -------
    df_input          = df_htri_w_source
    l_exclude_columns = ['product']
    l_include_columns = []
    """

            
    # Error check - Are all column names in 'l_exclude_column' and 'l_include_column' present in df_input?
    l_exclude_columns_not_in_df_input = [x for x in l_exclude_columns if x not in  df_input.columns]
    l_include_columns_not_in_df_input = [x for x in l_include_columns if x not in  df_input.columns]

    if len(l_exclude_columns_not_in_df_input) > 0:

        c_temp = ', '.join(f"'{x}'" for x in l_exclude_columns_not_in_df_input)
        
        raise ValueError(
            f"The following column name(s) in 'l_exclude_columns' are not present in the column names of 'df_input': {c_temp}"
        )

    if len(l_include_columns_not_in_df_input) > 0:

        c_temp = ', '.join(f"'{x}'" for x in l_include_columns_not_in_df_input)
        
        raise ValueError(
            f"The following column name(s) in 'l_include_columns' are not present in the column names of 'df_input': {c_temp}"
        )


    # Error check - Are the same column names present in both 'l_exclude_column' and 'l_include_column'?
    l_overlap_include_exclude_columns = set(l_include_columns).intersection(set(l_exclude_columns))

    if len(l_overlap_include_exclude_columns) > 0:

        c_temp = ', '.join(f"'{x}'" for x in l_overlap_include_exclude_columns)
        
        raise ValueError(
            f"The following column name(s) are present in both 'l_exclude_columns' and 'l_include_columns': {c_temp}"
        )


    # Initialization.
    if l_include_columns == []:
        l_include_columns = df_input.columns


    # Main.
    df_to_check = df_input[[x for x in df_input.columns if x in l_include_columns and x not in l_exclude_columns]]
    df_eval     = df_to_check[df_to_check.applymap(pd.isnull).any(axis = 1)]


    if df_eval.shape[0] > 0:

        print(
            f"\nWARNING - '{f_var_name(df_input)}' contains NA. We observe {df_eval.shape[0]} row(s) with at "
            f"least one NA, below we show the first 5 rows (at max):\n"
        )

        print(df_eval.head(5))

        print(
            f"\nFor reference, the full data frame, incl. those columns that were not evaluated. "
            "Below, we show at max the first 5 rows:\n"
        )

        #print(df_input.filter(items = df_eval.index, axis=0).head(5))
        print(df_input.head(5))

        print("\n")

    else:

        print(f"\nOK - '{f_var_name(df_input)}' is fully filled.\n")


#######################################################################################################################

def f_get_latest_file(

    c_name,
    c_path,
    c_type
    ):

    """
    Get latest file with said string in the file residing in said path.

    Parameters
    ----------   
    c_name: 'str'
        String in the file name.
    c_path: 'str'
        Path where file resides.
    c_type: 'str'
        Reference to file type to be read.

    Returns
    -------
    Pandas Series
        file: file name
        date_mod: modification date
        age: age of file as string

    Testing
    -------  
    c_name = 'HTRI'
    c_path        = C_PATH_DELIVERABLES
    c_type        = 'xlsx'


    f_get_latest_file(c_name, c_path, c_type)
    """ 


#----------------------------------------------------------------------------------------------------------------------
# Initialization.
#----------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------------
# Error check.
#----------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------------
# Main.
#----------------------------------------------------------------------------------------------------------------------

    # Get all files in said folder, excl. any folders.
    df_file = pd.DataFrame({
        'file': f_find_str(
            
            # String to search for in the file names.
            pattern = c_name,

            # List with all files in c_path.
            l_str   = [
                
                f for f in os.listdir(c_path)

                # Filter on files only (excl dirs) and on the requested file type.
                if os.path.isfile(os.path.join(c_path, f)) and
                    os.path.splitext(os.path.join(c_path, f))[1]== '.'+c_type
            ]
        )
    })

    # Error check - Is a file found?
    if df_file.shape[0] == 0:
        raise LookupError(
            f"No file found for:\nFile name: '{c_name}'\nFile type: '{c_type}'\nFile path: '{c_path}'"
        )

    # Add number of seconds since epoch.
    df_file.insert(1, 'date_mod_sec',
        [os.path.getmtime(os.path.join(c_path, f)) for f in df_file.file]
    )
    
    # Get first row (latest file).
    ps_file = (df_file
        .sort_values(by='date_mod_sec', ascending=False)
        .iloc[0]
    )

    # Convert seconds to time stamp.
    ps_file['date_mod'] = datetime.fromtimestamp(
        
        ps_file.date_mod_sec
        
        ).strftime('%Y-%m-%d %H:%M:%S')
  
    # Add age of file
    n_age = time.time() - ps_file.date_mod_sec

    if n_age < 60:
        c_age = 'sec'
    elif n_age < 3600:
        n_age = n_age / 60
        c_age = 'minutes'
    elif n_age < 3600*24:
        n_age = n_age / 3600
        c_age = 'hours'
    else:
        n_age = n_age / 3600 / 24
        c_age = 'days'

    ps_file['age'] = str(round(n_age,1)) + " " + c_age


#----------------------------------------------------------------------------------------------------------------------
# Return results.
#----------------------------------------------------------------------------------------------------------------------

    # Return pandas series with information, except 'date_mod_sec' (not needed).
    return ps_file.drop('date_mod_sec')


#######################################################################################################################

def f_read_data_from_file(

    c_name,
    c_path,
    c_type     = "xlsx",
    c_sheet    = None,
    l_usecols  = None,
    n_skiprows = None,
    n_header   = 0
    ):

    """
    Read data from file into a data frame object.

    Parameters
    ----------   
    c_name: 'str'
        Name of the file where data is to be read from.
    c_path: 'str'
        Path where file resides.
    c_type: 'str'
        Reference to file type to be read (default: 'xlsx').
    c_sheet: 'str'
        Sheet name in case data is to read from Excel file (default: 'None').
    l_usecols: 'int',
        If list of int, then indicates list of column numbers to be parsed (0-indexed).
    n_skiprows: 'int'
        Line numbers to skip (0-indexed) or number of lines to skip (int) at the start of the file. 
    n_header: 'int'
        Row (0-indexed) to use for the column labels of the parsed DataFrame.

    Returns
    -------
    Data frame
        Data read from file is stored in data frame object.

    Testing
    -------  
    c_name  = "HTRI"
    c_path  = C_PATH_DELIVERABLES
    c_type  = 'xlsx'
    c_type  = 'csv'
    c_type  = 'parquet'
    c_sheet = None
    c_sheet = 'DATA1'

    df_nline_w_result_all = f_read_data_from_file(

        c_name = "Predicted N-lines - Distance 4 - nline_w",
        c_type = "parquet",
        c_path = C_PATH_DATA
    )

    f_read_data_to_file(c_name, c_path, c_type, l_name)
    """ 


#----------------------------------------------------------------------------------------------------------------------
# Initialization.
#----------------------------------------------------------------------------------------------------------------------

    # Valid file types.
    l_type_valid = ['xlsx', 'xlsm', 'csv', 'parquet']

    # Latest file.
    ps_file = f_get_latest_file(c_name, c_path, c_type)

#----------------------------------------------------------------------------------------------------------------------
# Error check.
#----------------------------------------------------------------------------------------------------------------------

    if c_type not in l_type_valid :
        raise ValueError(f"You did not provide a valid file type. Choose 'c_type' to be one of {', '.join(l_type_valid)}.")


#----------------------------------------------------------------------------------------------------------------------
# Main.
#----------------------------------------------------------------------------------------------------------------------

    # Excel
    if c_type in ['xlsx', 'xlsm']:

        df_data = pd.read_excel(

            io         = os.path.join(c_path, ps_file.file),
            sheet_name = c_sheet,
            usecols    = l_usecols,
            skiprows   = n_skiprows,
            header     = n_header
        )

    # CSV
    if c_type == 'csv':

        df_data = pd.read_csv(

            filepath_or_buffer = os.path.join(c_path, ps_file.file),
            sep                = ',',
            usecols            = l_usecols,
            skiprows           = n_skiprows,
            header             = n_header
        )

    # Parquet
    if c_type == 'parquet':

        df_data = pd.read_parquet(

            path    = os.path.join(c_path, ps_file.file),
            engine  = 'pyarrow',
            columns = l_usecols
        )


    # Comms to the user.
    print(f"\nReading at : {datetime.now()}")

    print(f"Requested  : '{c_name}' (file), '{c_type}' (type)")

    print(f"Read file  : '{ps_file.file}'")

    if c_type in ['xlsx', 'xlsm'] and c_sheet is not None:
        print(f"Sheet name : '{c_sheet}'")

    print(f"Path       : '.../{re.sub(f_who_am_i()[1], '', c_path)}'")

    print(f"Modified   : {ps_file.date_mod}")

    print(f"Age        : {ps_file.age}")

    print(f"==========================")


#----------------------------------------------------------------------------------------------------------------------
# Return results.
#----------------------------------------------------------------------------------------------------------------------

    return df_data


#######################################################################################################################

def f_write_data_to_file(

    l_df,
    c_name,
    c_path,
    c_type = "xlsx",
    l_name = None
    ):

    """
    Write object to file.

    Parameters
    ----------
    l_df: 'list' or 'Pandas Series' of values, 'Pandas DataFrame', or 'list' of 'Pandas DataFrame'
        Data object to write to file.    
    c_name: 'str'
        Name of the file where data object will be saved in.
    c_path: 'str'
        Path where file will be saved.
    c_type: 'str'
        Reference to file type (default: 'xlsx').
    l_name: 'str', or 'list' of 'str'
        Names to be used as sheet names or added to file name (default: 'None').

    Returns
    -------
    -
        Print statement in console to confirm writing of data to file.

    Testing
    -------
    l_df          = [pd.DataFrame({'a': [1,2,3,2,3,3], 'b': [5,6,7,8,9,9]}), pd.DataFrame({'a': [1,2,3], 'b': [5,6,7]})]
    l_df          =  pd.DataFrame({'a': [1,2,3,2,3,3], 'b': [5,6,7,8,9,9]})
    l_df          = pd.Series([1,2,3,4])
    l_df          = [1,2,3,2,3,3]    
    c_name = "Data file"
    c_path        = C_PATH_DELIVERABLES
    c_type        = 'xlsx'
    c_type        = 'csv'
    c_type        = 'parquet'
    l_name        = None
    l_name        = ['DATA1', 'DATA2']

    f_write_data_to_file(l_df, c_name, c_path, c_type, l_name)
    """ 


#----------------------------------------------------------------------------------------------------------------------
# Initialization.
#----------------------------------------------------------------------------------------------------------------------

    # Assign object name, for later use when communicating to user, see end.
    c_l_df = f_var_name(l_df)

    # Valid file types.
    l_type_valid = ['xlsx', 'csv', 'parquet']

    # Current time.
    dt_now = datetime.now()
    c_now  = re.sub("-", " ", str(dt_now.date())) + " - " + dt_now.strftime("%H %M %S") + " - "


    # Check on type of l_df and make corrections as needed.
    if isinstance(l_df, list) and not isinstance(l_df[0], pd.DataFrame):
        l_df = pd.Series(l_df)

    if isinstance(l_df, pd.Series):
        l_df = pd.DataFrame({'l_df': l_df})

    if isinstance(l_df, pd.DataFrame):
        l_df = [l_df]


    # Check on type of l_name and make corrections as needed.
    if isinstance(l_name, str):
        l_name = [l_name]

    # Check on l_name
    if l_name is None:
        l_name = ['data' + str(i+1) for i in f_seq_along(x)]


#----------------------------------------------------------------------------------------------------------------------
# Error check.
#----------------------------------------------------------------------------------------------------------------------

    if len(l_df) != len(l_name):
        raise IndexError("Length of 'l_df' and 'l_name' are not the same.")

    if c_type not in l_type_valid :
        raise ValueError(f"You did not provide a valid file type. Choose 'c_type' to be one of {', '.join(l_type_valid)}.")


#----------------------------------------------------------------------------------------------------------------------
# Main.
#----------------------------------------------------------------------------------------------------------------------

    # Excel - Store dataframe(s) in separate worksheets in same workbook.
    # To check later - https://xlsxwriter.readthedocs.io/example_pandas_table.html
    if c_type == 'xlsx':

        with pd.ExcelWriter(c_path + c_now + c_name + "." + c_type) as writer:

            for i in range(len(l_df)):

                l_df[i].to_excel(
                    excel_writer = writer,
                    sheet_name   = l_name[i],
                    index        = False
                )


    # CSV - Store dataframe(s) in separate CSV files.
    if c_type == 'csv':

        for i in range(len(l_df)):

            l_df[i].to_csv(
                path  = c_path + c_now + c_name + " - " + l_name[i] + "." + c_type,
                index = False
            )


    # Parquet - Store dataframe(s) in separate CSV files.
    if c_type == 'parquet':

        for i in range(len(l_df)):

            l_df[i].to_parquet(
                path   = c_path + c_now + c_name + " - " + l_name[i] + "." + c_type,
                index  = False,
                engine = 'pyarrow'
            )


    # l_df[0].iloc[:,:5].to_parquet(c_path + c_now + c_name + " - " + l_name[i] + "." + c_type, index=False)

    # Comms to the user.
    print(f"\nWriting at : {datetime.now()}")

    print(f"Object     : '{c_l_df}'")

    print(f"Name       : '{c_now + c_name + '.' + c_type}'")

    print(f"As         : '{c_type}'")

    print(f"Path       : '.../{re.sub(f_who_am_i()[1], '', c_path)}'")

    print(f"==========================")

#----------------------------------------------------------------------------------------------------------------------
# Return results.
#----------------------------------------------------------------------------------------------------------------------


#######################################################################################################################

def f_seq_along(l_input):

    """
    Generate regular sequence as long as the provided list.
        
    Parameters
    ----------
    l_input : list
        List to determine length of sequence.
   
    Returns
    -------
    list
        Sequence as long as l_input.

    Test
    ----
    l_input = ['a', 'b', 'c']
    l_input = pd.Series(l_input)
    f_seq_along(l_input)
    """


#----------------------------------------------------------------------------------------------------------------------
# Initialization.
#----------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------------
# Error check.
#----------------------------------------------------------------------------------------------------------------------

    if not isinstance(l_input, (list, pd.Series)):
        raise IndexError("Length of 'x' and 'l_name' are not the same.")

#----------------------------------------------------------------------------------------------------------------------
# Main.
#----------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------------
# Return results.
#----------------------------------------------------------------------------------------------------------------------

    return list(np.arange(len(l_input)))


#######################################################################################################################

def reg_coef(v_x, v_y, label = None, color = None, **kwargs):

    """
    To calculate correlation coefficients in PairGrid plot.

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

    ax = plt.gca()

    r,p = pearsonr(v_x, v_y)

    ax.annotate('r = {:.2f}'.format(r), xy=(0.5, 0.5), xycoords = 'axes fraction', ha = 'center')

    ax.set_axis_off()


#######################################################################################################################

def f_heatmap(
        df_input,
        v_features_to_show,
        b_add_annotate     = True,
        n_font_size        = 15
    ):

    """
    Plot heatmap of correlation coefficients.

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

    plt.rcParams['figure.figsize'] = (15, 15)
    
    df_cor = df_input[v_features_to_show].corr()
    
    m_matrix = np.triu(df_cor)

    sns.heatmap(        
        data      = df_cor,
        annot     = b_add_annotate,
        annot_kws = {'size': n_font_size},
        square    = True,
        cmap      = 'coolwarm',
        mask      = m_matrix
    );


#######################################################################################################################

def f_train_test_split(df_X, ps_y):

    """
    Perform train/test split and share dimensions with user.

    Parameters
    ----------
    df_X : Pandas Data frame
        Feature data.
    ps_y : Pandas Series
        Outcome variable.

    Returns
    -------
    Pandas Data frame
        df_X_train

    Pandas Data frame
        df_X_test

    Pandas Series
        ps_y_train

    Pandas Series
        ps_y_test
    """

    df_X_train, df_X_test, ps_y_train, ps_y_test = train_test_split(df_X, ps_y, test_size=0.33, random_state=42)

    print(f"Dimension of df_X_train:                       {df_X_train.shape[0]} by {df_X_train.shape[1]}")
    print(f"Dimension of df_X_test:                        {df_X_test.shape[0]}  by {df_X_test.shape[1]}")

    print(f"Length of ps_y_train:                          {ps_y_train.shape[0]}")
    print(f"Length of ps_y_test:                           {ps_y_test.shape[0]}\n")

    print(f"Combined number of rows in train and test set: {ps_y_train.shape[0] + ps_y_test.shape[0]}")
    print(f"Original number of rows:                       {df_X.shape[0]}")
    print(f"Actual split:                                  {round(ps_y_test.shape[0]/ps_y.shape[0], 2)}")

    return df_X_train, df_X_test, ps_y_train, ps_y_test


#######################################################################################################################

# Share model evaluation results with the user.
def f_evaluation_results(v_y_true, v_y_pred):

    print("Performance Metrics:")
    print(f"MAE:  {metrics.mean_absolute_error(v_y_true, v_y_pred):,.1f}")
    print(f"MSE:  {metrics.mean_squared_error(v_y_true, v_y_pred):,.1f}")
    print(f"RMSE: {metrics.mean_squared_error(v_y_true, v_y_pred, squared=False):,.1f}")


#######################################################################################################################

# def f_(

#     ):

#     """
#     <short description>.

#     Parameters
#     ----------
#     <name> : <type>
#         <short description>.
#     <name> : <type>
#         <short description>.

#     Returns
#     -------
#     <type>
#         <short description>.
#     """


# #----------------------------------------------------------------------------------------------------------------------
# # Testing.
# #----------------------------------------------------------------------------------------------------------------------

# #----------------------------------------------------------------------------------------------------------------------
# # Initialization.
# #----------------------------------------------------------------------------------------------------------------------

# #----------------------------------------------------------------------------------------------------------------------
# # Error check.
# #----------------------------------------------------------------------------------------------------------------------

# #----------------------------------------------------------------------------------------------------------------------
# # Main.
# #----------------------------------------------------------------------------------------------------------------------

# #----------------------------------------------------------------------------------------------------------------------
# # Return results.
# #----------------------------------------------------------------------------------------------------------------------

#     return

#######################################################################################################################
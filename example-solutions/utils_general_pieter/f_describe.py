# Import module.
import pandas as pd
import numpy as np

from .f_join        import f_join
from .f_var_name    import f_var_name


# Define function.
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
        print(f"-> Integer columns:  {f_join(np.sort(df_integer.columns))}.\n")
    
    if len(df_floating.columns):
        print(f"-> Floating columns: {f_join(np.sort(df_floating.columns))}.\n")
    
    if len(df_category.columns):
        print(f"-> Category columns: {f_join(np.sort(df_category.columns))}.\n\n")
    
    if len(df_string.columns):
        print(f"-> String columns:   {f_join(np.sort(df_string.columns))}.\n\n")
    
    if len(df_other.columns):
        print(f"-> Other columns:    {f_join(np.sort(df_other.columns))}.\n\n")

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


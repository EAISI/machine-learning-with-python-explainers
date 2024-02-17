"""
Purpose:    Init file - Utilities Pieter
Author:     Pieter Overdevest
Date:       2024-02-09
"""

# Set version number
__version__ = "1.0.0"

# Import modules - By using this approach we can import the functions
# in to the Jupyter Notebook. There is no need to refer to the module
# name. We can state "from utils_pieter import f_info" and use the 
# f_info function in the Jupyter Notebook.
# In case we would exclude the lines below, we would have to state
# "from utils_pieter.f_info import f_info" in order to use said function
# in the Jupyter Notebook.
from .f_check_na_in_df               import f_check_na_in_df
from .f_check_nonnumeric_in_df       import f_check_nonnumeric_in_df
from .f_clean_up_header_names        import f_clean_up_header_names
from .f_describe                     import f_describe
from .f_get_account_name             import f_get_account_name
from .f_evaluate_results             import f_evaluate_results
from .f_get_filenames_in_folder      import f_get_filenames_in_folder
from .f_get_latest_file              import f_get_latest_file
from .f_heatmap                      import f_heatmap
from .f_info                         import f_info
from .f_join                         import f_join
from .f_now                          import f_now
from .f_plot_scatter_with_trend_grid import f_plot_scatter_with_trend_grid
from .f_plot_scatter_with_trend      import f_plot_scatter_with_trend
from .f_train_test_split             import f_train_test_split
from .f_var_name                     import f_var_name

# Print message - Just for demo purposes.
print("Done!")






# Import module.
import re

from pandas.api.types import is_numeric_dtype


# Define function.
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
        x3.lower() for x3 in [

        # Replace space by '_':
        x2 if is_numeric_dtype(x2) else re.sub(" |\.", "_", x2) for x2 in [

        str(x1) for x1 in l_input        
    ]]]

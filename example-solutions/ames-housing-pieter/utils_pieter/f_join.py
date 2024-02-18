# Import module.
import pandas as pd


# Define function.
def f_join(
          
          l_input,
          c_sep   = ',',
          b_quote = False,
          c_quote = "'",
          c_and   = None
    ):

    """
    Join list of items separated by ','.

    Parameters
    ----------
    l_input     : list
        List of items to collapse.
    c_sep:      : str
        Separator (default: ',').
    b_quote     : boolean
        Should items be quoted? (default: False).
    c_quote     : str
        The quote to be used, typically '"' or "'".
    c_and       : str
        Binding element between (for-)last elements (default: None).

    Returns
    -------
    str
        The joined string.

    Testing
    -------

    # In alle gevallen:
    c_sep   = ','
    b_quote = False
    c_quote = "'"
    c_and   = None

    l_input  = ['apple', 'banana', 'pear', 5]
    c_sep    = ','
    b_quote  = True
    c_quote  = "'"
    c_and    = 'and'

    f_join(l_input)

    l_input = df_non_allowed_score.competentie
    c_and   = 'en'
    b_quote = True

    """  

    ###################################################################################################################
    # Initialization.
    ###################################################################################################################

    # Check whether l_input is a list, if not make it a list.
    if isinstance(l_input, pd.Series):
            l_input = list(l_input)

    # Determine length of l_input.
    n_length = len(l_input)

    # Check on n_length.
    if n_length == 0:
         return ""

    # Add quotation if requested.
    if b_quote:

        l_input = [c_quote + item + c_quote for item in map(str, l_input)]

    # Add space behind c_sep if it is not "\n", e.g., when it is ","".
    c_sep = c_sep if c_sep == "\n" else c_sep + " "


    ###################################################################################################################
    # Main.
    ###################################################################################################################

    if c_and is None:

        c_output = c_sep.join(l_input)

    else:

        if n_length == 1:
        
            c_output = l_input[0]

        elif n_length == 2:

            c_output = l_input[0] + " " + c_and + " " + l_input[1]

        else:

            c_output = c_sep.join(l_input[:-1]) + c_sep + c_and + " " + l_input[n_length-1]


    ###################################################################################################################
    # Return.
    ###################################################################################################################

    return c_output

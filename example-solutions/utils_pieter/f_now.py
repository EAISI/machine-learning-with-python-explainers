# Import module.
import re

from datetime import datetime


# Define function.
def f_now():

    """
    Get string containing today's date and current time.

    Parameters
    ----------
    -

    Returns
    -------
    str
        String containing today's date and current time.

    Testing
    -------
    """ 

    # Current time.
    dt_now = datetime.now()

    return(
        re.sub("-", " ", str(dt_now.date())) + " - " +
        dt_now.strftime("%H %M %S")
    )

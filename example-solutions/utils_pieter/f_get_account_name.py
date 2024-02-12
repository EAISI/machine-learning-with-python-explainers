# Import module.
import os

# Define function.
def f_get_account_name():

    """
    Get name of the account.

    Parameters
    ----------
    -

    Returns
    -------
    str
        Account name.
    """

    # Machine name of computer.
    C_MACHINE_NAME = os.uname().nodename
    
    # Computer name.
    if C_MACHINE_NAME in ['Pieters-Mac-Studio.local']:
        return 'macstudio'
    
    elif C_MACHINE_NAME in ['Pieters-MacBook-Pro.local', 'Pieters-MBP', 'pieters-mbp.home']:
        return 'home'

    else:
        raise ValueError('Unknown machine name, cannot determine C_ACCOUNT_NAME')

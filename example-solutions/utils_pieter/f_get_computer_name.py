# Import module.
import os

# Define function.
def f_get_computer_name():

    """
    Get name of this computer.

    Parameters
    ----------
    -

    Returns
    -------
    str
        Computer name.
    """

    # Machine name of computer.
    C_MACHINE_NAME = os.uname().nodename
    
    # Computer name.
    if C_MACHINE_NAME in ['Pieters-Mac-Studio.local']:
        C_COMPUTER_NAME = 'macstudio'
    
    elif C_MACHINE_NAME in ['Pieters-MacBook-Pro.local', 'Pieters-MBP', 'pieters-mbp.home']:
        C_COMPUTER_NAME = 'macbookpro'

    else:
        raise ValueError('Unknown machine name, cannot determine C_COMPUTER_NAME')
        
    return C_COMPUTER_NAME

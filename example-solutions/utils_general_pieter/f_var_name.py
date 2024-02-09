# Import module.
import inspect

# Define function.
def f_var_name(var):

    """
    Get argument name of variable assigned to function parameter.

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
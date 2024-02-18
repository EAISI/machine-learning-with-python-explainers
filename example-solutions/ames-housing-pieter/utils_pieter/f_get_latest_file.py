# Import module.
from .f_get_filenames_in_folder import f_get_filenames_in_folder


# Define function.
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
    c_path = C_PATH_DELIVERABLES
    c_type = 'xlsx'

    c_name = 'Den Haag - Displays - Overzicht na plaatsing'
    c_path = c_path_file_xls
    c_type = 'xlsx'

    c_name      = "Tuning AV based on score"
    c_path      = os.path.join(C_PATH_DELIVERABLES, "2024 02 04 - Tuning GIs based on score")
    c_type      = "xlsx"


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

    # Data van latest file.
    ps_file = (
        
        f_get_filenames_in_folder(

            c_name      = c_name,
            c_path      = c_path,
            c_type      = c_type,
            b_recursive = False
        )

        # Neem eerste rij, want de rijen zijn gesorteerd van nieuw naar oud.
        .iloc[0]
    )

  
    # Age of latest file in seconds.
    n_age =  ps_file.age_mod_sec

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

    # Return pandas series with information, except 'folder' and
    # 'age_mod_sec' (not needed).
    return ps_file.drop(['folder', 'age_mod_sec'])

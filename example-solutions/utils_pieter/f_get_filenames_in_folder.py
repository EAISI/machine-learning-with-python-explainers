# Import module.
import os
import re
import time

import pandas as pd

from datetime import datetime


# Define function.
def f_get_filenames_in_folder(

    c_name,
    c_path,
    c_type,
    b_recursive = False
    ):

    """
    Get filenames with said string in the file residing in said path.

    Parameters
    ----------   
    c_name: 'str'
        String in the file name.
    c_path: 'str'
        Path where file resides.
    c_type: 'str'
        Reference to file type to be read.
    b_recursive: 'bool'
        Recursive search in subfolders (default: False).

    Returns
    -------
    Pandas Data Frame
        file: file name
        path: path to file
        date_mod: modification date
        age: age of file as string

    Testing
    -------  

    c_name      = ''
    c_name      = "Tuning AV based on score"
    c_path      = C_PATH_DELIVERABLES
    c_type      = "xlsx"
    b_recursive = False


    """ 


#----------------------------------------------------------------------------------------------------------------------
# Initialization.
#----------------------------------------------------------------------------------------------------------------------

    l_df_file = []


#----------------------------------------------------------------------------------------------------------------------
# Error check.
#----------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------------
# Main.
#----------------------------------------------------------------------------------------------------------------------
    
    if b_recursive:

        for c_root, l_dir, l_file in os.walk(c_path):

            # c_root: de root waarin naar directories en filenames gezocht wordt (str).
            # l_dirs: de directories in de root (list).
            # l_file: de files in de root (list).

            # File names.
            l_file_select = list(filter(
                    
                # String to search for in the file names.
                re.compile(c_name).search,

                # List with all files in c_path.
                [                
                    f for f in os.listdir(c_root)

                    # Filter on files only (excl dirs) and on the requested file type.
                    if (
                        os.path.isfile(os.path.join(c_root, f)) and
                        c_type in os.path.splitext(os.path.join(c_root, f))[1]
                    )
                ]
            ))

            df_file = pd.DataFrame({

                'folder': [
                    c_root for i in range(len(l_file_select))
                ],

                'file':   l_file_select,

                'full_path':   [                    
                    os.path.join(c_root, f) for f in l_file_select
                ]
            })

            l_df_file.append(df_file)

        # Concatenate the list of data frames.
        df_file = pd.concat(l_df_file)

    else:

        # Get all files in said folder, excl. any folders.
        l_file_select = list(filter(
                
            # String to search for in the file names.
            re.compile(c_name).search,

            # List with all files in c_path.
            [                
                f for f in os.listdir(c_path)

                # Filter on files only (excl dirs) and on the requested file type.
                if (
                    os.path.isfile(os.path.join(c_path, f)) and
                    c_type in os.path.splitext(os.path.join(c_path, f))[1]
                )
            ]
        ))
        
        df_file = pd.DataFrame({

            'folder': [
                c_path for i in range(len(l_file_select))
            ],

            'file':   l_file_select,

            'full_path':   [                    
                os.path.join(c_path, f) for f in l_file_select
            ]
        })


    # Error check - Is a file found?
    if df_file.shape[0] == 0:
        raise LookupError(
            f"No file found for:\nFile name: '{c_name}'\nFile type: '{c_type}'\nFile path: '{c_path}'"
        )


    # Add number of seconds since epoch.
    df_file = df_file.assign(
        
        date_mod_sec = [os.path.getmtime(f) for f in df_file.full_path]
    )
    
    # Convert seconds to time stamp.
    df_file = df_file.assign(
        
        date_mod = [

            datetime.fromtimestamp(d).strftime('%Y-%m-%d %H:%M:%S')
            
             for d in df_file.date_mod_sec
        ]
    )

    # Add age in seconds.
    df_file = df_file.assign(
        
        age_mod_sec = [time.time() - x for x in df_file.date_mod_sec]
    )
    
    # Sort by date of modification (descending).
    df_file = df_file.sort_values(by = 'date_mod_sec', ascending = False)
    

#----------------------------------------------------------------------------------------------------------------------
# Return results.
#----------------------------------------------------------------------------------------------------------------------

    # Return pandas data frame with information, except 'date_mod_sec' (not needed).
    return df_file.drop('date_mod_sec', axis=1)

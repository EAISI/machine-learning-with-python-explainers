# Import module.
from sklearn.model_selection import train_test_split


# Define function
def f_train_test_split(        
        df_X,
        ps_y,
        n_test_size = 0.33,
    ):

    """
    Perform train/test split and share dimensions with user.

    Parameters
    ----------
    df_X        : Pandas Data frame
        Feature data.
    ps_y        : Pandas Series
        Outcome variable.
    n_test_size : float, optional (default = 0.33)
        Size of test set.

    Returns
    -------
    Pandas Data frame
        df_X_train

    Pandas Data frame
        df_X_test

    Pandas Series
        ps_y_train

    Pandas Series
        ps_y_test
    """

    df_X_train, df_X_test, ps_y_train, ps_y_test = train_test_split(
        
        df_X,
        ps_y,
        test_size    = n_test_size,
        random_state = 42
    )

    print(
        f"Dimension of df_X_train:                       "
        f"{df_X_train.shape[0]} by {df_X_train.shape[1]}"
    )
    print(
        f"Dimension of df_X_test:                        "
        f"{df_X_test.shape[0]}  by {df_X_test.shape[1]}"
    )
    print(
        f"Length of ps_y_train:                          "
        f"{ps_y_train.shape[0]}"
    )    
    print(
        f"Length of ps_y_test:                           "
        f"{ps_y_test.shape[0]}\n"
    )

    print(
        f"Combined number of rows in train and test set: "
        f"{ps_y_train.shape[0] + ps_y_test.shape[0]}")
    print(
        f"Original number of rows:                       "
        f"{df_X.shape[0]}")
    print(
        f"Actual split:                                  "
        f"{round(ps_y_test.shape[0]/ps_y.shape[0], 2)}")

    return df_X_train, df_X_test, ps_y_train, ps_y_test

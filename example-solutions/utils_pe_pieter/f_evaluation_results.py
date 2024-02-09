# Import module.
from sklearn import metrics

# Define function
def f_evaluation_results(
        v_y_true,
        v_y_pred
    ):

    """
    Share model evaluation results with the user.

    Parameters
    ----------
    <name> : <type>
        <short description>.
    <name> : <type>
        <short description>.

    Returns
    -------
    <type>
        <short description>.
    """

    print("Performance Metrics:")
    print(f"MAE:  {metrics.mean_absolute_error(v_y_true, v_y_pred):,.1f}")
    print(f"MSE:  {metrics.mean_squared_error(v_y_true, v_y_pred):,.1f}")
    print(f"RMSE: {metrics.mean_squared_error(v_y_true, v_y_pred, squared=False):,.1f}")

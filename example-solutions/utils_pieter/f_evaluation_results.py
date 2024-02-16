# Import module.
from sklearn import metrics

from matplotlib import pyplot as plt

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

    plt.scatter(v_y_true, v_y_pred);

    print("Performance Metrics:")
    print(f"MAE:  {metrics.mean_absolute_error(v_y_true, v_y_pred):,.3f}")
    print(f"MSE:  {metrics.mean_squared_error(v_y_true, v_y_pred):,.3f}")
    print(f"RMSE: {metrics.mean_squared_error(v_y_true, v_y_pred, squared=False):,.3f}")

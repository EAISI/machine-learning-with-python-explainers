# Import module.
from sklearn import metrics
from pandas import DataFrame

import altair as alt

# Define function
def f_evaluate_results(
        ps_y_true,
        ps_y_pred
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
    print(f"MAE:  {metrics.mean_absolute_error(ps_y_true, ps_y_pred):,.3f}")
    print(f"MSE:  {metrics.mean_squared_error(ps_y_true, ps_y_pred):,.3f}")
    print(f"RMSE: {metrics.mean_squared_error(ps_y_true, ps_y_pred, squared=False):,.3f}")

    # import numpy as np
    # ps_y_true = np.random.rand(100) * 100  # 100 actual values
    # ps_y_pred = ps_y_true + (np.random.rand(100) - 0.5) * 20  # 100 predicted values with some noise

    # Initialize
    n_min = min(min(ps_y_true), min(ps_y_pred))
    n_max = max(max(ps_y_true), max(ps_y_pred))

    # Creating a pandas DataFrame
    df_scatter = (
        DataFrame({'Actual': ps_y_true, 'Predicted': ps_y_pred})
        .reset_index(drop=False)
        .rename(columns={'index': 'Row index'})
    )
    df_y_x     = DataFrame({'x': [n_min, n_max], 'y': [n_min, n_max]})

    # Creating the scatter plot
    alt1 = alt.Chart(df_scatter).mark_circle(size=60).encode(

        x = alt.X(
            'Actual',
            title = 'Actual Values',
            scale = alt.Scale(domain=(n_min, n_max))
        ),
        y = alt.Y(
            'Predicted',
            title = 'Predicted Values',
            scale = alt.Scale(domain=(n_min, n_max))
        ),
        tooltip = [
            alt.Tooltip('Actual',    format = '.2f'),
            alt.Tooltip('Predicted', format = '.2f'),
            'Row index'
        ]  # Rounds to 2 decimal places

    ).properties(
    ).properties(
        width  = 400,
        height = 400
    )

    # Adding y=x line for reference
    alt2 = alt.Chart(df_y_x).mark_line(color='red').encode(
        x='x',
        y='y'
    )

    # Combining the scatter plot and the line.
    # The x='shared' in the resolve_scale function of Altair means that
    # the x-axis scale will be shared across multiple charts or layers
    # within the visualization. This ensures that all components of the
    # combined plot use the same scale for the x-axis, allowing for
    # consistent comparison between them​.
    final_plot = (alt1 + alt2).resolve_scale(
        x='shared',
        y='shared'
    )

    display(final_plot)

    

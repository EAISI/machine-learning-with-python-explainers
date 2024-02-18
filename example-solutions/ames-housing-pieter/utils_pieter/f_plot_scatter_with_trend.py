# Import module.
import altair as alt

# Define function
def f_plot_scatter_with_trend(df_input, c_x, c_y):

    """
    Plot heatmap of correlation coefficients.

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

    alt1 = (
      
        alt.Chart(df_input)
        .mark_circle(opacity=0.1)
        .encode(
            x = c_x,
            y = 'SalePrice_log'
        )
        .properties(
            height = 200,
            width  = 200
        )
    )

    alt2 = (
      
        alt1
        .transform_regression(c_x, c_y, method="linear")
        .mark_line(color='red')
    )

    return (alt1 + alt2)

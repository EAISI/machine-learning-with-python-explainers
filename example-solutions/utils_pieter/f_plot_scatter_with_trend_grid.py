# Import module.
import altair as alt

from .f_plot_scatter_with_trend import f_plot_scatter_with_trend

# Define function
def f_plot_scatter_with_trend_grid(df_input, l_x, c_y, n_col):

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


    # Create list of charts (scatter with trend line).
    l_chart = [
        
        f_plot_scatter_with_trend(df_input=df_input, c_x=x, c_y=c_y) 
        
        for x in l_x
    ]

    # We transform `l_chart` to a list of smaller chart lists (`l_l_chart`).
    # Each chart list holds a row of `n_col` charts. E.g., we create as many
    # 'chart rows' until each of 38 charts is in a chart row. In case `n_col`
    # is set to four, this means that we end up with nine chart rows each
    # holding four charts and one last chart row holding the remaining two charts.

    # Create list of smaller chart lists from l_chart.
    l_l_chart = [
        
        l_chart[i:i+n_col] 
        
        for i in range(0, len(l_chart), n_col)
    ]

    # Now, we can plot the 38 panels on a canvas. Note, the '*' operator is used to unpack a list.
    alt1 = alt.vconcat(*[alt.hconcat(*row) for row in l_l_chart])

    display(alt1)


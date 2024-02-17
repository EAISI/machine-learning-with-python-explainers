# Import module.
import numpy as np
import altair as alt


# Define function
def f_heatmap(
        df_input,
        l_df_names,
        b_add_corr    = True,
        n_font_size   = 12,
        n_canvas_size = 600
    ):

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

    df_corr = (
        
        # Take subset of data.
        df_input[l_df_names]

        # Calculate Pearson correlation coefficient
        # between each variable in the subset.
        .corr(method='pearson')#.round(2) # This is alternative to alt.Text('corr', format='.2f')

        # Reset the index. By not dropping the index, 
        # the original index becomes a column 
        .reset_index(drop=False)

        # Convert the correlation matrix into a
        # long-form DataFrame
        .melt('index')

        # Rename columns for clarity
        .rename(
            columns={
                'index':    'var1',
                'variable': 'var2',
                'value':    'corr'}
        )
    )

    # Create the heatmap.
    alt1 = alt.Chart(df_corr).mark_rect().encode(
        x       = alt.X(
            'var1',
            axis = alt.Axis(
                labelFontSize = n_font_size,
                titleFontSize = n_font_size
            )
        ),
        y       = alt.Y(
            'var2',
            axis = alt.Axis(
                labelFontSize = n_font_size,
                titleFontSize = n_font_size
            )
        ), 
        color   = 'corr',
        tooltip = ['var1', 'var2', alt.Text('corr', format='.2f')],
    ).properties(
        height = n_canvas_size,
        width  = n_canvas_size,
        title  = "Heatmap of Variable Correlations"
    )

    # Add text label layer with font color adjusted for visibility.
    alt2 = alt1.mark_text().encode(

        text = alt.Text('corr', format='.2f'),  # Format text to show 2 decimal places

        # Conditional color to ensure text visibility against the rect color.
        color = alt.condition(
            alt.datum.corr > 0.8, 
            alt.value('white'),  # Use white text for high correlations for visibility
            alt.value('black')   # Use black text for low correlations for visibility
        )
    )

    if b_add_corr:

        # Show heatmap and correlation values (text).
        display(alt.layer(alt1, alt2))

    else:

        # Show only the heatmap, without the correlation values (text).
        display(alt1)


def f_get_chart(x):

    fig = alt.Chart(df_reduced).mark_circle(opacity=0.1).encode(
        x = x,
        y = 'SalePrice_log'
    ).properties(
        height = 200,
        width  = 200
    )

    return (
        
        fig + 
        
        fig
        .transform_regression(x, 'SalePrice_log', method="linear")
        .mark_line(color='red')
    )
    

l_chart = [f_get_chart(x) for x in l_df_X_names]


# We transform `l_chart` to a list of smaller chart lists (`l_l_chart`). Each chart list holds 
# a row of `n_col` charts. We create as many 'chart rows' until each of the 38 charts is in a 
# chart row. In the example below we set `n_col` to four. This means that we end up with nine 
# chart rows each holding four charts and one last chart row holding the remaining two charts.

# Number of chart columns on the canvas.
n_col   = 4

# Helper list holding the index of the first chart in each chart row.
l_helper = list(range(0, len(l_chart), n_col))

# Create list of smaller chart lists from l_chart.
l_l_chart = [
    
    l_chart[i:min(i+n_col, len(l_df_X_names))] 
    
    for i in l_helper
]

# To explain what the script does.
print(l_helper)
l_l_chart[:2] # Just to see the first two chart rows.


# Now, we can plot the 38 panels on a canvas. Note, the '*' operator is used to unpack a list.
alt.vconcat(*[alt.hconcat(*row) for row in l_l_chart])





#### This I tried but trend line did not work:
def f_create_chart_row1(df_data, l_col):

    # Define the base scatter plot
    base_scatter = (
        alt.Chart(df_data)
        .mark_point()
        .encode(
            x=alt.X(alt.repeat("column"), type='quantitative'),
            y=alt.Y(alt.repeat("row"), type='quantitative')
        )
    )

    # Define the regression line
    regression_line = (
        alt.Chart()
        .transform_regression('x', 'y')
        .mark_line(color='red')
        .encode(
            x=alt.X(alt.repeat("column"), type='quantitative'),
            y=alt.Y(alt.repeat("row"), type='quantitative')
        )
    )

    # Combine the plots using layer and repeat
    combined_chart = (
        alt.layer(
            base_scatter,
            regression_line
        )
        .properties(width=200, height=200)
        .repeat(row=['SalePrice_log'], column=l_col)
    )

    return combined_chart

"""
The issue with your code is that the regression line chart does not have a data source specified, and its transform_regression function is incorrectly referencing 'x' and 'y' instead of the actual column names. The transform_regression function requires explicit column names for its inputs, not placeholders like 'x' and 'y'. Additionally, since you're using alt.repeat("column") and alt.repeat("row") in the encoding, these cannot be directly used in transform_regression as it expects actual column names from the dataframe.

Here's a corrected approach to include the regression line in your charts:

Specify the Data for the Regression Line: You need to specify the data source (df_data) for the regression line chart.
Correct the Usage of transform_regression: Use actual column names for the transform_regression method. However, because you're creating a repeated chart, you'll face a challenge directly using dynamic column names within the transform_regression method as it does not directly support the alt.repeat functionality.
Since you're generating a repeated chart and wish to include a regression line for each scatter plot, you need to modify your approach to dynamically create regression lines based on the columns being plotted. A common workaround for this limitation involves creating individual charts for each combination of x and y and then combining them. However, this is more complex and might not be directly achievable with the simple use of alt.repeat.

Given the limitations of Altair's repeat functionality with respect to transformations like regression, you may need to individually plot each pair of variables (each x, y combination) if you want to include a regression line that dynamically adjusts based on the column selected. This typically involves a more manual process of creating charts or using a loop to generate them programmatically.

If you can specify which columns you're trying to plot or if your use case can be adjusted to explicitly name columns instead of using alt.repeat, I can provide a more tailored example of how to include a regression line for your scatter plots.
"""
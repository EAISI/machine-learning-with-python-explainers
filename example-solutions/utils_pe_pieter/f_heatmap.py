# Import module.
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns


# Define function
def f_heatmap(
        df_input,
        v_features_to_show,
        b_add_annotate     = True,
        n_font_size        = 15
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

    plt.rcParams['figure.figsize'] = (15, 15)
    
    df_cor = df_input[v_features_to_show].corr()
    
    m_matrix = np.triu(df_cor)

    sns.heatmap(        
        data      = df_cor,
        annot     = b_add_annotate,
        annot_kws = {'size': n_font_size},
        square    = True,
        cmap      = 'coolwarm',
        mask      = m_matrix
    );

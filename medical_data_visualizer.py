import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column
df['overweight'] = df['weight']*10000/df['height']**2 > 25

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholestorol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df.loc[df['cholesterol'] == 1, 'cholesterol'] = 0
df.loc[df['cholesterol'] > 1, 'cholesterol'] = 1
df.loc[df['gluc'] == 1, 'gluc'] = 0
df.loc[df['gluc'] > 1, 'gluc'] = 1

# Draw Categorical Plot


def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = df.melt(id_vars=df.columns.values[12], value_vars=df.columns.values[[
                     7, 8, 9, 10, 11, 13]])
    df_cat["total"] = 1

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the collumns for the catplot to work correctly.
    df_cat = pd.DataFrame(df_cat.groupby(
        ["cardio", "variable", "value"]).sum().reset_index())

    fig = sns.catplot(data=df_cat, kind='bar', x='variable',
                      y='total', hue='value', col='cardio')

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) & (df['height'] >= df['height'].quantile(0.025)) & (df["height"] <= df['height'].quantile(
        0.975)) & (df['weight'] >= df['weight'].quantile(0.025)) & (df["weight"] <= df['weight'].quantile(0.975))]

    # Calculate the correlation matrix
    corr = df_heat.corr().astype('float').round(1)

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr))

    # Set up the matplotlib figure
    fig, ax = plt.subplots()

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr, mask=mask, annot=True)

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig

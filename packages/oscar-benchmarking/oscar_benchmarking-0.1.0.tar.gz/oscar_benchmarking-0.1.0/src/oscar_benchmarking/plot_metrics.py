"""
This script plots the performance metrics from the SQL database using matplotlib.

Requirements:
- pandas 2.2.2
- matplotlib 3.9.0
"""

import pandas as pd
import sqlite3
import os
import matplotlib.pyplot as plt
import argparse

DATABASE_PATH = os.path.abspath("/oscar/data/shared/eval_gracehopper/results/performance.sqlite3")

# Configure parser
parser = argparse.ArgumentParser(
    prog='PlotMetrics',
    description='Plots the MLPerf metrics from sqlite3 database'
)
parser.add_argument('--model', help='Model for which to plot metrics')

# Get the command-line arguments
args = parser.parse_args()

# Establish a connection to the sqlite3 db + read the db into a pandas dataframe
with sqlite3.connect(DATABASE_PATH) as dbcon:
    df = pd.read_sql_query("SELECT * FROM perfmetrics", dbcon)

# Convert metrics into columns for each run ID
run_metrics = df[['RUN_ID', 'METRIC', 'VALUE']].pivot(index='RUN_ID', columns='METRIC', values='VALUE')

# Group by run ID
unique_runs_gb = df[['BENCH_MARK', 'ARCH', 'MODEL', 'BACKEND']].groupby(df['RUN_ID'])
unique_runs = unique_runs_gb.aggregate({'BENCH_MARK': 'first', 'ARCH': 'first', 'MODEL': 'first', 'BACKEND': 'first'})

# Achieved desired table form to plot on X-Y plane
plot_df = unique_runs.join(run_metrics, on='RUN_ID')

def subplot_model_metrics(df: pd.DataFrame, x: str, args):
    """
    Plots the metrics for the model specified by the '--model' argument.
    If this argument doesn't exist, then input df should already contain one model.
    """
    figure, axis = plt.subplots(2,2)
    if args.model:
        df = df[df['MODEL'].str.contains(args.model)]
    df.plot(x=x, y='MAX_LATENCY_NS', ax=axis[0,0], kind='bar')
    axis[0,0].set_title("Max Latency (S)")
    axis[0,0].tick_params(axis='x', labelrotation=0)

    df.plot(x=x, y='MEAN_LATENCY_NS', ax=axis[0,1], kind='bar')
    axis[0,1].set_title("Mean Latency (S)")
    axis[0,1].tick_params(axis='x', labelrotation=0)

    df.plot(x=x, y='MIN_LATENCY_NS', ax=axis[1,0], kind='bar')
    axis[1,0].set_title("Min Latency (S)")
    axis[1,0].tick_params(axis='x', labelrotation=0)

    df.plot(x=x, y='SAMPLES_PER_SECOND', ax=axis[1,1], kind='bar')
    axis[1,1].set_title("Samples Per Second")
    axis[1,1].tick_params(axis='x', labelrotation=0)

# Plot the metrics for each run
if args.model:
    subplot_model_metrics(plot_df, 'ARCH', args)
else:
    # Otherwise, show the average of the model across all architectures for each metric
    model_gb_plot_df = plot_df[['MODEL', 'MAX_LATENCY_NS', 'MEAN_LATENCY_NS', 'MIN_LATENCY_NS', 'SAMPLES_PER_SECOND']].groupby(plot_df['MODEL']).agg({'MODEL': 'first', 'MAX_LATENCY_NS': 'mean', 'MEAN_LATENCY_NS': 'mean', 'MIN_LATENCY_NS': 'mean', 'SAMPLES_PER_SECOND': 'mean'})
    num_models = model_gb_plot_df['MODEL'].size
    subplot_model_metrics(model_gb_plot_df, 'MODEL', args)

# Adjust subplots for better viewing experience
plt.subplots_adjust(hspace=0.5)
# plt.subplot_tool() # Use this tool to adjust subplot spacing to your liking
plt.show()
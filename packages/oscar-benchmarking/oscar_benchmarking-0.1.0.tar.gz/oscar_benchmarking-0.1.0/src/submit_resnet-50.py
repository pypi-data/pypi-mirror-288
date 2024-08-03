"""
This script creates a batch script that submits jobs to Slurm to run the MLPerf inference benchmarks.
"""

# python python-scripts/submit_resnet-50.py -d /oscar/data/ccvinter/mstu/gracehopper_eval/MLPerf_gpu/gh200_resnet-50 -i /oscar/data/shared/eval_gracehopper/container_images/MLPerf/arm64/mlperf-resnet-50-tf-arm64 --data /oscar/data/ccvinter/mstu/gracehopper_eval/data/imagenet/ILSVRC2012/val

# python python-scripts/submit_resnet-50.py -d /oscar/data/ccvinter/mstu/gracehopper_eval/MLPerf_gpu/gh200_resnet-50 -i /oscar/data/shared/eval_gracehopper/container_images/MLPerf/x86_64/mlperf-resnet-50-tf-x86_64 --data /oscar/data/ccvinter/mstu/gracehopper_eval/data/imagenet/ILSVRC2012/val

import os
import argparse
from oscar_benchmarking import SlurmJobSubmitter
from oscar_benchmarking import SlurmScriptGenerator
import pandas as pd
import yaml
from datetime import datetime

# Read the YAML file
try:
    with open("config.yaml", 'r') as file:
        general_params = yaml.safe_load(file) # Returns None, if file is empty
except OSError as e:
    raise e

# Parse the CSV
run_config_df = pd.read_csv("run_config.csv")

# Get the working directory + user from ENV
PWD = os.environ.get('PWD')
USER = os.environ.get('USER')

# Configure CLI
parser = argparse.ArgumentParser(prog="submit_resnet-50", description=__doc__)
parser.add_argument("-d", "--destination", 
                    dest="destination",
                    metavar="DIR",
                    help="Directory in which to run the script (default: '.')",
                    default=PWD)
args = parser.parse_args()

# Loop through each run configuration in the CSV
for _, run in run_config_df.iterrows():
    # Parameters for the current run
    RUN_ID = run["RUN_ID"]
    BENCHMARK = run["BENCHMARK"]
    MODEL = run["MODEL"]
    BACKEND = run["BACKEND"]
    ARCH = run["ARCH"]

    print(RUN_ID, BENCHMARK, MODEL, BACKEND, ARCH)

    # Get model args
    DESTINATION =       general_params["destination"]
    NUM_RUNS =          general_params["num_runs"]
    DATA_PATH =         general_params["model"][MODEL]["data_path"]
    CONTAINER_IMAGE =   general_params["arch"][ARCH]["container_image"]

    # Define the output script path
    BATCH_PATH = os.path.join(os.path.join(DESTINATION, "scripts"), f'{RUN_ID}_{BENCHMARK}_{MODEL}_{datetime.now().strftime("%Y%m%d")}.submit') # FIXME: refactor variable to remove os path joining

    slurm_script_writer = SlurmScriptGenerator.MLPerfScriptWriter(RUN_ID, BENCHMARK, MODEL, BACKEND, ARCH, container_image=CONTAINER_IMAGE, data_path=DATA_PATH)

    # Make directories necessary for this script to run
    slurm_script_writer.make_dirs()

    # Batch Variables
    NODES =             general_params["arch"][ARCH]["nodes"]
    PARTITION =         general_params["arch"][ARCH]["partition"]
    GRES =              general_params["arch"][ARCH]["gres"]
    ACCOUNT =           general_params["arch"][ARCH]["account"]
    NTASKS_PER_NODE =   general_params["arch"][ARCH]["ntasks_per_node"]
    MEMORY =            general_params["arch"][ARCH]["memory"]
    TIME =              general_params["arch"][ARCH]["time"]
    ERROR_FILE_NAME =   general_params["arch"][ARCH]["error_file_name"]
    OUTPUT_FILE_NAME =  general_params["arch"][ARCH]["output_file_name"]

    # Configure the logger
    logger = slurm_script_writer.config_logger()

    # Log important info
    logger.info("Command-line arguments:")
    for arg, val in vars(args).items():
        logger.info(f"{arg}: {val}")

    # Generate script body
    script_body = slurm_script_writer.generate_script_body()

    slurm_job_submitter = SlurmJobSubmitter.MLPerfJobSubmitter(script_path=BATCH_PATH,
                                        nodes=NODES, 
                                        gres=GRES, 
                                        ntasks_per_node=NTASKS_PER_NODE, 
                                        memory=MEMORY, 
                                        time=TIME, 
                                        partition=PARTITION, 
                                        error_file_name=ERROR_FILE_NAME, 
                                        output_file_name=OUTPUT_FILE_NAME, 
                                        account=ACCOUNT,
                                        num_runs=NUM_RUNS)
    slurm_job_submitter.submit(script_body)

    # Log successful submission
    logger.info("Batch script submitted successfully.\n")
# Scrape performance metrics from MLPerf inference results
# Metrics: 
# Accuracy, 
# Latency, 
# Throughput (results_samples_per_second), 
# Inference Time, 
# Memory Usage

import os
import re
import json
import sqlite3
import argparse
import logging

logging.basicConfig(filename='scrape_metrics_log.txt', 
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        )
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(
        prog='PerfMetrics',
        description='Gets the MLPerf metrics from input folder and adds to sqlite3 database',
        epilog='Need to manually edit the metric for now')

parser.add_argument('file', help='path to mlperf_log_detail.txt')
parser.add_argument('--runid', help='ID of your benchmark run')
parser.add_argument('--benchmark', help='Name of the benchmark')
parser.add_argument('--model', help='Model name')
parser.add_argument('--backend', help='Backend used, pytorch, tf, etc')
parser.add_argument('--arch', help='Architecture, x86_64 or arm64')

# Get the command-line arguments
args = parser.parse_args()

# Set databae and outfile
database = os.path.abspath("/oscar/data/shared/eval_gracehopper/results/performance.sqlite3")
outfile = os.path.join(args.file)

# Log args
logger.info('Database path: %s\n' %str(database))
logger.info('Command-line arguments:')
for arg, val in vars(args).items():
    logger.info(f'{arg}: {val}')


# Write to database: update values here
def write_db(metric, value, database, args=args):
    # Database info
    perfmetrics = {}
    perfmetrics['RUN_ID'] = args.runid
    perfmetrics['BENCH_MARK'] = args.benchmark
    perfmetrics['ARCH'] = args.arch
    perfmetrics['MODEL'] = args.model
    perfmetrics['BACKEND'] = args.backend
    perfmetrics['METRIC'] = metric
    perfmetrics['VALUE'] = value
    
    # Connect to database
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # Insert queries
    keys = ', '.join(perfmetrics.keys())
    placeholders = ', '.join(['?' for _ in range(len(perfmetrics))])
    values = tuple(perfmetrics.values())

    insert_query = f"INSERT INTO perfmetrics ({keys}) VALUES ({placeholders})"
    cursor.execute(insert_query, values)

    conn.commit()
    conn.close()



def parse_file(fname):
    data = []
    dict2 = {}
    with open(fname, 'r') as file:
        text = file.read()
        matches = re.findall(r':::MLLOG\s+(\{.*?\})', text)
        #return matches
        for match in matches:
            match += '}'
            entry = json.loads(match) # convert string to dictionary

            data.append(entry)

            key = entry.get('key')
            val = entry.get('value')
            if key and val:
                dict2[key] = val
    
    return dict2

# Get the results
results = parse_file(outfile)

# Write results to database
write_db('SAMPLES_PER_SECOND', results['result_samples_per_second'], database)
write_db('MIN_LATENCY_NS', results['result_min_latency_ns'], database)
write_db('MAX_LATENCY_NS', results['result_max_latency_ns'], database)
write_db('MEAN_LATENCY_NS', results['result_mean_latency_ns'], database)

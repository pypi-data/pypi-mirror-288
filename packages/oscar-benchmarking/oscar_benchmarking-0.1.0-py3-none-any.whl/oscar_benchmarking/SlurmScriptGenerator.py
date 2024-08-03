import os
import logging
from typing import List
import re
import pandas as pd
import subprocess
from io import StringIO
from abc import ABC, abstractmethod
import yaml

class SlurmScriptWriter(ABC):
    """
    This abstract base class is a template for script-writing classes that writes the body of Slurm scripts.
    """

    @abstractmethod
    def generate_script_body(self) -> List[str]:
        """
        Generates the body of the script. Returns a List of lines as strings.
        """
        pass

class MLPerfScriptWriter(SlurmScriptWriter):
    """
    Writes the script body for MLPerf scripts.
    """

    def __init__(self, 
                 run_id: int, 
                 benchmark: str, 
                 model: str, 
                 backend: str, 
                 arch: str,
                 container_image: str, 
                 data_path: str,
                 destination: str = None) -> None:
        """
        Initialize relevants variables for writing an MLPerf script.

        Args:
            run_id (int): Unique ID of this benchmark run
            benchmark (str): Type of benchmark
            model (str): Name of model (e.g. resnet50, bert99, etc.)
            backend (str): Backend of the model (e.g. tf, torch)
            arch (str): GPU architecture (e.g. gh200, h100, etc.)
            container_image (str): Path to pre-configured Apptainer image
            data_path (str): Path to dataset
            destination (str, optional): Path to where the script and files are located
        """
        # Get relevant environment variables
        self.PWD = os.environ.get('PWD')
        self.USER = os.environ.get('USER')

        self.RUN_ID = run_id

        # Validate + assign model parameters
        if not benchmark:
            raise ValueError("Invalid input for `benchmark`. Cannot be an empty string.")
        self.BENCHMARK = benchmark

        if not model:
            raise ValueError("Invalid input for `model`. Cannot be an empty string.")
        self.MODEL = model

        if not backend:
            raise ValueError("Invalid input for `backend`. Cannot be an empty string.")
        self.BACKEND = backend

        if not arch:
            raise ValueError("Invalid input for `arch`. Cannot be an empty string.")
        self.ARCH = arch

        # Initialize the directory for output files + directories
        # FIXME: Get rid of `destination` variable, if it becomes unnecessary
        if destination:
            self.DEST = destination
        else:
            self.DEST = self.PWD
        self.RESULTS_DIR = os.path.join(self.DEST, "results")
        self.SLURM_OUTPUT_DIR = os.path.join(self.DEST, "slurm_out")
        self.SLURM_ERROR_DIR = os.path.join(self.DEST, "slurm_err")
        self.LOG_DIR = os.path.join(self.DEST, "submit_log")
        self.SCRIPT_DIR = os.path.join(self.DEST, "scripts")
        self.OUTFILE = os.path.join(self.DEST, "test_results/default-reference-gpu-tf-v2.15.0-default_config/resnet50/offline/performance/run_1/mlperf_log_detail.txt")
        
        # Validate + assign path inputs
        # if not os.path.exists(container_image):
        #     raise ValueError("A valid container image must be specified.")
        self.CONTAINER_IMAGE = container_image

        # if not os.path.exists(data_path):
        #     raise ValueError("A valid path to dataset must be specified.")
        self.DATA_PATH = data_path

        # Initialize other relevant paths
        self.SCRAPE_METRICS_PATH = os.path.join(self.PWD, "scrape_metrics.py")
        self.YAML_PATH = os.path.join(self.PWD, "config.yaml")

        # Read the YAML file
        try:
            with open(self.YAML_PATH, 'r') as file:
                yaml_params = yaml.safe_load(file) # Returns None, if file is empty
        except OSError as e:
            raise e
        
        # Initialize model-specific variables
        model_config = yaml_params["model"][model]
        self.HW_NAME            = model_config["hw_name"]
        self.IMPLEMENTATION     = model_config["implementation"]
        self.DEVICE             = model_config["device"]
        self.SCENARIO           = model_config["scenario"]
        self.ADR_COMPILER_TAGS  = model_config["adr.compiler.tags"]
        self.TARGET_QPS         = model_config["target_qps"]
        self.CATEGORY           = model_config["category"]
        self.DIVISION           = model_config["division"]

    def get_slurm_args(self, args) -> None:
        """
        Read the slurm arguments and check if they are valid.
        """
        pass

    def make_dirs(self) -> None:
        """
        This function will check if folder exists or not,
        and create them. $PWD/results, $PWD/slurm_err,
        $PWD/slurm_out, $PWD/submit_log
        """
        # TODO: Log if folder exists.
        os.makedirs(self.RESULTS_DIR, exist_ok=True) # emulates 'mkdir -p' Linux command
        os.makedirs(self.SLURM_OUTPUT_DIR, exist_ok=True)
        os.makedirs(self.SLURM_ERROR_DIR, exist_ok=True)
        os.makedirs(self.LOG_DIR, exist_ok=True)
        os.makedirs(self.SCRIPT_DIR, exist_ok=True)
    
    def config_logger(self) -> logging.Logger:
        """
        This function configures the logger.
        """
        LOG_PATH = os.path.join(self.LOG_DIR, "submit_benchmarks_log.txt")
        logging.basicConfig(filename=LOG_PATH,
                            level=logging.INFO,
                            format="%(asctime)s - %(levelname)s: %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S")
        logger = logging.getLogger(__name__)
        return logger            
    
    def generate_script_body(self) -> List[str]:
        """
        This function will create the sbatch file.

        No arguments (e.g., number of nodes, model name, etc)
        should be specified inside this function. All of them
        should be inherited.
		"""
        return [
            # 'echo "Hello World"\n',
            'unset LD_LIBRARY_PATH\n',
            f'export APPTAINER_BINDPATH="/oscar/home/{self.USER}, /oscar/scratch/{self.USER}, /oscar/data"\n',
            'export APPTAINER_CACHEDIR=/tmp\n',
            '\n',
            'echo $SLURM_JOBID\n',
            '\n',
            f"srun apptainer exec --nv {self.CONTAINER_IMAGE} sh << 'EOF'\n" ,
            'export CM_REPOS=/tmp/CM\n',
            'cp -r /CM /tmp/.\n',
            '\n',
            f'cm run script "get validation dataset imagenet _2012 _full" --input={self.DATA_PATH}\n',
            f'cmr "run mlperf inference generate-run-cmds _submission" --quiet --submitter="MLCommons" --hw_name={self.HW_NAME} --model={self.MODEL} --implementation={self.IMPLEMENTATION} --backend={self.BACKEND} --device={self.DEVICE} --scenario={self.SCENARIO} --adr.compiler.tags={self.ADR_COMPILER_TAGS} --target_qps={self.TARGET_QPS} --category={self.CATEGORY} --division={self.DIVISION} --results_dir={self.RESULTS_DIR}\n',
            'EOF\n',
            '\n',
            # Move Slurm output files into directories
            f"mv *.out {self.SLURM_OUTPUT_DIR}\n",
            f"mv *.err {self.SLURM_ERROR_DIR}\n",
        ] # + self.scrape_metrics()
    
    def scrape_metrics(self) -> List[str]:
        """
        This function runs the scrape_metrics script.
        """
        return [
            # Save results to sqlite3 database
            f'python {self.SCRAPE_METRICS_PATH} {self.OUTFILE} --runid={self.RUN_ID} --benchmark={self.BENCHMARK} --model={self.MODEL} --backend={self.BACKEND} --arch={self.ARCH}\n'
        ]
        
    def slurm_input(self) -> List[int]:
        """
        Read input from slurm commands like sfeature and
        get the actual list of gpus to submit to.
        """
        # Create text file of the sfeature output
        try:
            result = subprocess.run(args=["sinfo", "-o", r"%N %P %c %m %f %G"], 
                                    shell=False, 
                                    capture_output=True, 
                                    text=True, 
                                    check=True) # check=True throws subprocess.CalledProcessError, if exits with code > 0
        except subprocess.CalledProcessError as e:
            print(e)

        # Read the output from sinfo into a pandas DataFrame
        df = pd.read_table(StringIO(result.stdout), delimiter=' ')

        # Extract the gpus
        gpus_df = df.loc[df["PARTITION"] == "gpu"]
        gpus_df.reset_index(drop=True, inplace=True)

        # Get the nodelist column
        nodelists = gpus_df["NODELIST"]
        node_list = []

        # Get a list of all the nodes
        pattern = re.compile(r'\[([^\[\]]+)\]') # Regex for strings enclosed in square brackets
        for nodelist in nodelists:
            stripped_node = nodelist.strip("gpu")
            match = pattern.search(stripped_node)
            if match:
                enclosed_string = match.group(1)
                items = enclosed_string.split(',')

                for item in items:
                    if '-' in item:
                        start, end = map(int, item.split('-'))
                        node_list.extend(range(start, end + 1))
                    else:
                        node_list.append(int(item))
            else:
                node_list.append(int(stripped_node))
        
        return node_list
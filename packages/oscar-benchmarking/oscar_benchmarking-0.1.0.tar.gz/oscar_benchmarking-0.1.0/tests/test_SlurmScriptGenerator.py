"""
TEST: 
- 
"""

import pytest
from SlurmJobSubmitter import MLPerfJobSubmitter
import os

@pytest.fixture
def pwd():
    return os.environ.get("PWD")

@pytest.fixture
def script_body():
    return ['echo "Hello World"\n']

@pytest.fixture(autouse=True)
def test_script(pwd, script_body):
    """
    Submits a test script and returns the script path.
    """
    script_path = os.path.join(pwd, "test")
    example = MLPerfJobSubmitter(script_path=script_path,
                                 nodes=1,
                                 gres="gpu:1",
                                 ntasks_per_node=1,
                                 memory="40G",
                                 time="01:00:00",
                                 partition="gracehopper",
                                 account="ccv-gh200-gcondo",
                                 num_runs=1)
    print(len(script_body), script_body)
    example.submit(script_body)
    yield script_path
    os.remove(script_path)

# TEST: '#!/bin/bash is written at the top of the file
def test_submit_bash_annotation(test_script):
    with open(test_script, 'r') as file:
        file_lines = file.readlines()
        assert (file_lines[0] == "#!/bin/bash\n")

# TEST: All necessary SBATCH header lines are written
def test_submit_sbatch_header(test_script):
    correct_header = [
        '#SBATCH --nodes=1\n',
        '#SBATCH -p gracehopper\n',
        '#SBATCH --gres=gpu:1\n',
        '#SBATCH --account=ccv-gh200-gcondo\n',
        '#SBATCH --ntasks-per-node=1\n',
        '#SBATCH --mem=40G\n',
        '#SBATCH -t 01:00:00\n',
        '#SBATCH -e %j.err\n',
        '#SBATCH -o %j.out\n',
    ]
    with open(test_script, 'r') as file:
        file_lines = file.readlines()
        assert any(file_lines[i:i+len(correct_header)] == correct_header for i in range(len(file_lines) - len(correct_header)))

# TEST: Script body is successfully written to script
def test_submit_body(test_script, script_body):
    with open(test_script, 'r') as file:
        file_lines = file.readlines()
        assert any(file_lines[i:i+len(script_body)] == script_body for i in range(len(file_lines) - len(script_body) + 1))

# TEST: Output directories are successfully created
def test_output_folders_exist(pwd):
    assert os.path.exists(os.path.join(pwd, "results"))
    assert os.path.exists(os.path.join(pwd, "scripts"))
    assert os.path.exists(os.path.join(pwd, "slurm_err"))
    assert os.path.exists(os.path.join(pwd, "slurm_out"))
    assert os.path.exists(os.path.join(pwd, "submit_log"))
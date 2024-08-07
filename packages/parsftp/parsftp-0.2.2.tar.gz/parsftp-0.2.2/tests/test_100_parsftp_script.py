# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import os
import shutil
import subprocess
import yaml

# Test folders
script_path = os.path.realpath(__file__)
testdir = os.path.dirname(script_path)
WRK_DIR = os.path.join(testdir, 'wrk')

# Script command
cmd = ['python', '-c', 'import parsftp; parsftp.main()']

def test_help() -> None:
    for opt in ['-h', '--help']:
        with subprocess.Popen(cmd + [opt], stdout=subprocess.PIPE) as proc:
            assert proc.wait() == 0

def test_no_yaml() -> None:

    # Create folders
    wrkdir = os.path.join(WRK_DIR, "test_no_yaml")
    shutil.rmtree(wrkdir, ignore_errors=True)
    os.makedirs(wrkdir)

    # run process
    output_yaml = os.path.join(wrkdir, "output.yml")
    with subprocess.Popen(cmd + ["-o", output_yaml],
                          stdout=subprocess.PIPE) as proc:
        assert proc.wait() != 0

def test_one_yaml_no_file() -> None:

    # Create folders
    wrkdir = os.path.join(WRK_DIR, "test_one_yaml_no_file")
    shutil.rmtree(wrkdir, ignore_errors=True)
    os.makedirs(wrkdir)
    output_dir = os.path.join(wrkdir, "output")
    os.makedirs(output_dir)

    # Create input YAML
    input_yaml = os.path.join(wrkdir, "input.yml")
    in_files = {"batch1": {"input": [], "output": output_dir}}
    with open(input_yaml, "w", encoding="utf8") as f:
        yaml.safe_dump_all([in_files], f, explicit_start=True)

    # Run process
    output_yaml = os.path.join(wrkdir, "output.yml")
    with subprocess.Popen(cmd + ["-i", input_yaml, "-o", output_yaml],
                          stdout=subprocess.PIPE) as proc:
        assert proc.wait() == 0

    # Check output YAML
    with open(output_yaml, "r", encoding="utf8") as f:
        docs = list(yaml.safe_load_all(f))
        assert len(docs) == 1
        assert "batch1" in docs[0]
        assert docs[0]["batch1"] != 0

def test_one_yaml_one_file() -> None:

    # Create folders
    wrkdir = os.path.join(WRK_DIR, "test_one_yaml_one_file")
    output_dir = os.path.join(wrkdir, "output")
    shutil.rmtree(wrkdir, ignore_errors=True)
    os.makedirs(wrkdir)
    os.makedirs(output_dir)

    # Create file to transfer
    myfile = os.path.join(wrkdir, "myfile.txt")
    with open(myfile, "w", encoding="utf8") as f:
        f.write("Hi!\n")

    # Create input YAML
    input_yaml = os.path.join(wrkdir, "input.yml")
    in_files = {"batch1": {"input": [myfile], "output": output_dir}}
    with open(input_yaml, "w", encoding="utf8") as f:
        yaml.safe_dump_all([in_files], f, explicit_start=True)

    # Run process
    output_yaml = os.path.join(wrkdir, "output.yml")
    with subprocess.Popen(cmd + ["-i", input_yaml, "-o", output_yaml],
                          stdout=subprocess.PIPE) as proc:
        assert proc.wait() == 0

    # Check output YAML
    with open(output_yaml, "r", encoding="utf8") as f:
        docs = list(yaml.safe_load_all(f))
        assert len(docs) == 1
        assert "batch1" in docs[0]
        assert docs[0]["batch1"] == 0

def test_passing_args_to_treesftp() -> None:

    # Create folders
    wrkdir = os.path.join(WRK_DIR, "test_passing_args_to_treesftp")
    output_dir = os.path.join(wrkdir, "output")
    shutil.rmtree(wrkdir, ignore_errors=True)
    os.makedirs(wrkdir)

    # Create input YAML
    input_yaml = os.path.join(wrkdir, "input.yml")
    in_files = {"batch1": {"input": ['non_existing_file'],
                           "output": output_dir}}
    with open(input_yaml, "w", encoding="utf8") as f:
        yaml.safe_dump_all([in_files], f, explicit_start=True)

    # Run process
    output_yaml = os.path.join(wrkdir, "output.yml")
    with subprocess.Popen(cmd + ["-i", input_yaml, "-o", output_yaml, "--",
                                 "--dryrun"],
                          stdout=subprocess.PIPE) as proc:
        assert proc.wait() == 0

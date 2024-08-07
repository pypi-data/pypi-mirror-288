# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import os
import shutil

import parsftp

# Test folders
script_path = os.path.realpath(__file__)
testdir = os.path.dirname(script_path)
WRK_DIR = os.path.join(testdir, 'wrk')

def test_no_batches() -> None:
    trans = parsftp.ParSftp()
    trans.run()
    assert trans.status == 0
    # pylint: disable-next=use-implicit-booleaness-not-comparison
    assert trans.get_batch_statuses() == {}

def test_one_batch_no_file() -> None:
    trans = parsftp.ParSftp()
    trans.add_batch(parsftp.Batch(name = "a", input_paths = [],
                                  output_dir = "output"))
    trans.run()
    assert trans.status == 1
    assert trans.get_batch_statuses()["a"] != 0

def test_one_batch_one_non_existing_file() -> None:
    trans = parsftp.ParSftp()
    trans.add_batch(parsftp.Batch(name = "a", input_paths = ["a.txt"],
                                  output_dir = "output"))
    trans.run()
    assert trans.status == 1
    assert trans.get_batch_statuses()["a"] != 0

def test_one_batch_one_file_no_output_dir() -> None:

    # Create folders
    wrkdir = os.path.join(WRK_DIR, "test_one_batch_one_file_no_output_dir")
    output_dir = os.path.join(wrkdir, "output")
    shutil.rmtree(wrkdir, ignore_errors=True)
    os.makedirs(wrkdir)

    # Create file to transfer
    myfile = os.path.join(wrkdir, "a.txt")
    with open(myfile, "w", encoding="utf8") as f:
        f.write("Hi!\n")

    # Transfer
    trans = parsftp.ParSftp()
    trans.add_batch(parsftp.Batch(name = "a", input_paths = [myfile],
                                  output_dir = output_dir))
    trans.run()
    assert trans.status == 0
    assert trans.get_batch_statuses() == {"a": 0}

def test_one_batch_one_file() -> None:

    # Create folders
    wrkdir = os.path.join(WRK_DIR, "test_one_batch_one_file")
    output_dir = os.path.join(wrkdir, "output")
    shutil.rmtree(wrkdir, ignore_errors=True)
    os.makedirs(output_dir)

    # Create file to transfer
    myfile = os.path.join(wrkdir, "a.txt")
    with open(myfile, "w", encoding="utf8") as f:
        f.write("Hi!\n")

    # Transfer
    trans = parsftp.ParSftp()
    trans.add_batch(parsftp.Batch(name = "a", input_paths = [myfile],
                                  output_dir = output_dir))
    trans.run()
    assert trans.status == 0
    assert trans.get_batch_statuses() == {"a": 0}
    assert os.path.exists(os.path.join(output_dir, os.path.basename(myfile)))

def test_one_batch_two_files() -> None:

    # Create folders
    wrkdir = os.path.join(WRK_DIR, "test_one_batch_two_files")
    output_dir = os.path.join(wrkdir, "output")
    shutil.rmtree(wrkdir, ignore_errors=True)
    os.makedirs(output_dir)

    # create files to transfer
    files = []
    for fname in ["a.txt", "b.csv"]:
        file = os.path.join(wrkdir, fname)
        with open(file, "w", encoding="utf8") as f:
            f.write(f"hi! it's file {fname}.\n")
        files.append(file)

    # Transfer
    trans = parsftp.ParSftp()
    trans.add_batch(parsftp.Batch(name = "a", input_paths = files,
                                  output_dir = output_dir))
    trans.run()
    assert trans.status == 0
    assert trans.get_batch_statuses() == {"a": 0}
    for file in files:
        assert os.path.exists(os.path.join(output_dir, os.path.basename(file)))

def test_two_batches_two_files() -> None:

    # Create folders
    wrkdir = os.path.join(WRK_DIR, "test_two_batch_two_files")
    output_dir = os.path.join(wrkdir, "output")
    shutil.rmtree(wrkdir, ignore_errors=True)
    os.makedirs(output_dir)

    # create files to transfer
    files = []
    for fname in ["a.txt", "b.csv"]:
        file = os.path.join(wrkdir, fname)
        with open(file, "w", encoding="utf8") as f:
            f.write(f"hi! it's file {fname}.\n")
        files.append(file)

    # Transfer
    trans = parsftp.ParSftp()
    trans.add_batch(parsftp.Batch(name = "a", input_paths = [files[0]],
                                  output_dir = output_dir))
    trans.add_batch(parsftp.Batch(name = "b", input_paths = [files[1]],
                                  output_dir = output_dir))
    trans.run()
    assert trans.status == 0
    assert trans.get_batch_statuses() == {"a": 0, "b": 0}
    for file in files:
        assert os.path.exists(os.path.join(output_dir, os.path.basename(file)))

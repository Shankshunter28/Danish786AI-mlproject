import os
import tempfile
import shutil
import importlib.util

import pandas as pd


def load_module_from_path(path, module_name="data_ingestion"):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_data_ingestion_creates_train_test_files():
    tmpdir = tempfile.mkdtemp()
    try:
        # create a small sample csv
        sample_csv = os.path.join(tmpdir, "sample.csv")
        df = pd.DataFrame({"a": range(100), "b": range(100, 200)})
        df.to_csv(sample_csv, index=False)

        # load the data_ingestion module directly by path to avoid package import issues
        module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data_ingestion.py"))
        module_path = os.path.normpath(module_path)
        module = load_module_from_path(module_path)

        DataIngestionConfig = getattr(module, "DataIngestionConfig")
        DataIngestion = getattr(module, "DataIngestion")

        artifact_dir = os.path.join(tmpdir, "artifacts")
        cfg = DataIngestionConfig(input_data_path=sample_csv, artifact_dir=artifact_dir, test_size=0.25, random_state=0)

        ing = DataIngestion(cfg)
        paths = ing.run()

        assert os.path.exists(paths["train_path"]), "train file was not created"
        assert os.path.exists(paths["test_path"]), "test file was not created"

        # Basic sanity: number of rows
        train_df = pd.read_csv(paths["train_path"]) 
        test_df = pd.read_csv(paths["test_path"]) 
        assert len(train_df) + len(test_df) == 100

    finally:
        shutil.rmtree(tmpdir)

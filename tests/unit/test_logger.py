import os
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from sci_watch.utils.logger import get_logger, logging_wrapper


def test_logging_wrapper(capsys):
    
    current_wd = os.getcwd()

    with TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)

        log_path = Path("logs", "test.log")
        test_logger = get_logger(__name__, log_file_path=log_path)

        @logging_wrapper(test_logger)
        def failable_function(fail: bool):
            local_logger = get_logger("localLogger", level="WARNING")
            if fail:
                raise ValueError("Something bad happened")
            else:
                local_logger.info("Function did not fail!")

        failable_function(fail=False)

        with pytest.raises(ValueError):
            failable_function(fail=True)
        
        assert log_path.exists()

        with log_path.open(encoding="utf-8") as fd:
            file_logs = fd.read()

        stderr_logs = capsys.readouterr().err

        for logs in (stderr_logs, file_logs):
            assert "INFO" not in logs
            assert logs.count("ERROR") == 1
            assert "Something bad happened" in logs 

        os.chdir(current_wd)

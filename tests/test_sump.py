import os
import tempfile
from click.testing import CliRunner
from sump.__main__ import main

def test_main():
    runner = CliRunner()
    with tempfile.TemporaryDirectory() as temp_dir:
        result = runner.invoke(main, [temp_dir])
        assert result.exit_code == 0
        assert os.path.exists(os.path.join(temp_dir, 'dump.txt'))

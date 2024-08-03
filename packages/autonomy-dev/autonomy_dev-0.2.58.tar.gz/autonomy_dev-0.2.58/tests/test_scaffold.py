"""Tests for the scaffold command"""

import subprocess
import sys
from pathlib import Path

import pytest
from aea.cli import cli as aea_cli

from auto_dev.cli import cli
from auto_dev.constants import DEFAULT_ENCODING
from auto_dev.protocols.scaffolder import read_protocol

FSM_SPEC = Path("auto_dev/data/fsm/fsm_specification.yaml").absolute()


@pytest.mark.skip(reason="Needs chain contracts update")
@pytest.mark.parametrize("spec", [None, FSM_SPEC])
def test_scaffold_fsm_with_aea_run(cli_runner, spec, dummy_agent_tim):
    """Test scaffold base FSM upto `aea run`."""

    command = ["scaffold", "fsm"]
    if spec:
        command.extend(["--spec", str(spec)])

    dummy_agent_tim.exists()
    result = cli_runner.invoke(cli, command)
    assert result.exit_code == 0, result.output

    assert (Path.cwd() / "vendor" / "valory" / "skills" / "abstract_abci").exists()
    assert (Path.cwd() / "vendor" / "valory" / "skills" / "abstract_round_abci").exists()
    assert (Path.cwd() / "vendor" / "valory" / "skills" / "registration_abci").exists()
    assert (Path.cwd() / "vendor" / "valory" / "skills" / "reset_pause_abci").exists()
    assert (Path.cwd() / "vendor" / "valory" / "skills" / "termination_abci").exists()

    result = cli_runner.invoke(aea_cli, ["run"])
    assert result.exit_code == 1
    assert "An error occurred during instantiation of connection valory" in result.output


def test_scaffold_protocol(cli_runner, dummy_agent_tim, caplog):
    """Test scaffold protocol"""

    path = Path.cwd() / ".." / "tests" / "data" / "dummy_protocol.yaml"
    command = ["scaffold", "protocol", str(path)]
    result = cli_runner.invoke(cli, command)

    assert result.exit_code == 0, result.output
    assert f"New protocol scaffolded at {dummy_agent_tim}" in caplog.text

    protocol = read_protocol(str(path))
    original_content = path.read_text(encoding=DEFAULT_ENCODING)
    readme_path = dummy_agent_tim / "protocols" / protocol.metadata["name"] / "README.md"
    assert original_content in readme_path.read_text(encoding=DEFAULT_ENCODING)


class TestScaffoldConnection:
    """Test scaffold connection."""

    @classmethod
    def setup_class(cls):
        """Setup class"""

        cls.protocol_id = "zarathustra/sql_crud:0.1.0"
        cls.protocol_path = "../tests/data/crud_protocol.yaml"

    def test_no_name_provided(self, cli_runner, dummy_agent_tim):
        """Test no name provided."""

        assert Path.cwd() == Path(dummy_agent_tim)

        result = cli_runner.invoke(cli, f"scaffold protocol {self.protocol_path}")
        assert result.exit_code == 0, result.output

        result = cli_runner.invoke(cli, ["scaffold", "connection"])
        assert result.exit_code == 2, result.output
        assert "Missing argument 'NAME'" in result.output

    def test_scaffold_with_spec_readme(self, cli_runner, dummy_agent_tim, caplog):
        """Test scaffold protocol specification in README."""

        result = cli_runner.invoke(cli, f"scaffold protocol {self.protocol_path}")
        assert result.exit_code == 0, result.output

        result = cli_runner.invoke(cli, ["scaffold", "connection", "my_connection", "--protocol", self.protocol_id])
        assert result.exit_code == 0, result.output
        assert f"Read protocol specification: {self.protocol_path}" in caplog.text
        assert f"New connection scaffolded at {dummy_agent_tim}" in caplog.text

    def test_scaffold_with_python(self, cli_runner, dummy_agent_tim, caplog):
        """Test scaffold with python run for correct imports."""

        result = cli_runner.invoke(cli, f"scaffold protocol {self.protocol_path}")
        assert result.exit_code == 0, result.output

        result = cli_runner.invoke(cli, ["scaffold", "connection", "my_connection", "--protocol", self.protocol_id])
        assert result.exit_code == 0, result.output
        assert f"New connection scaffolded at {dummy_agent_tim}" in caplog.text

        result = cli_runner.invoke(aea_cli, "remove-key ethereum".split())
        assert result.exit_code == 0, result.output

        result = cli_runner.invoke(aea_cli, "publish --push-missing --local".split())
        assert result.exit_code == 0, result.output

        connection_dir = Path("../packages/zarathustra/connections/my_connection")
        connection_path = connection_dir / "connection.py"
        test_connection_path = connection_dir / "tests" / "test_connection.py"

        for path in (connection_path, test_connection_path):
            result = subprocess.run([sys.executable, path], shell=True, check=True, capture_output=True)
            assert result.returncode == 0, result.stderr

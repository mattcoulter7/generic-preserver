import pytest

from typer.testing import CliRunner
from mclib.template.application.cli import main  # Adjust based on your actual module name

runner = CliRunner()


@pytest.mark.parametrize(
    "template_input, expected_output",
    [
        ("blah", "blah"),
    ]
)
def test_cli_via_runner(
    template_input: str,
    expected_output: str,
):
    # Run the CLI command with the given parameters
    result = runner.invoke(
        main,
        [
            "--template-input", template_input,
        ]
    )

    assert result.exit_code == 0
    assert expected_output in result.output

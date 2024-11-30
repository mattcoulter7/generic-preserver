import pytest
import os


@pytest.mark.parametrize(
    "template_input, expected_output",
    [
        ("blah", "blah"),
    ]
)
def test_cli_via_subprocess(
    template_input: str,
    expected_output: bool,
):
    stdout = os.popen(
        f"poetry run mclib_template --template-input {template_input}"
    ).read()

    assert expected_output in stdout

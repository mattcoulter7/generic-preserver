import pytest

from mclib.template.helpers import template_func


@pytest.mark.parametrize(
    "template_input, expected_output",
    [
        ("blah", "blah"),
    ]
)
def test_template(
    template_input: str,
    expected_output: str,
):
    actual_output = template_func(
        template_input=template_input,
    )

    assert actual_output == expected_output

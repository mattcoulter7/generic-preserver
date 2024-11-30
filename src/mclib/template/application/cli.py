import typer

from mclib.template.helpers import template_func

main = typer.Typer()


@main.command()
def template_command(
    template_input: str = typer.Option(
        ...,
        prompt="Template Input 1",
        help="Template Input 1",
    ),
):
    response = template_func(
        template_input=template_input,
    )

    typer.echo(response)


# Entry point for the CLI app
if __name__ == "__main__":
    main()

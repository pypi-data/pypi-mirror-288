import click


@click.group()
def cli():
    pass


@click.command()
@click.option("-f", "--file", type=click.Path(exists=True), help="File to upload")
def submit(file):
    if file:
        click.echo(f"Uploading file: {file}")
        # 在这里添加你的文件上传逻辑
    else:
        click.echo("No file provided. Use the -f option to specify a file.")


cli.add_command(submit)

if __name__ == "__main__":
    cli()

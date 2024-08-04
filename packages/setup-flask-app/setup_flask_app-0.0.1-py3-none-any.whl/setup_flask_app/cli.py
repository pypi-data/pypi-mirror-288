import typer
import os
from typing_extensions import Annotated
import shutil

app = typer.Typer()

directories = ['static', 'templates', 'models', 'views', 'forms']
files = ['__init__.py', 'routes.py', 'config.py', 'run.py']

def create_directories(parent_directory: str ,directories_list: list):
    print("making directories")
    with typer.progressbar(directories_list) as progress:
        for dir in progress:
            if not os.path.exists(f"./{parent_directory}/{dir}"):
                os.mkdir(f"./{parent_directory}/{dir}")
                progress.update(1)

def create_files(parent_directory: str ,files_list: list):
    print("making files")
    with typer.progressbar(files_list) as progress:
        for file in progress:
            if not os.path.exists(f"./{parent_directory}/{file}"):
                open(f"./{parent_directory}/{file}", 'w').close()
                progress.update(1)
                
def delete_app(app_name):
    if os.path.exists(app_name):
        shutil.rmtree(app_name)

@app.command()
def create_app(name: str = typer.Argument(), boostrap: Annotated[bool, typer.Option(help="This is to setup boostrap along with app")] = False):
    if boostrap:
        print("working")
    delete_app(name)
    
    if not os.path.exists(name):
        os.makedirs(name)
    

    create_directories(name, directories)

    create_files(name, files)


if __name__ == "__main__":
    app()

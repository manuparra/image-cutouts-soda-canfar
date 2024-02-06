from ast import arg
import click
import subprocess
import os, sys

#@click.group()
#def cli():
#    pass

@click.command()
@click.argument('input', type=click.Path(exists=True))
@click.option('--output-dir',default='.',help='Director for cutouts')

def cli(input, output_dir):
    """Process input source list to cutouts"""

    format = "fits"

    # Run process to find images where sources are located    
    res = subprocess.run(["check_LoTSS_soda",input])

    # Check process ran okay
    if res.returncode!=0:
        print("Problem running check_LoTSS_soda.py")
        sys.exit(-1)

    # Now make arg list to make cutouts
    
    arg_list = ["sort_json_soda"]

    if format=="fits":
        arg_list.append("make-fits")
        arg_list.append(f"{input}")
        arg_list.append(f"data_soda.json")
 
    arg_list.append("--output-dir")
    arg_list.append(f"{output_dir}")
       
    subprocess.run(arg_list)

#cli.add_command(make)

if __name__ == '__main__':
    cli()

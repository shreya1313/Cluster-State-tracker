import os
import re
import click
from itertools import cycle

from subprocess import check_output, CalledProcessError, STDOUT


table_cell_pattern = re.compile(r'([a-zA-Z0-9\-]+)\s+')


def execute(command):
    click.echo('')
    click.echo('Executing COMMAND: {}'.format(command))
    os.system(command)


def get_command_output(command):
    click.echo('')
    click.echo('Executing COMMAND: {}'.format(command))

    try:
        return check_output(command, shell=True, stderr=STDOUT)
    except CalledProcessError as e:
        return e.output, e.returncode


def parse_cli_table(text):
    if not text.endswith('\n'):
        text += '\n'

    n_rows = len(text.split('\n')) - 1
    cells = table_cell_pattern.findall(text)
    n_cols = len(cells) / n_rows

    headers = cells[:n_cols]
    parsed_data = {head: [] for head in headers}

    for head, value in zip(cycle(headers), cells[n_cols:]):
        parsed_data[head].append(value)

    return parsed_data

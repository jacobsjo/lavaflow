import os
from beet import Context

def beet_default(ctx: Context):
    if 'GITHUB_OUTPUT' in os.environ:
        with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
            print(f'version={ctx.project_version}', file=fh)
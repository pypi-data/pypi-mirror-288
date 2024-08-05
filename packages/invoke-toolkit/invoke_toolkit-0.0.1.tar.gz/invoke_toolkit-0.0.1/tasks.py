from invoke import task, Context
import subprocess

REPO_ROOT = (
    subprocess.check_output("git rev-parse --show-toplevel", shell="sh")
    .strip()
    .decode()
)


@task()
def build(ctx: Context):
    ctx.run("hatch build", pty=True)


@task()
def test(ctx: Context):
    ctx.run("hatch run dev:pytest", pty=True)


@task()
def clean_dist(ctx: Context):
    with ctx.cd(REPO_ROOT):
        ctx.run("dist/*")

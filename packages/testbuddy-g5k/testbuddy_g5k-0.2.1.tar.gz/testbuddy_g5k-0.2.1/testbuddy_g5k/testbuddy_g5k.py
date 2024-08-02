import tomllib
import shlex
import json
import click
import subprocess
import os

# This scripts name. Everything in the Grid'5000 servers goes under
# this directory in the home directory of the user.
this_script = "testbuddy-g5k"
# The access server of Grid'5000. See
# <https://www.grid5000.fr/w/Getting_Started#Connecting_for_the_first_time>
# for a description of the server layout of Grid'5000.
access_fqdn = "access.grid5000.fr"

# REST API URL for Grid'5000.
api_url = f"https://api.grid5000.fr"


# Grab the list of available Grid'5000 sites from its REST API.
#
# This function first has to SSH into the access server because the
# API server is not publicly available.
def get_sites(login, dry_run=False):
    cmd = subprocess_run(
        [
            "ssh",
            "-o",
            "StrictHostKeyChecking=accept-new",
            "-T",
            f"{login}@{access_fqdn}",
            f"curl --silent {api_url}/stable/sites?branch=master",
        ],
        check=True,
        stdout=subprocess.PIPE,
        text=True,
        dry_run=dry_run,
    )
    if dry_run:
        return ["site_1", "site_2", "site_N"]
    sites_json = json.loads(cmd.stdout)
    sites = list(map(lambda x: x["uid"], sites_json["items"]))
    return sites


# Add a 'dry_run' option to subprocess.run that only prints the
# command to be executed.
def subprocess_run(*args, dry_run=False, **kwargs):
    if dry_run:
        click.secho(" ".join(*args), fg="yellow", bg="black", bold=True)
        return subprocess.CompletedProcess(
            args=args, returncode=0, stdout="", stderr=""
        )
    else:
        return subprocess.run(*args, **kwargs)


# This class is used to have --help override the error of "required
# arguments missing" for subcommands.
#
# Source: Stephen Rauch,
# <https://stackoverflow.com/a/55821551/19253280>.
# License: CC BY-SA 4.0.
# See <https://stackoverflow.com/posts/55821551/timeline> for
# licensing details.
class IgnoreRequiredWithHelp(click.Group):
    def parse_args(self, ctx, args):
        try:
            return super(IgnoreRequiredWithHelp, self).parse_args(ctx, args)
        except click.MissingParameter:
            if "--help" not in args:
                raise
            for param in self.params:
                param.required = False
            return super(IgnoreRequiredWithHelp, self).parse_args(ctx, args)


# The callback to --configuration that simply loads the TOML
# configuration file into Click's variables.
def configuration(ctx, param, file):
    del param
    if file:
        conf = tomllib.load(file)
        ctx.default_map = conf
        try:
            ctx.default_map["launch"]["experiments"] = list(
                map(json.dumps, conf["launch"]["experiments"])
            )
        except:
            pass


# The callback to --experiments that loads the 'experiments' field
# into Click's context dictionary.
#
# This callback allows for two syntaxes, to account for proper TOML
# configuration files a-la:
#
# experiments = [
#  { site="rennes", cluster="paravance" },
#  { ... },
# ]
#
# and also the shorter command-line invocation:
#
#   --experiments 'site="rennes",cluster="paravance"'.
def experiments(ctx, param, tomls):
    del param
    if tomls:
        try:
            tmp = ",".join(map(lambda toml: f"{{{toml}}}", tomls))
            ctx.params.update(tomllib.loads(f"experiments = [{tmp}]"))
        except tomllib.TOMLDecodeError as e:
            try:
                ctx.params["experiments"] = list(map(json.loads, tomls))
            except:
                raise click.BadParameter(str(e))
    else:
        ctx.params["experiments"] = {}


@click.group(
    cls=IgnoreRequiredWithHelp,
    context_settings={"help_option_names": ["-h", "--help"]},
    epilog="""Use "COMMAND --help" to learn more about COMMAND.

    Additional documentation may be found at
    <https://_-.pages.debian.net/testbuddy-g5k>.""",
)
@click.version_option(None, "--version", "-v")
@click.option(
    "-c",
    "--configuration",
    help="Set the configuration file.",
    metavar="FILE",
    type=click.File("rb"),
    callback=configuration,
    expose_value=False,
)
@click.option(
    "--dry-run", help="Print a dry run and do nothing else", is_flag=True, default=False
)
@click.option(
    "-l", "--login", help="SSH login name to Grid'5000", metavar="LOGIN", type=str
)
@click.option("-p", "--project", help="Project name", metavar="PROJECT", type=str)
@click.option("-n", "--name", help="Subproject name", metavar="NAME", type=str)
@click.pass_context
def main(ctx, dry_run, login, project, name):
    ctx.obj = {"dry_run": dry_run, "login": login, "project": project, "name": name}


@main.command()
@click.option(
    "-a",
    "--assets",
    help="Directories or files to be transferred into PROJECT/NAME  [multiple]",
    metavar="ASSETS",
    type=click.Path(exists=True),
    multiple=True,
)
@click.option(
    "-e",
    "--entrypoint",
    help="The entrypoint, relative to PROJECT/NAME",
    metavar="ENTRYPOINT",
    type=click.Path(dir_okay=False),
)
@click.option(
    "-g",
    "--grd-environment",
    help="The Grid'5000 kaenv3 environment to use",
    metavar="GRD_ENVIRONMENT",
    type=str,
    default="debiantesting-nfs",
    show_default=True,
)
@click.option(
    "-o",
    "--grd-options",
    help="The Grid'5000 options to use",
    metavar="GRD_OPTIONS",
    type=str,
    default="host=1",
    show_default=True,
)
@click.option(
    "-s",
    "--script-args",
    help="Extra arguments for the entrypoint script  [multiple]",
    metavar="SCRIPT_ARGS",
    type=str,
    multiple=True,
)
@click.option(
    "-x",
    "--experiments",
    help="Specifications for the experiments to run  [multiple]",
    type=str,
    required=True,
    callback=experiments,
    expose_value=False,
    multiple=True,
)
@click.option(
    "-w",
    "--wall-time",
    help="Total resource time granted to experiment by Grid'5000",
    metavar="WALL_TIME",
    type=str,
    default="1:00:00",
    show_default=True,
)
@click.option(
    "-O",
    "--override-options",
    help="Launch options override experiment options",
    is_flag=True,
    default=False,
    show_default=True,
)
@click.pass_obj
def launch(
    conf,
    assets,
    entrypoint,
    grd_environment,
    grd_options,
    script_args,
    experiments,
    wall_time,
    override_options,
):
    """Launch experiments on Grid'5000."""
    dry_run = conf["dry_run"]
    login = conf["login"]
    project = conf["project"]
    name = conf["name"]
    total_experiments = len(experiments)
    launch_conf = {
        "assets": assets,
        "entrypoint": entrypoint,
        "grd_environment": grd_environment,
        "grd_options": grd_options,
        "script_args": script_args,
    }
    with click.progressbar(
        length=total_experiments, label="Progress & Estimated Time Left"
    ) as bar:
        for index, experiment in enumerate(experiments):
            index_status = f"[{index+1}/{total_experiments}]"
            click.echo(f"\n{index_status} On {project}/{name}:")
            if override_options:
                experiment_conf = experiment | launch_conf
            else:
                experiment_conf = launch_conf | experiment
            assets = list(experiment_conf["assets"])
            entrypoint = experiment_conf["entrypoint"]
            grd_environment = experiment_conf["grd_environment"]
            grd_options = experiment_conf["grd_options"]
            script_args = list(experiment_conf["script_args"])
            try:
                site = experiment_conf["site"]
                cluster = experiment_conf["cluster"]
            except KeyError as k:
                click.echo(
                    click.style("ERROR", fg="red")
                    + f": {k} is not specified in the experiment.",
                    err=True,
                )
                click.echo(
                    "To specify an experiment, at bare "
                    "minimum you must provide values for 'site' and "
                    "'cluster'.\nFor instance, you may write:\n"
                    '    --experiment \'site="rennes",cluster="paravance"\'\n'
                    "or if you would rather have it in your configuration:\n"
                    '    experiments = [ { site="rennes", cluster="paravance" } ]',
                    err=True,
                )
                raise click.ClickException(f"Please provide {k}.")

            site_fqdn = f"{site}.grid5000.fr"
            src_dir = f"/home/{login}/{this_script}/{project}/{name}"
            entrypoint_full = f"{src_dir}/{entrypoint}"
            script_args_q = [""] + list(
                map(shlex.quote, [f"--src-dir={src_dir}"] + script_args)
            )
            script_args_s = " --script-arg ".join(script_args_q).strip()
            dst = f"{site}/{this_script}/{project}/{name}"
            click.echo(f"  Transferring assets into {dst} with rsync...")
            rsync = subprocess_run(
                ["rsync", "--archive", "--recursive", "--compress", "--mkpath"]
                + assets
                + [f"{login}@{access_fqdn}:{dst}"],
                dry_run=dry_run,
            )
            if rsync.returncode == 0:
                click.echo("  ==> " + click.style("OK", fg="green") + ".")
            else:
                click.echo(
                    "  ==> "
                    + click.style("ERROR", fg="red")
                    + f": {index_status} skipped.",
                    err=True,
                )
                bar.update(1)
                continue
            click.echo("  Requesting resources...")
            if grd_options:
                grd_options = "/" + grd_options
            ssh = subprocess_run(
                [
                    "ssh",
                    "-o",
                    "StrictHostKeyChecking=accept-new",
                    "-T",
                    "-J",
                    f"{login}@{access_fqdn}",
                    f"{login}@{site_fqdn}",
                    f"grd bootstrap --resources {{cluster='{cluster}'}}{grd_options} --detach "
                    f"--environment {grd_environment} --walltime '{wall_time}' --terminate-after-script "
                    f"--script {entrypoint_full} {script_args_s}",
                ],
                dry_run=dry_run,
            )
            if ssh.returncode == 0:
                click.echo(
                    "  ==> "
                    + click.style("OK", fg="green")
                    + f": {index_status} Resources will be available when Grid'5000 grants them.\n"
                )
            else:
                click.echo("  ==> " + click.style("ERROR", fg="red") + ".\n", err=True)
            bar.update(1)


@main.command()
@click.option(
    "-y", "--yes", is_flag=True, help="Answer interactively yes to the prompt."
)
@click.pass_obj
def free_disk_memory(conf, yes):
    """
    Remove tarballs from Grid'5000.

    Removes from the Grid'5000 sites the tarballs inside the results/
    directory. Also removes all lingering directories that were not
    made into tarballs because of crashes or other issues.

    Use 'sync' to download the tarballs in the results directories
    before removing them.

    This action will remove the tarballs and lingering directories
    from all Grid'5000 sites.
    """
    dry_run = conf["dry_run"]
    login = conf["login"]
    project = conf["project"]
    name = conf["name"]
    if not yes:
        confirm_msg = f"Proceed with freeing memory on Grid'5000 for {project}/{name}?"
        if dry_run:
            confirm_msg += " (dry-run)"
        click.confirm(
            confirm_msg,
            default=False,
            abort=True,
        )
    click.echo(
        f"Deleting tarballs and lingering directories for {project}/{name}, please wait..."
    )
    sites = get_sites(login, dry_run=dry_run)
    project_dirs = list(
        map(
            lambda site: shlex.quote(f"{site}/{this_script}/{project}/{name}"),
            sites,
        )
    )
    result_dirs = map(
        lambda project_dir: shlex.quote(f"{project_dir}/results"),
        project_dirs,
    )
    project_dirs_s = " ".join(project_dirs)
    result_dirs_s = " ".join(result_dirs)
    result = subprocess_run(
        [
            "ssh",
            "-o",
            "StrictHostKeyChecking=accept-new",
            "-T",
            f"{login}@{access_fqdn}",
            f"find {result_dirs_s} -maxdepth 1 -type f -name '*.tar.gz' -exec rm -f {{}} + ;",
            f"find {project_dirs_s} -maxdepth 1 -type d -regextype posix-egrep ",
            f"-regex '.*/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]\\+[0-9][0-9]:[0-9][0-9]-.*' "
            f"-exec rm -rf {{}} +",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
        dry_run=dry_run,
    )
    result_error = False
    for line in result.stderr.splitlines():
        if "No such file or directory" not in line:
            click.echo(line, err=True)
            result_error = True
    if result_error:
        click.echo("  ==> " + click.style("ERROR", fg="red") + ".", err=True)
    else:
        click.echo("  ==> " + click.style("OK", fg="green") + ".")


@main.command()
@click.option(
    "-r",
    "--results-dir",
    help="Sync result tarballs from Grid'5000 into local directory",
    type=click.Path(file_okay=False, exists=True),
    metavar="RESULTS",
    required=True,
)
@click.pass_obj
def sync(conf, results_dir):
    """Synchronize (download) results from Grid'5000."""
    dry_run = conf["dry_run"]
    login = conf["login"]
    project = conf["project"]
    name = conf["name"]
    os.makedirs(results_dir, exists_ok=True)
    click.echo(
        f"Synchronizing directories for {project}/{name}.\n"
        f"Synchronizing into {results_dir}, please wait."
    )
    sites = get_sites(login, dry_run=dry_run)
    click.echo(f"Synchronizing from the following sites: {' '.join(sites)}.")
    rsync_dirs = list(
        map(lambda site: f":{site}/{this_script}/{project}/{name}/results/", sites)
    )
    rsync_dirs[0] = access_fqdn + rsync_dirs[0]
    out = subprocess_run(
        [
            "rsync",
            "--archive",
            "--compress",
            "--progress",
            "--info=progress2,stats1",
            "--ignore-existing",
            "--prune-empty-dirs",
            "--include",
            "*/",
            "--include",
            "*.tar.gz",
            "--exclude",
            "*",
        ]
        + rsync_dirs
        + [shlex.quote(results_dir)],
        stderr=subprocess.PIPE,
        text=True,
        dry_run=dry_run,
    )
    error = False
    for line in out.stderr.splitlines():
        if "change_dir" in line and "No such file or directory (2)" in line:
            continue
        if error:
            click.echo(line, err=True)
        elif "rsync error: some files/attrs were not transferred" not in line:
            click.echo(line, err=True)
            error = True
    if not error:
        click.echo(click.style("OK", fg="green") + ". Synchronization complete.")
    else:
        click.echo(
            click.style("ERROR", fg="red")
            + ". Errors were encountered during the rsync operation.",
            err=True,
        )


if __name__ == "__main__":
    main()

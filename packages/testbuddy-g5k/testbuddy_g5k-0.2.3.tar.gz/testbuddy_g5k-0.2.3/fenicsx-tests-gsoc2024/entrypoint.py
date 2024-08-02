#!/usr/bin/env python3

import subprocess
import os
import json
import requests
import datetime
import tempfile
import tarfile
import shutil
import argparse
from pathlib import Path


def shell(cmd):
    return subprocess.check_output(cmd).decode("utf-8")


def run_job(
    args,
    login,
    cores,
    hostfile,
    hypre,
    scaling_type,
    problem_type,
    dof,
    filename,
):
    poisson_options = "--problem_type poisson"
    elasticity_options = (
        "--problem_type elasticity "
        "-pc_type gamg "
        "-pc_gamg_coarse_eq_limit 1000 "
        "-mg_levels_ksp_type chebyshev "
        "-mg_levels_pc_type jacobi "
        "-mg_levels_esteig_ksp_type cg "
        "-matptap_via scalable"
    )
    hypre_options = (
        "-pc_type hypre "
        "-pc_hypre_type boomeramg "
        "-pc_hypre_boomeramg_strong_threshold 0.5"
    )
    if problem_type == "poisson":
        problem_options = poisson_options
        if hypre:
            problem_options += " " + hypre_options
    elif problem_type == "elasticity":
        problem_options = elasticity_options
    else:
        raise ValueError('problem_type is either "poisson" or "elasticity".')
    common_options = (
        "--log_view " "-ksp_view " "-ksp_type cg " "-ksp_rtol 1.0e-8 " "-options_left"
    )
    mpiexec = (
        "mpiexec --bind-to core "
        f"-n {cores} "
        f"--hostfile {hostfile} "
        f"{args.exe} --scaling_type {scaling_type} "
        f"--ndofs {dof} "
        f"{problem_options} {common_options}"
    )
    cmd = [
        "su",
        "--pty",
        "--login",
        login,
        f"--command=export OMP_NUM_THREADS=1 && {mpiexec}",
    ]
    with open(f"{filename}.stdout", "w") as fout:
        with open(f"{filename}.stderr", "w") as ferr:
            result = subprocess.run(cmd, stdout=fout, stderr=ferr)
    return {
        "command": mpiexec,
        "cores": cores,
        "dof": dof,
        "exit_status": str(result.returncode),
        "problem_type": problem_type,
        "scaling_type": scaling_type,
    }


def main(args):
    results_dir = f"{args.src_dir}/{args.results_dir}"
    if args.blas_all:
        # Grab all the Debian packages providing the virtual package
        # libblas.so.3.
        tmp_blas_packages = shell(["apt-cache", "showpkg", "libblas.so.3"])
        tmp_pattern = "Reverse Provides: \n"
        tmp_i = tmp_blas_packages.find(tmp_pattern) + len(tmp_pattern)
        blas_packages = list(
            map(lambda s: s.split()[0], tmp_blas_packages[tmp_i:].splitlines())
        )
    else:
        blas_packages = args.blas.split(",")
    packages = [args.mpi] + blas_packages + ["fenicsx-performance-tests"]
    packages_s = " ".join(packages)

    grd_jobid = os.environ["GRD_JOBID"]
    hostname = shell("hostname").rstrip()
    this_host, site = hostname.split(".")[:2]
    cluster = this_host.split("-")[0]

    # Grab cluster and job info.
    cluster_info_json = requests.get(
        f"{args.api_url}/{site}/clusters/{cluster}?deep=true"
    )
    job_info_json = requests.get(f"{args.api_url}/{site}/jobs/{grd_jobid}")

    cluster_info = json.loads(cluster_info_json.text)
    job_info = json.loads(job_info_json.text)
    host0 = cluster_info["items"]["nodes"][0]
    host_info = {}
    host_info["total_cores"] = host0["architecture"]["nb_cores"]
    host_info["sockets"] = host0["architecture"]["nb_procs"]
    host_info["isa"] = host0["processor"]["instruction_set"]
    host_info["model"] = host0["processor"]["model"]
    host_info["model_other"] = host0["processor"]["other_description"]
    login = job_info["user"]
    hosts = job_info["assigned_nodes"]
    n_hosts = len(hosts)
    job_total_cores = host_info["total_cores"] * n_hosts

    # Install packages on every host, including the one currently
    # running this script.
    processes = []
    for host in hosts:
        processes.append(
            subprocess.Popen(
                [
                    "su",
                    "--pty",
                    "--login",
                    login,
                    f"--command=ssh -o StrictHostKeyChecking=accept-new "
                    f"-l root -T {host} "
                    f'"export DEBIAN_FRONTEND=noninteractive && '
                    f"apt-get update && "
                    f"apt-get upgrade --yes && "
                    f'apt-get install --yes binutils {packages_s}"',
                ]
            )
        )
    for process in processes:
        process.wait()

    packages_json = {}
    dpkg = shell(["dpkg", "-l"] + packages).splitlines()
    for package, version in map(
        lambda line: line.split()[1:3],
        filter(lambda line: line.startswith("ii "), dpkg),
    ):
        # Potentially remove :amd64 (or whichever arch in general) from the package name.
        package = package.split(":")[0]
        packages_json[package] = version
    # If complex symbols are enabled, turn off hypre.
    objdump = shell(["objdump", "--private-headers", args.exe])
    hypre = "petsc_complex" not in objdump
    # Create results_dir if it does not already exist.
    try:
        os.mkdir(results_dir, mode=0o750)
    except FileExistsError:
        pass
    # Open a temporary directory in which all resulting files will be
    # placed; use tempfile to guarantee uniqueness of this
    # directory. This temporary directory will then be tarballed into
    # results_dir.
    date = (
        datetime.datetime.now(tz=datetime.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
    )
    with tempfile.TemporaryDirectory(prefix=f"{date}-", dir=args.src_dir) as tmpdir:
        suffix = tmpdir.split("-")[-1]
        hostfile = f"{tmpdir}/hostfile"
        with open(hostfile, "w") as f:
            for host in hosts:
                f.write(f"{host}\n" * host_info["total_cores"])
        result = {}
        result["date"] = date
        result["date_id"] = suffix
        result["version"] = "1.0"
        result["software"] = {
            "uname": shell(
                ["uname", "--kernel-name", "--kernel-release", "--kernel-version"]
            ).rstrip(),
            "packages": packages_json,
            "dolfinx_parameters": {"hypre": str(hypre).lower()},
        }
        machine = shell(["uname", "--machine"]).rstrip()
        result["grid5000"] = {
            "login": login,
            "grd_jobid": grd_jobid,
            "site": site,
            "cluster": cluster,
            "hosts": n_hosts,
            "arch": machine,
            "total_cores": job_total_cores,
            "host": host_info,
        }
        if args.cores_mode == "single-host":
            cores_list = list(range(1, job_total_cores + 1))
        else:
            cores_list = [job_total_cores]
        # Run and dry-run experiments
        virt = f"libblas.so.3-{machine}-linux-gnu"
        alts = shell(["update-alternatives", "--list", virt]).splitlines()
        for alt in alts:
            blas_package = shell(["dpkg", "--search", alt]).split(":")[0]
            if blas_package not in blas_packages:
                continue
            shell(["update-alternatives", "--set", virt, alt])
            for scaling_type in ["weak", "strong"]:
                for problem_type in ["poisson", "elasticity"]:
                    for cores in cores_list:
                        for dof in args.dof.split(","):
                            blas_pkg = shell(["dpkg", "--search", alt]).split(":")[0]
                            filename = (
                                f"{tmpdir}/{scaling_type}-{problem_type}"
                                f"-{cores}cores-{dof}dof"
                                f"-{blas_pkg}"
                            )
                            experiment_json = run_job(
                                args,
                                login,
                                cores,
                                hostfile,
                                hypre,
                                scaling_type,
                                problem_type,
                                dof,
                                filename,
                            )
                            with open(
                                f"{filename}.json",
                                "w",
                            ) as f:
                                result["experiment"] = experiment_json | {
                                    "libblas_choice": blas_pkg
                                }
                                json.dump(result, f)

        # Finally, tarball tmpdir into results_dir.
        tmpdirname = Path(tmpdir).name
        tarball = f"{tmpdir}.tar.gz"
        with tarfile.open(tarball, "w:gz", format=tarfile.GNU_FORMAT) as tar:
            tar.add(tmpdir, arcname=os.path.basename(tmpdir))
            # Atomic move to avoid sending incomplete tarballs. This can
            # happen if the user is syncronizing while we're archiving a
            # tarball.
            shutil.move(tarball, f"{results_dir}/{tmpdirname}.tar.gz")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="The entrypoint for run-fenicsx-tests."
    )
    parser.add_argument(
        "--dof",
        help="Degrees of freedom (comma-separated values)",
        default="2000000,4000000",
    )
    parser.add_argument(
        "--exe",
        help="Path to DOLFINx executable",
        default="/usr/bin/dolfinx-scaling-test",
    )
    parser.add_argument(
        "--src-dir", help="The script directory of this script", required=True
    )
    parser.add_argument(
        "--results-dir",
        help="The directory to store the result tarball, relative to SRC-DIR",
        default="results",
    )
    parser.add_argument("--mpi", help="The MPI library to use", default="libopenmpi3")
    parser.add_argument(
        "--blas",
        help="The BLAS library to use (comma-separated values results in multiple experiments)",
        default="libblas3",
    )
    parser.add_argument(
        "--blas-all",
        help="Use all available BLAS libraries (see also --blas) [default: False]",
        action="store_true",
    )
    parser.add_argument(
        "--api-url",
        help="The Grid'5000 REST API URL",
        default="https://api.grid5000.fr/stable/sites",
    )
    parser.add_argument(
        "--cores-mode",
        help="How to use the available cores",
        type=str,
        choices=["max", "single-host"],
        default="max",
    )
    args = parser.parse_args()
    main(args)

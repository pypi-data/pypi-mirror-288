#!/usr/bin/env python3

import tomllib
import click
import json
import pandas
import tarfile
import sqlite3
import pathlib


def grab_timings(b):
    """Grab the timings from a fenicsx-performance-tests output."""
    timings_table = {
        "build_box_mesh": "Build BoxMesh (tetrahedra)",
        "build_dofmap_data": "Build dofmap data",
        "build_sparsity": "Build sparsity",
        "compute_connectivity_20": "Compute connectivity 2-0",
        "compute_dof_reordering_map": "Compute dof reordering map",
        "compute_entities_dim2": "Compute entities of dim = 2",
        "compute_scotch_graph_partition": "Compute graph partition (SCOTCH)",
        "compute_local_mesh_dual_graph": "Compute local part of mesh dual graph",
        "compute_local_to_local_map": "Compute local-to-local map",
        "compute_nonlocal_mesh_dual_graph": "Compute non-local part of mesh dual graph",
        "compute_local_to_global_links": "Compute-local-to-global links for global/local adjacency list",
        "distribute_nodes_to_ranks": "Distribute AdjacencyList nodes to destination ranks",
        "distribute_rowwise": "Distribute row-wise data (scalable)",
        "gps_create_level_structure": "GPS: create_level_structure",
        "gibbs_poole_stockmeyer_ordering": "Gibbs-Poole-Stockmeyer ordering",
        "init_mpi": "Init MPI",
        "init_petsc": "Init PETSc",
        "init_dofmap_from_element_dofmap": "Init dofmap from element dofmap",
        "init_logging": "Init logging",
        "petsc_krylov_solver": "PETSc Krylov solver",
        "scotch_dgraphbuild": "SCOTCH: call SCOTCH_dgraphBuild",
        "scotch_dgraphpart": "SCOTCH: call SCOTCH_dgraphPart",
        "sparsitypattern_finalize": "SparsityPattern::finalize",
        "topology_create": "Topology: create",
        "topology_shared_index_ownership": "Topology: determine shared index ownership",
        "topology_vertex_groups": "Topology: determine vertex ownership groups",
        "zzz_assemble_matrix": "ZZZ Assemble matrix",
        "zzz_assemble_vector": "ZZZ Assemble vector",
        "zzz_create_mesh": "ZZZ Create Mesh",
        "zzz_create_rhs_function": "ZZZ Create RHS function",
        "zzz_create_boundary_conditions": "ZZZ Create boundary conditions",
        "zzz_create_facets_connectivity": "ZZZ Create facets and facet->cell connectivity",
        "zzz_create_forms": "ZZZ Create forms",
        "zzz_create_nearnullspace": "ZZZ Create near-nullspace",
        "zzz_functionspace": "ZZZ FunctionSpace",
        "zzz_solve": "ZZZ Solve",
    }
    values = {}
    flag = True
    for line in b.decode("utf-8").splitlines():
        if flag and "Summary of timings" not in line:
            continue
        flag = False
        for key, pattern in timings_table.items():
            if pattern in line:
                [reps, wall_avg, wall_tot] = line.split("|")[1].strip().split()
                values |= {
                    f"timings.{key}.reps": reps,
                    f"timings.{key}.wall_avg": wall_avg,
                    f"timings.{key}.wall_tot": wall_tot,
                }
    return values


def create_schema(cur):
    """Creates the version=1.0 database schema"""
    cur.execute(
        'CREATE TABLE IF NOT EXISTS results (id INTEGER PRIMARY KEY AUTOINCREMENT,"date","date_id","experiment.command","experiment.cores","experiment.dof","experiment.exit_status","experiment.libblas_choice","experiment.problem_type","experiment.scaling_type","experiment.stderr","experiment.stdout","grid5000.arch","grid5000.cluster","grid5000.grd_jobid","grid5000.host.isa","grid5000.host.model","grid5000.host.model_other","grid5000.host.sockets","grid5000.host.total_cores","grid5000.hosts","grid5000.login","grid5000.site","grid5000.total_cores","software.dolfinx_parameters.hypre","software.packages.fenicsx-performance-tests","software.packages.libblas3","software.uname","timings.build_box_mesh.reps","timings.build_box_mesh.wall_avg","timings.build_box_mesh.wall_tot","timings.build_dofmap_data.reps","timings.build_dofmap_data.wall_avg","timings.build_dofmap_data.wall_tot","timings.build_sparsity.reps","timings.build_sparsity.wall_avg","timings.build_sparsity.wall_tot","timings.compute_connectivity_20.reps","timings.compute_connectivity_20.wall_avg","timings.compute_connectivity_20.wall_tot","timings.compute_dof_reordering_map.reps","timings.compute_dof_reordering_map.wall_avg","timings.compute_dof_reordering_map.wall_tot","timings.compute_entities_dim2.reps","timings.compute_entities_dim2.wall_avg","timings.compute_entities_dim2.wall_tot","timings.compute_local_mesh_dual_graph.reps","timings.compute_local_mesh_dual_graph.wall_avg","timings.compute_local_mesh_dual_graph.wall_tot","timings.compute_local_to_global_links.reps","timings.compute_local_to_global_links.wall_avg","timings.compute_local_to_global_links.wall_tot","timings.compute_local_to_local_map.reps","timings.compute_local_to_local_map.wall_avg","timings.compute_local_to_local_map.wall_tot","timings.compute_nonlocal_mesh_dual_graph.reps","timings.compute_nonlocal_mesh_dual_graph.wall_avg","timings.compute_nonlocal_mesh_dual_graph.wall_tot","timings.compute_scotch_graph_partition.reps","timings.compute_scotch_graph_partition.wall_avg","timings.compute_scotch_graph_partition.wall_tot","timings.distribute_nodes_to_ranks.reps","timings.distribute_nodes_to_ranks.wall_avg","timings.distribute_nodes_to_ranks.wall_tot","timings.distribute_rowwise.reps","timings.distribute_rowwise.wall_avg","timings.distribute_rowwise.wall_tot","timings.gibbs_poole_stockmeyer_ordering.reps","timings.gibbs_poole_stockmeyer_ordering.wall_avg","timings.gibbs_poole_stockmeyer_ordering.wall_tot","timings.gps_create_level_structure.reps","timings.gps_create_level_structure.wall_avg","timings.gps_create_level_structure.wall_tot","timings.init_dofmap_from_element_dofmap.reps","timings.init_dofmap_from_element_dofmap.wall_avg","timings.init_dofmap_from_element_dofmap.wall_tot","timings.init_logging.reps","timings.init_logging.wall_avg","timings.init_logging.wall_tot","timings.init_mpi.reps","timings.init_mpi.wall_avg","timings.init_mpi.wall_tot","timings.init_petsc.reps","timings.init_petsc.wall_avg","timings.init_petsc.wall_tot","timings.petsc_krylov_solver.reps","timings.petsc_krylov_solver.wall_avg","timings.petsc_krylov_solver.wall_tot","timings.scotch_dgraphbuild.reps","timings.scotch_dgraphbuild.wall_avg","timings.scotch_dgraphbuild.wall_tot","timings.scotch_dgraphpart.reps","timings.scotch_dgraphpart.wall_avg","timings.scotch_dgraphpart.wall_tot","timings.sparsitypattern_finalize.reps","timings.sparsitypattern_finalize.wall_avg","timings.sparsitypattern_finalize.wall_tot","timings.topology_create.reps","timings.topology_create.wall_avg","timings.topology_create.wall_tot","timings.topology_shared_index_ownership.reps","timings.topology_shared_index_ownership.wall_avg","timings.topology_shared_index_ownership.wall_tot","timings.topology_vertex_groups.reps","timings.topology_vertex_groups.wall_avg","timings.topology_vertex_groups.wall_tot","timings.zzz_assemble_matrix.reps","timings.zzz_assemble_matrix.wall_avg","timings.zzz_assemble_matrix.wall_tot","timings.zzz_assemble_vector.reps","timings.zzz_assemble_vector.wall_avg","timings.zzz_assemble_vector.wall_tot","timings.zzz_create_boundary_conditions.reps","timings.zzz_create_boundary_conditions.wall_avg","timings.zzz_create_boundary_conditions.wall_tot","timings.zzz_create_facets_connectivity.reps","timings.zzz_create_facets_connectivity.wall_avg","timings.zzz_create_facets_connectivity.wall_tot","timings.zzz_create_forms.reps","timings.zzz_create_forms.wall_avg","timings.zzz_create_forms.wall_tot","timings.zzz_create_mesh.reps","timings.zzz_create_mesh.wall_avg","timings.zzz_create_mesh.wall_tot","timings.zzz_create_nearnullspace.reps","timings.zzz_create_nearnullspace.wall_avg","timings.zzz_create_nearnullspace.wall_tot","timings.zzz_create_rhs_function.reps","timings.zzz_create_rhs_function.wall_avg","timings.zzz_create_rhs_function.wall_tot","timings.zzz_functionspace.reps","timings.zzz_functionspace.wall_avg","timings.zzz_functionspace.wall_tot","timings.zzz_solve.reps","timings.zzz_solve.wall_avg","timings.zzz_solve.wall_tot","version")'
    )


@click.command(
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.option(
    "-d",
    "--database",
    help="The database to load the results into, created if it doesn't exist",
    metavar="DATABASE",
    required=True,
    type=click.Path(dir_okay=False),
)
@click.option(
    "-c",
    "--configuration",
    help="Use the results directory from the testbuddy-g5k configuration",
    metavar="CONFIGURATION",
    default=None,
    type=click.File("rb"),
)
@click.argument("results_dirs", nargs=-1)
def main(database, configuration, results_dirs):
    """
    Load tarballs into the database.

    Tarballs that have been previously preprocessed are not processed again.
    """
    if not configuration and not results_dirs:
        raise click.ClickException(
            "Either --configuration or RESULTS_DIRS... must be specified, see --help."
        )
    tmp = list(results_dirs)
    if configuration:
        conf = tomllib.load(configuration)
        try:
            tmp += [conf["sync"]["results_dir"]]
        except:
            if tmp:
                pass
            else:
                click.echo(
                    click.style("ERROR", fg="red")
                    + ": The configuration file does not contain a 'results_dir' key in its [sync] section.",
                    err=True,
                )
                exit(1)
    dirs = map(pathlib.Path, tmp)
    con = sqlite3.connect(database)
    cur = con.cursor()
    create_schema(cur)
    con.commit()
    tarball_count = 0
    total_tarball_count = 0
    row_count = 0
    for dir in dirs:
        for file in dir.glob("*.tar.gz"):
            total_tarball_count += 1
            [date, date_id] = file.name.removesuffix(".tar.gz").rsplit("-", 1)
            cur.execute(
                f"SELECT EXISTS(SELECT 1 FROM results WHERE date=? AND date_id=?)",
                [date, date_id],
            )
            if cur.fetchone()[0]:
                # The tarball has already been processed and its
                # results already exist in the database, therefore
                # continue to avoid creating a duplicate entry.
                continue
            tarball_count += 1
            with tarfile.open(file, "r") as t:
                for tf in t:
                    if tf.isfile() and tf.name.endswith(".json"):
                        f = t.extractfile(tf)
                        name = tf.name.removesuffix(".json")
                        bout = t.extractfile(f"{name}.stdout")
                        berr = t.extractfile(f"{name}.stderr")
                        if f and bout and berr:
                            df = pandas.json_normalize(json.load(f))
                            d1 = df.to_dict(orient="index")[0]
                            bout_read = bout.read()
                            berr_read = berr.read()
                            d2 = grab_timings(bout_read)
                            d3 = {
                                "experiment.stdout": bout_read,
                                "experiment.stderr": berr_read,
                            }
                            xs = sorted((d1 | d2 | d3).items())
                            keys, values = zip(*xs)
                            keys_s = ",".join([f'"{k}"' for k in keys])
                            placeholders = ",".join(["?"] * len(keys))
                            cur.execute(
                                f"INSERT INTO results({keys_s}) VALUES({placeholders})",
                                values,
                            )
                            f.close()
                            row_count += 1
    con.commit()
    con.close()
    click.echo(
        f"Processed {tarball_count} new tarballs out of {total_tarball_count} in total, added {row_count} new experiments."
    )


if __name__ == "__main__":
    main()

The fenicsx-tests-gsoc2024 script
=================================

Introduction
------------

A typical testbuddy-g5k project will have an *entrypoint*, it will have some tarball *results* and other auxiliary scripts for processing the results further.

In the :file:`fenicsx-tests-gsoc2024` directory lies an example of a project that testbuddy-g5k can work with. The files :file:`entrypoint.bash` and :file:`entrypoint.py` are essentially the entrypoint, meaning the script that will run in one of the hosts when the cluster resources are available. There's a Bash and a Python script because the Bash script sets up the :code:`python3-requests` dependency before executing the Python script. The :file:`load_db.py` script is a post-processing script that will load the tarballed data into an SQLite3 database, whose schema is described below in `The SQL schema`_ section. The :file:`plot.py` file will load data from the database and create Plotly plots which will be stored in HTML files in the given output directory.

- The :file:`config/fenicsx-tests-gsoc2024.toml` configuration file contains the configuration to launch these experiments.
- The :file:`fenicsx-tests-gsoc2024/entrypoint.bash` script is the entrypoint that installs the `Python3 requests <https://requests.readthedocs.io/en/latest/>`_ Debian package. This is important because the real entrypoint, :file:`fenicsx-tests-gsoc2024/entrypoint.py` uses requests to interact with the Grid'5000 REST API.
- The :file:`fenicsx-tests-gsoc2024/load_db.py` script will import the tarballed results into an SQLite3 database. The database is created if it does not exist.
- The :file:`fenicsx-tests-gsoc2024/plot.py` script will plot the results of a database, creating HTML files inside the specified directory.

Example session
---------------

We illustrate the use of testbuddy-g5k and the fenicsx-tetss-gsoc2024 scripts in the following section. This is a typical use of them to perform experiments and create HTML plots.

Launching experiments
~~~~~~~~~~~~~~~~~~~~~

We can launch experiments with:

.. code-block:: sh

   testbuddy-g5k -c config/fenicsx-tests-gsoc2024.toml launch

Or if we are interested in running on every number of cores of a single host, we can instead do:

.. code-block:: sh

   testbuddy-g5k -c config/fenicsx-tests-gsoc2024.toml launch --grd-options host=1 --override-options --script-args --single-host

.. note::

   With :code:`--script-args --single-host` we are telling testbuddy-g5k to pass the option :code:`--single-host` to the entrypoint, which activates the single-host mode for fenicsx-tests-gsoc2024: instead of running on max cores available, run from 1 to max cores available. Reasonably, we tell testbuddy-g5k to only allocate one host with :code:`--grd-options host=1` and for this option to override any host configuration with :code:`--override-options`, since the :file:`config/fenicsx-tests-gsoc2024.toml` configuration file specifies other numbers of hosts.


Downloading the tarballs
~~~~~~~~~~~~~~~~~~~~~~~~

We can sync the results with:

.. code-block:: sh

   testbuddy-g5k -c config/fenicsx-tests-gsoc2024.toml sync

The configured directory under the :code:`[sync]` section is :file:`./www/results` and that is where the tarballs will be stored, but it can be changed. Note that tarballs are named according to `ISO 8601 <https://en.wikipedia.org/wiki/ISO_8601>`_ universal time date, i.e. as in the output of :code:`date -uIs` of :manpage:`date(1)` and to be extracted you must use the :code:`--force-local` option to :manpage:`tar(1)`.

.. note::

   You typically don't have to inspect the tarballs yourself. The :file:`fenicsx-tests-gsoc2024/load_db.py` will load them into an SQLite3 database.

Loading the results in a database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If we'd like to create a brand new database, we can do:

.. code-block:: sh

   ./fenicsx-tests-gsoc2024/load_db.py -c config/fenicsx-tests-gsoc2024.toml -d results.db

This will load all the results of :file:`www/results` into a database called :file:`results.db`. This script takes care to not create duplicate rows, so you can use it as many times as you'd like; it will do nothing if there are no new results.

Plotting the results into graphs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With the command

.. code-block:: sh

   ./fenicsx-tests-gsoc2024/plot.py -d results.db www/plots

we are instructing the script to load the :file:`results.db` database and create four HTML files named :file:`strong_poisson.html`, :file:`weak_poisson.html`, :file:`strong_elasticity.html`, and :file:`weak_elasticity.html` into the directory :file:`www/plots`.


The SQL schema
--------------

The database contains a single table called :code:`results` which contains all the results of the *experiments*. We explain all the columns of the :code:`results` table. Keep in mind that an experiment can be a batch of results;  each result is a row entry. To clarify further, an experiment will run both Poisson and Elasticity problems, in both weak and strong scaling; each combination is a single result resulting in a row entry. An experiment is essentially an invocation of the :file:`fenicsx-tests-gsoc2024` entrypoint in a particular group of hosts in a cluster.

.. warning::
   Some of the column names contain dots :code:`.` and hyphens :code:`-`. SQLite3 will require you to double-quote these identifiers to operate on them, see `SQLite Keywords <https://sqlite.org/lang_keywords.html>`_. 

:id: An incrementing integer that is unique to the row entry.
:date: The date when the experiment group was conducted in ISO-8601 format.
:date_id: A random string; together with date, they are unique to an experiment (but **not** to a result; see above, many results can be performed in a single experiment.)
:experiment.command: The command that gave the results; typically starts with :code:`mpiexec ...`.
:experiment.cores: The number of cores used in the experiment. This is smaller than total cores available when :code:`--cores-mode=single-host`.
:experiment.dof: The degrees of freedom used.
:experiment.exit_status: The exit status of :code:`experiment.command`.
:experiment.libblas_choice: The particular `BLAS <https://en.wikipedia.org/wiki/Basic_Linear_Algebra_Subprograms>`_ implementation used.
:experiment.problem_type: The problem type, either :code:`poisson` or :code:`elasticity`.
:experiment.scaling_type: The scaling type, either :code:`weak` or :code:`strong`.
:experiment.stderr: The :code:`stderr` of the :code:`experiment.command`.
:experiment.stdout: The :code:`stdout` of the :code:`experiment.command`.
:grid5000.arch: The architecture as reported by uname; usually :code:`x86_64`.
:grid5000.cluster: The name of the Grid'5000 cluster.
:grid5000.grd_jobid: The ID of the Grid'5000 job. Information about jobs is permanently stored in Grid'5000 servers; useful for debugging.
:grid5000.host.isa: The architecture as reported by Grid'500; usually :code:`x86-64`.
:grid5000.host.model: The model of the CPU as reported by Grid'5000.
:grid5000.host.model_other: The model of the CPU as reported by Grid'5000 (more details.)
:grid5000.host.sockets: The number of sockets of the CPU.
:grid5000.host.total_cores: The total number of cores available to the host; the number of CPU cores multiplied by number of sockets.
:grid5000.hosts: The number of hosts reserved in the cluster.
:grid5000.login: The login username to Grid'5000.
:grid5000.site: The Grid'5000 site in which the clusters belong to; :code:`grenoble`, :code:`rennes`, and so on.
:grid5000.total_cores: The total number of cores reserved; i.e. the number of hosts times the cores in each.
:software.dolfinx_parameters.hypre: A boolean :code:`true` or :code:`false`. Whether hypre is enabled or not. Hypre is disabled when complex math is enabled.
:software.packages.fenicsx-performance-tests: The version of the Debian package :code:`fenicsx-performance-tests`.
:software.packages.BLAS_PKG: The version of the Debian package :code:`$BLAS_PKG`; which BLAS packages are installed depends on :code:`--blas` (see also :code:`--blas-all`.)
:software.uname: The :code:`uname --kernel-name --kernel-release --kernel-version` string.

Also the following timings are available, but we do not individually describe them; they are all grabbed from the table printed in the :code:`stdout` output of the DOLFINx tested program. Some comments on their particular meaning can be found on this `FEniCS discourse post <https://fenicsproject.discourse.group/t/understanding-the-timings-of-performance-tests/14751/7>`_. We merely point out that :code:`wall_tot` is the total wall time a particular step took, while :code:`reps` is the number of repetitions of that step.

:timings.build_box_mesh.reps: 
:timings.build_box_mesh.wall_avg:
:timings.build_box_mesh.wall_tot:
:timings.build_dofmap_data.reps:
:timings.build_dofmap_data.wall_avg:
:timings.build_dofmap_data.wall_tot:
:timings.build_sparsity.reps:
:timings.build_sparsity.wall_avg:
:timings.build_sparsity.wall_tot:
:timings.compute_connectivity_20.reps:
:timings.compute_connectivity_20.wall_avg:
:timings.compute_connectivity_20.wall_tot:
:timings.compute_dof_reordering_map.reps:
:timings.compute_dof_reordering_map.wall_avg:
:timings.compute_dof_reordering_map.wall_tot:
:timings.compute_entities_dim2.reps:
:timings.compute_entities_dim2.wall_avg:
:timings.compute_entities_dim2.wall_tot:
:timings.compute_local_mesh_dual_graph.reps:
:timings.compute_local_mesh_dual_graph.wall_avg:
:timings.compute_local_mesh_dual_graph.wall_tot:
:timings.compute_local_to_global_links.reps:
:timings.compute_local_to_global_links.wall_avg:
:timings.compute_local_to_global_links.wall_tot:
:timings.compute_local_to_local_map.reps:
:timings.compute_local_to_local_map.wall_avg:
:timings.compute_local_to_local_map.wall_tot:
:timings.compute_nonlocal_mesh_dual_graph.reps:
:timings.compute_nonlocal_mesh_dual_graph.wall_avg:
:timings.compute_nonlocal_mesh_dual_graph.wall_tot:
:timings.compute_scotch_graph_partition.reps:
:timings.compute_scotch_graph_partition.wall_avg:
:timings.compute_scotch_graph_partition.wall_tot:
:timings.distribute_nodes_to_ranks.reps:
:timings.distribute_nodes_to_ranks.wall_avg:
:timings.distribute_nodes_to_ranks.wall_tot:
:timings.distribute_rowwise.reps:
:timings.distribute_rowwise.wall_avg:
:timings.distribute_rowwise.wall_tot:
:timings.gibbs_poole_stockmeyer_ordering.reps:
:timings.gibbs_poole_stockmeyer_ordering.wall_avg:
:timings.gibbs_poole_stockmeyer_ordering.wall_tot:
:timings.gps_create_level_structure.reps:
:timings.gps_create_level_structure.wall_avg:
:timings.gps_create_level_structure.wall_tot:
:timings.init_dofmap_from_element_dofmap.reps:
:timings.init_dofmap_from_element_dofmap.wall_avg:
:timings.init_dofmap_from_element_dofmap.wall_tot:
:timings.init_logging.reps:
:timings.init_logging.wall_avg:
:timings.init_logging.wall_tot:
:timings.init_mpi.reps:
:timings.init_mpi.wall_avg:
:timings.init_mpi.wall_tot:
:timings.init_petsc.reps:
:timings.init_petsc.wall_avg:
:timings.init_petsc.wall_tot:
:timings.petsc_krylov_solver.reps:
:timings.petsc_krylov_solver.wall_avg:
:timings.petsc_krylov_solver.wall_tot:
:timings.scotch_dgraphbuild.reps:
:timings.scotch_dgraphbuild.wall_avg:
:timings.scotch_dgraphbuild.wall_tot:
:timings.scotch_dgraphpart.reps:
:timings.scotch_dgraphpart.wall_avg:
:timings.scotch_dgraphpart.wall_tot:
:timings.sparsitypattern_finalize.reps:
:timings.sparsitypattern_finalize.wall_avg:
:timings.sparsitypattern_finalize.wall_tot:
:timings.topology_create.reps:
:timings.topology_create.wall_avg:
:timings.topology_create.wall_tot:
:timings.topology_shared_index_ownership.reps:
:timings.topology_shared_index_ownership.wall_avg:
:timings.topology_shared_index_ownership.wall_tot:
:timings.topology_vertex_groups.reps:
:timings.topology_vertex_groups.wall_avg:
:timings.topology_vertex_groups.wall_tot:
:timings.zzz_assemble_matrix.reps:
:timings.zzz_assemble_matrix.wall_avg:
:timings.zzz_assemble_matrix.wall_tot:
:timings.zzz_assemble_vector.reps:
:timings.zzz_assemble_vector.wall_avg:
:timings.zzz_assemble_vector.wall_tot:
:timings.zzz_create_boundary_conditions.reps:
:timings.zzz_create_boundary_conditions.wall_avg:
:timings.zzz_create_boundary_conditions.wall_tot:
:timings.zzz_create_facets_connectivity.reps:
:timings.zzz_create_facets_connectivity.wall_avg:
:timings.zzz_create_facets_connectivity.wall_tot:
:timings.zzz_create_forms.reps:
:timings.zzz_create_forms.wall_avg:
:timings.zzz_create_forms.wall_tot:
:timings.zzz_create_mesh.reps:
:timings.zzz_create_mesh.wall_avg:
:timings.zzz_create_mesh.wall_tot:
:timings.zzz_create_nearnullspace.reps:
:timings.zzz_create_nearnullspace.wall_avg:
:timings.zzz_create_nearnullspace.wall_tot:
:timings.zzz_create_rhs_function.reps:
:timings.zzz_create_rhs_function.wall_avg:
:timings.zzz_create_rhs_function.wall_tot:
:timings.zzz_functionspace.reps:
:timings.zzz_functionspace.wall_avg:
:timings.zzz_functionspace.wall_tot:
:timings.zzz_solve.reps:
:timings.zzz_solve.wall_avg:
:timings.zzz_solve.wall_tot:

Finally there is a schema version, currently set at :code:`1.0`.

:version: 1.0, the schema version. If the schema changes, this version will change.

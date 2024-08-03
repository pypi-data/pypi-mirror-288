.. _conffile:

The configuration file
======================

We provide an example configuration file under :file:`config/fenicsx-tests-gsoc2024.toml`. In order to launch its experiments, we would use:

.. code-block:: sh

   testbuddy-g5k --configuration config/fenicsx-tests-gsoc2024.toml launch

Generally, it is envisioned that you would write your own configuration files to declare the tests you would like to run on Grid'5000. The configuration files are using the TOML format. A configuration file has two sections, :code:`[sync]` and :code:`[launch]`. There are also three keys, :code:`login, project, name` that do not belong in those sections, and you would declare them at the top of the file:

.. code-block:: toml

   login = "g5k-username"
   project = "my-fenicsx-tests"
   name = "my-experiment"

This will log in to Grid'5000 with the username set to :code:`g5k-username`. The :code:`project` and :code:`name` keys will have the effect of testbuddy-g5k creating a directory :file:`~/testbuddy-g5k/my-fenics-tests/poisson`, and putting inside it all declared assets. The experiment is expected to store its results under and :file:`~/testbuddy-g5k/my-fenics-tests/my-experiments/results`. Note that this is per-server, meaning that under the Grid'5000 access point server you'd find corresponding assets under :file:`~/{site}`.

In a single configuration file, only one login, project, and name can be set. However, each experiment can declare its own assets, entrypoint, parameters, site, and grd options (i.e. how many hosts to run on, what type of CPU/GPU/hardware resources to request from Grid'5000, and so on.)

The [sync] section
------------------

These are the configuration options particular to the :code:`sync` subcommand of :code:`testbuddy-g5k`. Currently, there is only:

.. code-block:: toml

   results = "/local/path/to/results"

which will store all obtained tarballs from :code:`testbuddy sync` locally into :code:`/local/path/to/results`. This directory lies in the filesystem of the computer that runs testbuddy-g5k.

.. warning::

   In order for this feature to work, your experiments must store their results in tarballs under the directory :file:`{SRC_DIR}/results`, where :file:`{SRC_DIR}` is passed to the script by testbuddy-g5k via :code:`--src-dir=` (you cannot configure this; it is the directory :file:`/home/{login}/testbuddy-g5k/{project}/{name}`.)

The [launch] section
--------------------

In this section we declare the :code:`experiments` array which contains all the experiments that will be executed. Each experiment is a different job on its own resources in Grid'5000. Some options can be the same for all experiments, and are defined in their own keys under :code:`[launch]`, while others are defined within the elements of :code:`experiments`. For example:

.. code-block:: toml

   [launch]
   assets = [
     "/path/to/experiment_sources/",
     "/some/additional/directory/",
     "/some/additional/file/db.sqlite3"
   ]
   entrypoint = "entrypoint.py"
   grd_environment = "debian11-nfs"
   experiments = [
     { site = "rennes", cluster = "paravance", grd_options = "hosts=8" },
     { site = "grenoble", cluster = "dahu", grd_options = "hosts=4" }
   ]

What we call assets here are the source code files that will run an experiment.

This is a configuration of two experiments. In this configuration, both experiments have common assets and a common entrypoint, :file:`entrypoint.py`, as well as common :code:`grd_environment`, but they have different key values for :code:`site, cluster, grd_options`. The assets are placed under :file:`{site}/testbuddy-g5k/{project}/{name}`, and then :code:`entrypoint` is a filepath relative to that directory, i.e. :file:`{site}/testbuddy-g5k/{project}/{name}/{entrypoint}`. The entrypoint script will be executed on one host of those acquired, and typically coordinates all hosts in a cluster to work together for the experiment.

Note that the entrypoint script is passed in its first argument the directory in which it resides (this is because Grid'5000 launches the entrypoint from a different directory) so that the entrypoint can find all experiment assets.

.. admonition:: Keep it simple

   The configuration files allow for some cleverness, but it is best to avoid it and instead maintain simple configuration files, perhaps at the cost of some redundancy.

Overriding fields
-----------------

There's an interesting interplay between command-line options and declarative configuration files: We can use one to override the other.

Suppose we have a configuration :file:`example-config.toml` that defines the following experiments:

.. code-block:: toml

   experiments = [
     { site = "rennes", cluster = "paravance" },
     { site = "lyon", cluster = "nova" }
     { site = "grenoble", cluster = "dahu", grd_options = "hosts=8" }
   ]

For instance, perhaps we'd like to use :file:`example-config.toml` but request 2 hosts instead. We can of course edit the file or create a new configuration file, but for a one-off, we can do:

.. code-block:: sh

  testbuddy-g5k --configuration example-config.toml launch --grd-options hosts=2

This is equivalent to defining the :code:`grd_options` key in the launch section, and it will have the effect of being added to every experiment that does not already define its :code:`grd_options` key, i.e. the rennes and lyon clusters but not grenoble. If we would like to override all the :code:`grd_options` keys, including for experiments that define it (e.g. including grenoble), we must use :code:`--override-options`.

This is generally the interplay between the :code:`[launch]` section and :code:`experiments` array: you can define the fields for an experiment wholly within it, or you can define some common, between experiments, options in the :code:`[launch]` section. The fields in :code:`experiments` array take precedence unless :code:`--override-options` is used in which case precedence is reversed and the fields in :code:`[launch]` take precedence. The :code:`site:` and :code:`cluster` fields are the only fields that **must** be specified in an experiment.

Example: Add an experiment
==========================

Let's assume that you have a program that `computes the digits of π <https://en.wikipedia.org/wiki/Approximations_of_%CF%80>`_ to a certain precision. Let's say it's called :file:`compute_pi` and it can be distributed over `MPI <https://en.wikipedia.org/wiki/Message_Passing_Interface>`_. This program can either be a script on your computer (or a Debian package you can install with :code:`apt`; we assume the former case hereafter.) Let's say that this program also has an option :code:`--mode=` with two choices, :code:`fast` and :code:`memory` and an option :code:`--output` to store the π computation in a file.

Naturally you may write another script, say :code:`launch`, that does two things:

1) It parses testbuddy-g5k's :code:`--src-dir=SRC_DIR` option to pass down to :code:`compute_pi` the option `--output=SRC_DIR/pi_computation.txt`.
2) Runs :code:`compute_pi` in a :code:`mpiexec` context and passes down other options such as :code:`--mode=fast`.

.. warning::

   In the clean-up phase, :code:`launch` should store :file:`{SRC_DIR}/pi_computation.txt` in a tarball named :file:`{SRC_DIR}/results/{NAME}.tar.gz` where :code:`NAME` is decided by the script. This is important because the :file:`{SRC_DIR}/results` directory is hardcoded and where testbuddy-g5k expects the results to be in. If you don't do this, :code:`testbuddy-g5k sync` will not work.

Writing the configuration file
------------------------------

Assuming we have all this, let's write a :ref:`configuration file <conffile>` for testbuddy-g5k to launch this experiment:

.. code-block:: toml

  login = "your-Grid5000-login"
  project = "compute-pi"
  name = "my-experiment"

  [launch]
  assets = [
    "./scripts/compute_pi",
    "./scripts/launch"
  ]
  entrypoint = "launch"
  script_args = [
    "--mode=fast"
  ]
  experiments = [
    { site = "rennes", cluster = "paravance", grd_options = "host=8" },
    { site = "nantes", cluster = "econome", grd_options = "host=2" }
  ]

  [sync]
  results_dir = "/path/to/local/computer/compute-pi/my-experiment/results"

This script tells testbuddy-g5k the following:

1) In its *launch* mode, upload the assets to g5k under :file:`~/testbuddy-g5k/compute-pi/my-experiment`, request 8 hosts from :code:`paravance.rennes.grid5000.fr` and 2 hosts from :code:`econome.nantes.grid5000.fr` and then proceed to launch the entrypoint, i.e. the :code:`launch` script with arguments :code:`--src-dir=/home/your-Grid5000-login/testbuddy-g5k/compute-pi/my-experiment` and :code:`--mode=fast`.
2) In its *sync* mode, testbuddy-g5k will download all :file:`/home/your-Grid5000-login/testbuddy-g5k/compute-pi/my-experiment/*.tar.gz` tarballs into the local directory :file:`/path/to/local/computer/compute-pi/my-experiment/results` directory.

Launching the experiment
------------------------

We can now launch experiments and download the results. To wit:

.. code-block:: sh

   testbuddy-g5k --configuration myconf.toml launch
   mkdir -p /path/to/local/computer/compute-pi/my-experiment/results
   testbuddy-g5k --configuration myconf.toml sync

.. note::

   Testbuddy-g5k relies on :manpage:`ssh(1)` to establish connections. You must configure your SSH client to allow for passwordless login to :code:`access.grid5000.fr`.

Dry running
~~~~~~~~~~~

We can check what testbuddy-g5k intends to do with :code:`--dry-run`:

.. code-block:: sh

   testbuddy-g5k --dry-run --configuration myconf.toml launch
   Progress & Estimated Time Left  [------------------------------------]    0%
   [1/2] On compute-pi/my-experiment:
     Transferring assets into rennes/testbuddy-g5k/compute-pi/my-experiment with rsync...
   rsync --archive --recursive --compress --mkpath ./scripts/compute_pi ./scripts/launch your-Grid5000-login@access.grid5000.fr:rennes/testbuddy-g5k/compute-pi/my-experiment
     ==> OK.
     Requesting resources...
   ssh -o StrictHostKeyChecking=accept-new -l your-Grid5000-login -T -J access.grid5000.fr rennes.grid5000.fr grd bootstrap --resources {cluster='paravance'}/host=8 --detach --environment debiantesting-nfs --walltime '1:00:00' --terminate-after-script --script /home/your-Grid5000-login/testbuddy-g5k/compute-pi/my-experiment/launch --script-arg --src-dir=/home/your-Grid5000-login/testbuddy-g5k/compute-pi/my-experiment --script-arg --mode=fast
     ==> OK: [1/2] Resources will be available when Grid'5000 grants them.
   
   Progress & Estimated Time Left  [##################------------------]   50%
   [2/2] On compute-pi/my-experiment:
     Transferring assets into nantes/testbuddy-g5k/compute-pi/my-experiment with rsync...
   rsync --archive --recursive --compress --mkpath ./scripts/compute_pi ./scripts/launch your-Grid5000-login@access.grid5000.fr:nantes/testbuddy-g5k/compute-pi/my-experiment
     ==> OK.
     Requesting resources...
   ssh -o StrictHostKeyChecking=accept-new -l your-Grid5000-login -T -J access.grid5000.fr nantes.grid5000.fr grd bootstrap --resources {cluster='econome'}/host=2 --detach --environment debiantesting-nfs --walltime '1:00:00' --terminate-after-script --script /home/your-Grid5000-login/testbuddy-g5k/compute-pi/my-experiment/launch --script-arg --src-dir=/home/your-Grid5000-login/testbuddy-g5k/compute-pi/my-experiment --script-arg --mode=fast
     ==> OK: [2/2] Resources will be available when Grid'5000 grants them.
   
   Progress & Estimated Time Left  [####################################]  100%

Options and script arguments
----------------------------

If we'd like to now run the same configuration file but request 1 host from each cluster instead, we can override :code:`grd_options` as follows:

.. code-block:: sh

   testbuddy-g5k --configuration myconf.toml launch --grd-option host=1 --override-options

Script arguments cannot be overriden, but if we'd like to have the flexibility, we can remove :code:`script_args` from the configuration file and instead pass it as:

.. code-block:: sh

   testbuddy-g5k --configuration myconf.toml launch --script-args --mode=memory

Repeated script arguments may be passed by using :code:`--script-args` multiple times.

.. note::

   Testbuddy-g5k can override any option in the configuration via its corresponding command-line option (simply replace underscores by hyphens), or can be used without configuration files, instead specifying everything on the command line. The :code:`[launch]` and :code:`[sync]` sections in the TOML configuration correspond to the namesake testbuddy-g5k subcommands, i.e. :code:`testbuddy-g5k launch` and :code:`testbuddy-g5k sync`.

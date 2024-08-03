Installation
============

Installing via PyPI
-------------------

To install in a virtual environment using pip:

.. code-block:: sh

  python3 -m venv .venv
  source .venv/bin/activate
  pip install -U testbuddy-g5k

Dependencies
~~~~~~~~~~~~

Testbuddy-g5k makes use of :manpage:`ssh(1)` and :manpage:`rsync(1)`.

Testbuddy-g5k depends on the Python3 package `Click <https://click.palletsprojects.com/en/8.1.x/>`_ and has been tested with Python 3.11 on Debian 12.

Contributing
------------

If you would like to contribute to this project, the easiest way to start is to clone the `git repository <https://salsa.debian.org/_-/testbuddy-g5k>`_ and use `Poetry <https://python-poetry.org/>`_ to get a dev environment with all the dependencies.

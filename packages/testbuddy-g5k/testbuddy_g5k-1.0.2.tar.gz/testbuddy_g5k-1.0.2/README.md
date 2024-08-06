# Testbuddy-g5k

Testbuddy-g5k is a tool for declaratively defining experiments to be
launched from a local computer into
[Grid\'5000](https://www.grid5000.fr/w/Grid5000:Home)\'s clusters.

It was created as part of the Google Summer of Code 2024 Debian project
titled \"[Benchmarking Parallel Performance of Numerical MPI
Packages](https://summerofcode.withgoogle.com/programs/2024/projects/E9Jp7RUx)\",
mentored by Francesco Ballarin and Drew Parsons.

## Source code

The source code is contained in the `testbuddy_g5k` Python module
directory. The `fenicsx-tests-gsoc2024` directory contains an example
script that can be ran as an experiment, with its configuration in
`config/fenicsx-tests-gsoc2024.toml`; these files serve as a working
example for those interested in using testbuddy-g5k for their own
purposes.

## Documentation

The documentation can be read online
[here](https://_-.pages.debian.net/testbuddy-g5k).

The documentation can be found under `docs`. It may be built either
using the makefiles, e.g.

```
make clean html
```

or by using `sphinx-build`, e.g.

```
sphinx-build -b html docs/source docs/build
```

The CI will update the GitLab Pages when the `pages` branch is merged
with `main`.

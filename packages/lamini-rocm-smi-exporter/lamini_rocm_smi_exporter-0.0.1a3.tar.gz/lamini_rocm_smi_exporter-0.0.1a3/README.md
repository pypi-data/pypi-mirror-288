# rocm-smi-exporter

Export rocm-smi metrics as prometheus metrics

## Pants

[Pants](https://www.pantsbuild.org/2.21/docs/introduction/welcome-to-pants)
uses explicit `BUILD` files to track source files' dependencies and builds.

Pants is hermetic, means that the entire build environment is specified in
[pants.toml](pants.toml), which is copied from
[example-python](https://github.com/pantsbuild/example-python).
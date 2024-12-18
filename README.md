## explore_nwps

Simple Python scripts for exploring the file structure of numerical weather predictions on cloud object storage.

The main use-case is to help generate machine-readable descriptions of NWP datasets for [hypergrib](https://github.com/JackKelly/hypergrib).

## Plan for the MVP

### Scope

- Only consider the most recent version of GEFS (starting at `2020-09-23T12`).
  See [`hypergrib::datasets::gefs::version`](https://github.com/JackKelly/hypergrib/blob/0d55fb7d385a7363fa9c025ddc0c453969c251fa/crates/hypergrib/src/datasets/gefs/version.rs#L45-L58)
  for notes about the structure of the object keys.
- Only consider a small subset of coord labels where there are no missing coord combinations.
- Write the YAML primarily for consumption into Rust (later, we may also want to load into Python. But it'll be easier to modify the YAML in Python).
- Then write a minimal Rust `hypergrib` that loads the mostly hand-written YAML and pumps glorious GRIB data into `xarray`!

### Features

The ultimate goal is to output `yaml` which roughly conforms to the design sketch [here](https://github.com/JackKelly/hypergrib/blob/main/design.md#a-file-structure-for-describing-nwp-datasets).

That breaks down into these sub-tasks:

- Ensemble members and vertical levels (see issues [#3](https://github.com/JackKelly/explore_nwps/issues/3) and [#4](https://github.com/JackKelly/explore_nwps/issues/3)).
- Get a list of parameters & vertical levels by reading the contents of a sample of `.idx` files.
  See [issue #2](https://github.com/JackKelly/explore_nwps/issues/2).
  Start simple. We don't need an exhaustive list of parameters for the MVP.
- Get a list of horizontal spatial coordinates by reading a sample of GRIB files.
  See [issue #1](https://github.com/JackKelly/explore_nwps/issues/1).

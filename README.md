## explore_nwps

Simple Python scripts for exploring the file structure of numerical weather predictions on cloud object storage.

The main use-case is to help generate machine-readable descriptions of NWP datasets for [hypergrib](https://github.com/JackKelly/hypergrib) as part of the [project to make it super-easy to use weather forecast data](https://github.com/JackKelly/lets_make_it_super_easy_to_use_weather_forecast_data).

## Plan for the MVP (v0.1)

### Scope

- Only consider the most recent version of GEFS (starting at `2020-09-23T12`).
  See [`hypergrib::datasets::gefs::version`](https://github.com/JackKelly/hypergrib/blob/0d55fb7d385a7363fa9c025ddc0c453969c251fa/crates/hypergrib/src/datasets/gefs/version.rs#L45-L58)
  for notes about the structure of the object keys.
- Only consider a small subset of coord labels where there are no missing coord combinations.
- Write the YAML primarily for consumption into Rust (later, we may also want to load into Python. But it'll be easier to modify the YAML in Python).
- Then write a minimal Rust `hypergrib` that loads the mostly hand-written YAML and pumps glorious GRIB data into `xarray`!

### Features

The ultimate goal is to output `yaml` which all the dataset-specific information that `hypergrib` needs to open the dataset. See [this early version of some YAML describing GEFS](https://github.com/JackKelly/explore_nwps/blob/main/metadata/gefs/index.yaml).

That breaks down into these sub-tasks:

- [x] Manually list ensemble members and vertical levels (see issues [#3](https://github.com/JackKelly/explore_nwps/issues/3) and [#4](https://github.com/JackKelly/explore_nwps/issues/4)).
- [ ] Get a list of a few parameters & a few vertical levels.
  Start simple. We don't need an exhaustive list of parameters for the MVP.
  See [issue #2](https://github.com/JackKelly/explore_nwps/issues/2).
- Don't bother getting horizontal spatial coords for the MVP! We can just tell `xarray` that we don't have spatial coords.
- [ ] Once the metadata contains the above (minimal) items, go back to working on `hypergrib`, with the aim being to build an MVP for hypergrib, which doesn't contain any GEFS-specific code, and loads the metadata, and sends GRIB data through to `xarray` in Python!

## Plan for v0.2:
- [ ] Get the horizontal spatial coordinates by reading a sample of GRIB files, and encode these coord labels into the metadata. See [issue #1](https://github.com/JackKelly/explore_nwps/issues/1).
- [ ] Write Python code to exhaustively list all params & vertical levels, and determine which params are available for which vertical levels, forecast steps, and daily cycles. Start by visualising this. See [issue #5](https://github.com/JackKelly/explore_nwps/issues/5).
- [ ] Record if/when the number of ensemble members and/or steps changes. (Update: This is probably already in the MVP)

## Plan for v0.3:
- [ ] Decode the parameter abbreviation string and the string summarising the vertical level using the `grib_tables` sub-crate (so the user gets more information about what these mean, and so the levels can be put into order). Maybe provide a Python API to `grib_tables`. Or maybe just re-implement `grib_tables` in Python! It's pretty simple and not that performance-sensitive, and it'd be good to have other people be able to contribute to the code.

## Plan for v0.4
- [ ] Open other GRIB datasets. (If we have to parse the step from the body of `.idx` files then consider using [`nom`](https://crates.io/crates/nom)).
- [ ] Also need to decode `.idx` parameter strings like this (from HRRR): `var discipline=0 center=7 local_table=1 parmcat=16 parm=201`
- [ ] Optimise the extraction of the horizontal spatial coords from the GRIBs by only loading the relevant sections from the GRIBs (using the `.idx` files). Although this optimisation isn't urgent. Users will never have to run this step.


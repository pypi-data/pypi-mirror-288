"""
Support for testing

This covers (or could cover) both testing (e.g. comparing objects)
and generation of test/example instances.
"""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import Union

import cftime
import numpy as np
import pint
import xarray as xr

from input4mips_validation.cvs import Input4MIPsCVs
from input4mips_validation.dataset import (
    Input4MIPsDataset,
    Input4MIPsDatasetMetadataDataProducerMinimum,
)


def get_valid_ds_min_metadata_example(
    variable_id: str = "siconc",
    units: str = "%",
    unit_registry: Union[pint.registry.UnitRegistry, None] = None,
) -> tuple[xr.Dataset, Input4MIPsDatasetMetadataDataProducerMinimum]:
    """
    Get an example of a valid dataset and associated minimum metadata

    The results can be combined to create a
    [`Input4MIPsDataset`][input4mips_validation.dataset.Input4MIPsDataset].

    Parameters
    ----------
    variable_id
        Variable ID to apply to the dataset

    units
        Units to attach to the dataset

    unit_registry
        Unit registry to use.
        If not supplied, we retrieve it with
        [pint.get_application_registry][].

    Returns
    -------
    dataset :
        Example valid dataset

    minimum_metadata :
        Example minimum metadata
    """
    if unit_registry is None:
        ur: pint.registry.UnitRegistry = pint.get_application_registry()  # type: ignore

    metadata_minimum = Input4MIPsDatasetMetadataDataProducerMinimum(
        grid_label="gn",
        nominal_resolution="10000 km",
        source_id="CR-CMIP-0-2-0",
        target_mip="CMIP",
    )

    lon = np.arange(-165.0, 180.0, 30.0, dtype=np.float64)
    lat = np.arange(-82.5, 90.0, 15.0, dtype=np.float64)
    time = [
        cftime.datetime(y, m, 1) for y in range(2000, 2010 + 1) for m in range(1, 13)
    ]

    rng = np.random.default_rng()
    ds_data = ur.Quantity(
        rng.random((lon.size, lat.size, len(time))),
        units,
    )

    ds = xr.Dataset(
        data_vars={
            variable_id: (["lat", "lon", "time"], ds_data),
        },
        coords=dict(
            lon=("lon", lon),
            lat=("lat", lat),
            time=time,
        ),
        attrs={},
    )

    return ds, metadata_minimum


def create_files_in_tree(
    variable_ids: Iterable[str],
    units: Iterable[str],
    tree_root: Path,
    cvs: Input4MIPsCVs,
) -> list[Path]:
    """
    Create test files in a tree

    Parameters
    ----------
    variable_ids
        Variable IDs to write in the created files

    units
        Units to use in/assign to the created files

    tree_root
        Root of the tree in which to write the files

    cvs
        CVs to use when writing the files

    Returns
    -------
    :
        List of created files
    """
    written_files = []
    for variable_id, units in zip(variable_ids, units):
        ds, metadata_minimum = get_valid_ds_min_metadata_example(
            variable_id=variable_id, units=units
        )
        ds["time"].encoding = {
            "calendar": "proleptic_gregorian",
            "units": "days since 1850-01-01 00:00:00",
            "dtype": np.dtypes.Float32DType,
        }

        input4mips_ds = Input4MIPsDataset.from_data_producer_minimum_information(
            data=ds,
            metadata_minimum=metadata_minimum,
            standard_and_or_long_names={variable_id: {"standard_name": variable_id}},
            cvs=cvs,
        )

        written_file = input4mips_ds.write(root_data_dir=tree_root)

        written_files.append(written_file)

    return written_files

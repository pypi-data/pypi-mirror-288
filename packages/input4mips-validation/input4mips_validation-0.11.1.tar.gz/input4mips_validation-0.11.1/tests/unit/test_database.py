"""
Tests of `input4mips_validation.dataset`
"""

from __future__ import annotations

import pytest

from input4mips_validation.database import (
    Input4MIPsDatabaseEntryFile,
    dump_database_file_entries,
    load_database_file_entries,
)


@pytest.mark.parametrize(
    "inp",
    (
        pytest.param(
            (
                Input4MIPsDatabaseEntryFile(
                    Conventions="CF-1.7",
                    activity_id="input4MIPs",
                    contact="zebedee.nicholls@climate-resource.com;malte.meinshausen@climate-resource.com",
                    creation_date="2024-08-07T13:31:60Z",
                    dataset_category="GHGConcentrations",
                    datetime_end="2010-12-01T00:00:00Z",
                    datetime_start="2000-01-01T00:00:00Z",
                    esgf_dataset_master_id="input4MIPs.CMIP6Plus.CMIP.CR.CR-CMIP-0-2-0.atmos.mon.mole-fraction-of-carbon-dioxide-in-air.gn.v20240807",
                    filepath="/path/to/somewhere.nc",
                    frequency="mon",
                    further_info_url="http://www.tbd.invalid",
                    grid_label="gn",
                    institution_id="CR",
                    license="Long license text can go here. Multi-sentence perhaps",
                    license_id="CC BY 4.0",
                    mip_era="CMIP6Plus",
                    nominal_resolution="10000 km",
                    product=None,
                    realm="atmos",
                    region=None,
                    sha256="hashhere",
                    source_id="CR-CMIP-0-2-0",
                    source_version="0.2.0",
                    target_mip="CMIP",
                    time_range="200001-201012",
                    tracking_id="hdl:21.14100/tracking-id",
                    variable_id="mole_fraction_of_carbon_dioxide_in_air",
                    version="v20240807",
                    grid=None,
                    institution=None,
                    references=None,
                    source=None,
                ),
            ),
            id="standard",
        ),
        pytest.param(
            (
                Input4MIPsDatabaseEntryFile(
                    Conventions="CF-1.7",
                    activity_id="input4MIPs",
                    contact="zebedee.nicholls@climate-resource.com;malte.meinshausen@climate-resource.com",
                    creation_date="2024-08-07T13:31:60Z",
                    dataset_category="GHGConcentrations",
                    datetime_end=None,
                    datetime_start=None,
                    esgf_dataset_master_id="input4MIPs.CMIP6Plus.CMIP.CR.CR-CMIP-0-2-0.atmos.fx.areacella.gn.v20240807",
                    filepath="/path/to/somewhere.nc",
                    frequency="fx",
                    further_info_url="http://www.tbd.invalid",
                    grid_label="gn",
                    institution_id="CR",
                    license="Long license text can go here. Multi-sentence perhaps",
                    license_id="CC BY 4.0",
                    mip_era="CMIP6Plus",
                    nominal_resolution="10000 km",
                    product=None,
                    realm="atmos",
                    region=None,
                    sha256="hashhere",
                    source_id="CR-CMIP-0-2-0",
                    source_version="0.2.0",
                    target_mip="CMIP",
                    time_range=None,
                    tracking_id="hdl:21.14100/tracking-id",
                    variable_id="areacella",
                    version="v20240807",
                    grid=None,
                    institution=None,
                    references=None,
                    source=None,
                ),
            ),
            id="fixed_field",
        ),
    ),
)
def test_roundtrip(inp, tmp_path):
    dump_database_file_entries(inp, db_dir=tmp_path)

    res = load_database_file_entries(db_dir=tmp_path)

    assert set(res) == set(inp)

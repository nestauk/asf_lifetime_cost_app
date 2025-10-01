"""Data getters for inputs into lifetime cost calculations.

It includes functions to get the following data:
- inflation adjusted air source heat pump installation costs per decile and property archetype
- air source heat pump subsidy options data
- annual heat demand for each property archetype
- gas boiler installation costs per property archetype
"""

# package imports
import pandas as pd
import streamlit as st
import io
import boto3


def _read_s3_csv_to_dataframe(
    bucket_name: str,
    s3_key: str,
) -> pd.DataFrame:
    """
    Get dataframe from .csv file stored in S3.

    Args:
        bucket_name (str): S3 bucket name
        s3_key (str): Key of file in S3 bucket

    Returns:
        pd.DataFrame: Dataframe of content in .csv file
    """
    s3 = boto3.client("s3")
    obj = s3.get_object(Bucket=bucket_name, Key=s3_key)
    content = io.BytesIO(obj["Body"].read())
    return pd.read_csv(content)

@st.cache_data
def get_ashp_installation_costs() -> pd.DataFrame:
    """Get dataframe of inflation-adjusted ashp installations costs.

    Installation costs are for each decile in different property archetypes.

    Returns:
        pd.DataFrame: Dataframe of air-source heat pump installation costs
    """
    data = _read_s3_csv_to_dataframe(
        bucket_name="asf-lifetime-cost-model",
        s3_key="inputs/ashp_installation_costs.csv",
    )
    data.set_index("archetype_label", inplace=True)
    return data


@st.cache_data
def get_property_heat_demand() -> pd.DataFrame:
    """Get dataframe of average heat demand data from S3 for each property archetype.

    Returns:
        pd.DataFrame: Dataframe of average heat demand
    """
    data = _read_s3_csv_to_dataframe(bucket_name="asf-lifetime-cost-model", s3_key="inputs/property_heat_demand.csv")
    data.set_index("archetype_label", inplace=True)
    return data

@st.cache_data
def get_ashp_subsidy_options_data() -> pd.DataFrame:
    """Gets dataframe of air source heat pump subsidy options data from S3.

    There's a column for each year between 2024 and 2035 and each option
    is provided as a row in the dataset. Options include:
        - "flat"
        - "slow stepdown"
        - "fast stepdown"
        - "high"
        - "zero from 2028"
        - "smallest"
        - "no subsidy"
    For each pair of year and option, the value is the amount in GBP for subsidising the cost of getting an air source
    heat pump in that year.

    Returns:
        pd.DataFrame: Dataframe of subsidy options
    """
    return _read_s3_csv_to_dataframe(
        bucket_name="asf-lifetime-cost-model",
        s3_key="inputs/ashp_subsidy_options.csv",
    )


@st.cache_data
def get_gas_boiler_installation_costs() -> pd.DataFrame:
    """Gets dataframe of gas boiler costs from S3.

    For reference, the numbers are taken from the NESO heating tech options project (2025).

    Returns:
        pd.DataFrame: Dataframe of boiler costs for different property sizes.
    """
    data = _read_s3_csv_to_dataframe(
        bucket_name="asf-lifetime-cost-model",
        s3_key="inputs/gas_boiler_installation_costs.csv",
    )
    data.set_index("archetype_label", inplace=True)
    return data


def get_installation_cost(costs_data: pd.DataFrame, heating_system: str, decile: int = None) -> pd.DataFrame:
    """Gets the cost of a heating system for different archetypes (and a specific decile, where applicable).

    Args:
        costs_data (pd.DataFrame): DataFrame containing installation costs for different property archetypes.
        heating_system (str): heating system.
            Takes "ashp" (for air source heat pump) or "boiler" (for gas boiler).
        decile (int): cost decile, only applicable when heating system is "ashp" air source heat pumps.
            Takes multiples of 10 between 10 and 90, inclusive.

    Raises:
        ValueError: If the heating system inputed is not supported
                    or the decile is not a multiple of 10 between 10 and 90.

    Returns:
        pd.DataFrame: A DataFrame with property archetypes as index and installation cost as column.
    """
    if decile is not None and (decile < 10 or decile > 90 or decile % 10 != 0):
        raise ValueError("Decile must be a multiple of 10 between 10 and 90, inclusive.")

    if heating_system == "ashp":
        costs_data = costs_data[[f"cost_percentile_{decile}"]].rename(
            columns={f"cost_percentile_{decile}": "installation_cost"}
        )
    elif heating_system == "boiler":
        costs_data = costs_data.rename(columns={"cost": "installation_cost"})
    else:
        raise ValueError(
            f"Unsupported heating system: {heating_system}. Supported heating systems are `ashp` and `boiler`."
        )

    return costs_data

import pandas as pd

from .. import settings


def factly_std_names(filter: str = None):

    if filter:
        if filter == "country":
            data = pd.read_csv(settings.COUNTRY_NAMES_URL)
            return data["standard_country_name"].drop_duplicates().dropna().tolist()
        else:
            data = pd.read_csv(settings.STANDARD_NAMES_URL)
            return data[filter].dropna().tolist()

    std_data = pd.read_csv(settings.STANDARD_NAMES_URL)
    country_std_data = pd.read_csv(settings.COUNTRY_NAMES_URL)

    std_dict = {col: std_data[col].dropna().tolist() for col in std_data.columns}
    std_dict["country"] = (
        country_std_data["standard_country_name"].drop_duplicates().dropna().tolist()
    )

    return std_dict

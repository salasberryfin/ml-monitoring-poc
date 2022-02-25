import json

import pandas as pd
from sklearn import datasets, utils

from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab

from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection


def save_to_file(result: Dashboard, name: str = "report") -> str:
    result.save(f"{name}.html")

    return f"{name}.html"


def data_drift_dashboard(frame: pd.DataFrame, save: bool = False):
    dashboard = Dashboard(tabs=[DataDriftTab(verbose_level=1)])
    dashboard.calculate(frame[:75], frame[75:], column_mapping=None)
    # show only available in Jupyter Notebook
    # dashboard.show()
    if save:
        save_to_file(dashboard)


def data_drift_profile(frame: pd.DataFrame):
    profile = Profile(sections=[DataDriftProfileSection()])
    profile.calculate(frame[:75], frame[75:], column_mapping=None)
    # print(f"Data Drift profile: {profile.json()}")
    with open("data_drift_result.json", "w+") as result_file:
        json.dump(json.loads(profile.json()), result_file, indent=4)


def main(name: str) -> pd.DataFrame:
    dataset = utils.Bunch()
    if name == "iris":
        dataset = datasets.load_iris()

    frame = pd.DataFrame(
            dataset.data,
            columns=dataset.feature_names)
    frame["target"] = dataset.target

    return frame


if __name__ == "__main__":
    frame = main("iris")
    data_drift_dashboard(frame, True)
    data_drift_profile(frame)

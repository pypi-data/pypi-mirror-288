import requests
import pandas as pd
from pandas import DataFrame
import numpy as np
import pytz
from typing import Dict
from datetime import datetime, timedelta

# import matplotlib.pyplot as plt
# from PIL._imaging import display
# from tabulate import tabulate
import os


class Project:
    """
    project object class
    """

    def __init__(self, project_id, cur_user):
        self.cur_user = cur_user
        # raise error if user is not logged in
        if not self.cur_user.active:
            raise ValueError("User is not logged in.")
        self.project_id = project_id
        self.project_name = self.get_project_info()["name"]
        self.utc_tz = "UTC"
        self.project_tz = self.get_project_info()["timezone"]
        """
        project_sensor_types_dic = {
            idx: sensorType
        }
        """
        self.project_sensor_types_dic = {}
        """
        project_asset_types_dic = {
            idx: (assetType, assetId)
        }
        """
        self.project_asset_types_dic = {}

    def get_project_info(self) -> Dict:
        """
        get project JSON information
        """
        try:
            response = requests.get(
                f"{self.cur_user.base_url}/projects/{self.project_id}",
                headers=self.cur_user.headers,
                timeout=5,
            )
            response.raise_for_status()
            project_info = response.json()
            return project_info
        except requests.exceptions.RequestException as e:
            print("Get project info failed: ", e)
            return None

    def get_project_users(self) -> DataFrame:
        """
        get project users list DataFrame
        """
        try:
            response = requests.get(
                f"{self.cur_user.base_url}/users",
                headers=self.cur_user.headers,
                timeout=5,
            )
            response.raise_for_status()
            users = response.json()
            # create dataframe for all usernames
            first_name = [
                user["firstName"]
                for user in users
                if self.project_id in user["projects"]
            ]
            last_name = [
                user["lastName"]
                for user in users
                if self.project_id in user["projects"]
            ]
            data = {"fistname": first_name, "lastname": last_name}
            users_df = pd.DataFrame(data)
            return users_df
        except requests.exceptions.RequestException as e:
            print("Get project users failed: ", e)
            return None

    def list_users(self) -> None:
        """
        list project users
        """
        users_df = self.get_project_users()
        print("\n========= Project Users ===========")
        print(users_df.to_string(index=False))
        print("===============================================")

    def get_sensor_types(self) -> DataFrame:
        """
        get project sensor types DataFrame
        """
        try:
            response = requests.get(
                f"{self.cur_user.base_url}/v2/projects/{self.project_id}/sensors/kpi/keyfigures",
                headers=self.cur_user.headers,
                timeout=5,
            )
            response.raise_for_status()
            sensor_types = response.json()
            # create sensor_type_df
            sensor_name = [i["type"] for i in sensor_types["sensorTypeCounts"]]
            data = {"SensorType": sensor_name}
            sensor_type_df = pd.DataFrame(data)
            sensor_type_df = sensor_type_df.sort_values(by=["SensorType"])
            sensor_type_df.insert(
                0,
                "SensorNo.",
                np.linspace(1, len(sensor_type_df), len(sensor_type_df)).astype(int),
                True,
            )
            # create project_sensor_types_dic based on sensor_type_df
            self.project_sensor_types_dic = dict(
                zip(
                    sensor_type_df["SensorNo."],
                    sensor_type_df["SensorType"].values.tolist(),
                )
            )
            return sensor_type_df
        except requests.exceptions.RequestException as e:
            print("Get project sensor types failed: ", e)
            return None

    def list_sensor_types(self, show=False) -> None:
        """
        list project sensors types
        """
        sensor_type_df = self.get_sensor_types()
        print("\n========= Project Sensor Types ===========")
        if show:
            print(sensor_type_df.to_string(index=False))
        print("==========================================")

    def get_sensor_type(self, sensor_id) -> None:
        """
        get sensor type by sensor_id
        """
        try:
            response = requests.get(
                f"{self.cur_user.base_url}/v2/projects/{self.project_id}/sensors/{sensor_id}",
                headers=self.cur_user.headers,
                params={"lang": "en"},
                timeout=5,
            )
            response.raise_for_status()
            sensor = response.json()
            return sensor["type"]
        except requests.exceptions.RequestException as e:
            print("Get sensor type by id failed: ", e)
            return None

    def get_sensor_id(self, sensor_code) -> str:
        """
        return sensor_id given sensor_code
        """
        response = requests.post(
            f"{self.cur_user.base_url}/v2/projects/{self.project_id}/sensors/search",
            headers=self.cur_user.headers,
            timeout=5,
        )
        sensors = response.json()
        for sensor in sensors:
            if sensor["code"] == sensor_code:
                return sensor["id"]
        return "sensor_id not found"

    def get_sensors_info(self) -> Dict:
        """
        get project sensors tree JSON
        """
        try:
            payload = {"with": ["acquiredDatapoints", "derivedDatapoints", "location"]}
            response = requests.post(
                f"{self.cur_user.base_url}/v2/projects/{self.project_id}/sensors/search",
                headers=self.cur_user.headers,
                json=payload,
                timeout=5,
            )
            response.raise_for_status()
            sensors = response.json()
            return sensors
        except requests.exceptions.RequestException as e:
            print("Get project sensors tree failed: ", e)
            return None

    def get_asset_types(self) -> DataFrame:
        """
        get project asset types DataFrame
        """
        try:
            response = requests.get(
                f"{self.cur_user.base_url}/v2/projects/{self.project_id}/asset-types",
                headers=self.cur_user.headers,
                timeout=5,
            )
            response.raise_for_status()
            asset_types = response.json()
            # create asset_type_df
            data = {
                "AssetType": [asset["code"] for asset in asset_types],
                "AssetId": [asset["id"] for asset in asset_types],
            }
            asset_type_df = pd.DataFrame(data)
            asset_type_df = asset_type_df.sort_values(by=["AssetType"])
            asset_type_df.insert(
                0,
                "AssetNo.",
                np.linspace(1, len(asset_type_df), len(asset_type_df)).astype(int),
                True,
            )
            # create project_sensor_types_dic based on asset_type_df
            self.project_asset_types_dic = dict(
                zip(
                    asset_type_df["AssetNo."],
                    zip(asset_type_df["AssetType"], asset_type_df["AssetId"]),
                )
            )
            return asset_type_df.drop(columns=["AssetId"])
        except requests.exceptions.RequestException as e:
            print("Get project asset types failed: ", e)
            return None

    def list_asset_types(self, show=False) -> None:
        """
        list project asset types
        """
        asset_type_df = self.get_asset_types()
        print("\n========= Project Asset Types ===========")
        if show:
            print(asset_type_df.to_string(index=False))
        print("==========================================")

    def get_asset_type_id(self, asset_id) -> None:
        """
        get asset type by asset_id, return asset_type id
        """
        try:
            response = requests.get(
                f"{self.cur_user.base_url}/v2/projects/{self.project_id}/assets/{asset_id}",
                headers=self.cur_user.headers,
                params={"lang": "en"},
                timeout=5,
            )
            response.raise_for_status()
            asset = response.json()
            return asset["assetType"]
        except requests.exceptions.RequestException as e:
            print("Get asset type id by id failed: ", e)
            return None

    def get_asset_id(self, asset_code) -> str:
        """
        return asset_id given asset_code
        """
        response = requests.post(
            f"{self.cur_user.base_url}/v2/projects/{self.project_id}/assets/search",
            headers=self.cur_user.headers,
            timeout=5,
        )
        assets = response.json()
        for asset in assets["data"]:
            if asset["code"] == asset_code:
                return asset["id"]
        return "asset_id not found"

    def get_assets_info(self) -> Dict:
        """
        get project assets tree JSON
        """
        try:
            payload = {"with": ["acquiredDatapoints", "derivedDatapoints", "location"]}
            response = requests.post(
                f"{self.cur_user.base_url}/v2/projects/{self.project_id}/assets/search",
                headers=self.cur_user.headers,
                json=payload,
                timeout=5,
            )
            response.raise_for_status()
            sensors = response.json()
            return sensors
        except requests.exceptions.RequestException as e:
            print("Get project sensors tree failed: ", e)
            return None

    def export_dailycheck_report(
        self, sensor_types, asset_types, include_coord, timeout, export_path
    ) -> None:
        """
        export dailycheck excel report
        """
        print(" ... Generating dailycheck excel sheet ...")
        try:
            color_report_styler = self.get_dailycheck_report(
                sensor_types, asset_types, include_coord, timeout
            )
            # save as xlsx without column 'AlarmColor'
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")
            project_folder = self.project_name.replace("/", "_").replace(
                "\\", "_"
            )  # avoid path error
            export_path = f"{export_path}\\dailycheckSheet\\{project_folder}"
            # Create the folder
            if not os.path.exists(export_path):
                os.makedirs(export_path)
            writer = pd.ExcelWriter(
                f"{export_path}\\{project_folder}_{current_time}.xlsx",
                engine="xlsxwriter",
            )
            color_report_styler.to_excel(
                writer,
                sheet_name="Your sheet name",
                index=False,
            )
            worksheet, color_report_df = (
                writer.sheets["Your sheet name"],
                color_report_styler.data,
            )
            # Adjust column width
            for idx, col in enumerate(
                color_report_df.columns
            ):  # Loop through all columns
                max_len = (
                    max(
                        color_report_df[col]
                        .astype(str)
                        .map(len)
                        .max(),  # Length of the largest item in the column
                        len(str(col)),  # Length of the column name/header
                    )
                    + 1
                )  # Adding a little extra space
                worksheet.set_column(
                    first_col=idx, last_col=idx, width=max_len
                )  # Set column width
            header_row, num_cols = 0, len(color_report_styler.columns)
            # Apply autofilter to the header row
            worksheet.autofilter(header_row, 0, header_row, num_cols - 1)
            # Freeze the header row
            worksheet.freeze_panes(header_row + 1, 0)
            writer.close()
            print(f"Dailycheck report successfully exported to: {export_path}")
        except Exception as e:
            print("Dailycheck report export failed: ", e)

    def get_dailycheck_report(self, sensor_types, asset_types, include_coord, timeout):
        """
        get dailycheck report Styler object with colors applied based on alarms
        """
        items = [
            "sensorName",
            "sensorType",
            "sensorID",
            "pointName",
            "pointType",
            f"timeStamp [{timeout} hr timeout]",
            "lastValue",
            "unit",
            "alarmStatus",
            "alarmTime",
            "threshold",
            "alarmColor",
            "lng/X",
            "lat/Y",
            "alt/Z",
        ]
        report = {item: [] for item in items}
        sensors, assets = self.get_sensors_info(), self.get_assets_info()
        project_alarms = self.get_project_alarms(status=["Open"])
        parent_cache = {None: None}  # cache parent_type result to speed-up
        ##### sensors #####
        for sensor in sensors:
            # skip if not in user's selection of sensors (current and parent)
            parent_id = sensor["parentId"]
            if parent_id not in parent_cache:
                parent_cache[parent_id] = self.get_sensor_type(parent_id)
            parent_type = parent_cache[parent_id]
            if sensor["type"] not in sensor_types and parent_type not in sensor_types:
                continue
            # acquired points
            for pt_type in ["acquiredDatapoints", "derivedDatapoints"]:
                if pt_type in sensor and sensor[pt_type]:
                    for pt in sensor[pt_type]:
                        ########### alarm status ###########
                        for alarm_item, alarm_val in zip(
                            ["alarmStatus", "alarmTime", "threshold", "alarmColor"],
                            list(self.get_alarm_status(project_alarms, sensor, pt)),
                        ):
                            report[alarm_item].append(alarm_val)
                        ########### sensors ###########
                        report["sensorName"].append(sensor["code"])
                        report["sensorType"].append(parent_type or sensor["type"])
                        report["sensorID"].append(sensor["id"])
                        report["lng/X"].append(
                            sensor["location"]["lng"] if sensor["location"] else None
                        )
                        report["lat/Y"].append(
                            sensor["location"]["lat"] if sensor["location"] else None
                        )
                        report["alt/Z"].append(
                            sensor["location"]["alt"] if sensor["location"] else None
                        )
                        ########### datapoints ###########
                        report["pointName"].append(pt["code"])
                        report["pointType"].append(
                            "acquired" if pt_type == "acquiredDatapoints" else "derived"
                        )
                        ########### unit ###########
                        report["unit"].append(pt["unit"] if "unit" in pt else None)
                        ########### lastValue, lastTime ###########
                        report["lastValue"].append(
                            pt.get("lastValidValue", {}).get(
                                "v"
                                if (
                                    "m0" not in pt
                                    or pt.get("m0", {}).get("value") is None
                                )
                                else "dv"
                            )
                        )
                        report[f"timeStamp [{timeout} hr timeout]"].append(
                            pd.to_datetime(
                                self.from_utc_to_project_tz(
                                    pt.get("lastValidValue", {}).get("t", "")[:-5]
                                )
                            )
                            if "lastValidValue" in pt and "t" in pt["lastValidValue"]
                            else None
                        )
        ##### assets #####
        for asset in assets["data"]:
            # skip if not in user's selection of sensors (current and parent)
            parent_id = asset["parentId"]
            if parent_id not in parent_cache:
                parent_cache[parent_id] = self.get_asset_type_id(parent_id)
            parent_type_id = parent_cache[parent_id]
            if asset["id"] not in asset_types and parent_type_id not in asset_types:
                continue
            # acquired points
            for pt_type in ["acquiredDatapoints", "derivedDatapoints"]:
                if pt_type in asset and asset[pt_type]:
                    for pt in asset[pt_type]:
                        ########### alarm status ###########
                        for alarm_item, alarm_val in zip(
                            ["alarmStatus", "alarmTime", "threshold", "alarmColor"],
                            list(self.get_alarm_status(project_alarms, asset, pt)),
                        ):
                            report[alarm_item].append(alarm_val)
                        ########### sensors ###########
                        report["sensorName"].append(asset["code"])
                        report["sensorType"].append(parent_type or asset["assetType"])
                        report["sensorID"].append(asset["id"])
                        report["lng/X"].append(
                            asset["location"]["lng"] if asset["location"] else None
                        )
                        report["lat/Y"].append(
                            asset["location"]["lat"] if asset["location"] else None
                        )
                        report["alt/Z"].append(
                            asset["location"]["alt"] if asset["location"] else None
                        )
                        ########### datapoints ###########
                        report["pointName"].append(pt["code"])
                        report["pointType"].append(
                            "acquired" if pt_type == "acquiredDatapoints" else "derived"
                        )
                        ########### unit ###########
                        report["unit"].append(pt["unit"] if "unit" in pt else None)
                        ########### lastValue, lastTime ###########
                        report["lastValue"].append(
                            pt.get("lastValidValue", {}).get(
                                "v"
                                if (
                                    "m0" not in pt
                                    or pt.get("m0", {}).get("value") is None
                                )
                                else "dv"
                            )
                        )
                        report[f"timeStamp [{timeout} hr timeout]"].append(
                            pd.to_datetime(
                                self.from_utc_to_project_tz(
                                    pt.get("lastValidValue", {}).get("t", "")[:-5]
                                )
                            )
                            if "lastValidValue" in pt and "t" in pt["lastValidValue"]
                            else None
                        )
        try:
            report_df = pd.DataFrame(report)
        except ValueError as e:
            print("Report data might not have same length:", e)
            return None
        report_df = report_df.sort_values(
            by=["sensorType", "sensorName", "pointType", "pointName"]
        )
        # exclude coordination info
        if not include_coord:
            report_df = report_df.drop(columns=["lng/X", "lat/Y", "alt/Z"])
        # apply color to report_df
        color_report_styler = self.apply_color_to_report(report_df, timeout)
        return color_report_styler

    def apply_color_to_report(self, report_df, timeout):
        """
        color dataframe based on column 'alarmColor' with styler
        return report_df Styler object
        """

        def highlight_rows(row, alarm_colors):
            return [f"background-color: {alarm_colors[row.name]}" for _ in row]

        def highlight_timeout(dt):
            now = datetime.now()
            return f"background-color: {'red' if dt < now - timedelta(hours=timeout) else None}"

        try:
            alarm_colors = report_df["alarmColor"]  # store alarmColors
            report_df.drop(
                columns=["alarmColor"], inplace=True
            )  # drop alarmColor column
            color_report_styler = report_df.style.apply(
                highlight_rows, axis=1, alarm_colors=alarm_colors
            ).map(highlight_timeout, subset=[f"timeStamp [{timeout} hr timeout]"])
            return color_report_styler
        except AttributeError as e:
            print("Apply color to report failed:", e)
            return None

    def from_utc_to_project_tz(self, dt) -> str:
        """
        convert datetime str from UTC to project timezone
        """
        from_tz, to_tz = pytz.timezone("UTC"), pytz.timezone(self.project_tz)
        dt = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
        dt = from_tz.localize(dt).astimezone(to_tz)
        dt = dt.strftime("%Y-%m-%d %H:%M:%S")
        return dt

    def from_project_to_utc_tz(self, dt) -> str:
        """
        convert datetime str from project to UTC timezone
        """
        from_tz, to_tz = pytz.timezone(self.project_tz), pytz.timezone("UTC")
        dt = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
        dt = from_tz.localize(dt).astimezone(to_tz)
        dt = dt.strftime("%Y-%m-%d %H:%M:%S")
        return dt

    def get_alarm_status(self, project_alarms, sensor, pt):
        """
        given project alarms_dic returned from get_alarms()
        return alarm_status:
        """
        alarmTime = alarmLevel = threshold = alarmColor = None
        if (sensor["id"], pt["code"]) in project_alarms:
            levels = {
                1: "Level 1",
                2: "Level 2",
                3: "Level 3",
                4: "Level 4",
                5: "Level 5",
            }
            types = {1: "low", 2: "high", 3: "no data"}
            alarm = project_alarms[(sensor["id"], pt["code"])]
            alarmType, alarmTime = alarm["alarmType"], self.from_utc_to_project_tz(
                alarm["alarmTime"]
            )
            # get alarm limit status
            level, tp = alarmType % 10, types[alarmType // 100]
            if alarmType // 100 != 3:
                # loop thru limits
                for i, limit in enumerate(pt["alarm"]["limits"]):
                    if level == i + 1:
                        alarmLevel = (
                            limit["label"]
                            if limit["label"] not in levels
                            else f"{tp} {level}"
                        )
                        threshold, alarmColor = limit[tp], limit["color"]
                        break
            else:
                alarmLevel = f"{tp} {level}"
                threshold = pt["noData"][
                    ["low", "high"][level - 1] if level in [1, 2] else None
                ]
                alarmColor = (
                    ["#DCDCDC", "#A9A9A9"][level - 1] if level in [1, 2] else None
                )
        return alarmLevel, alarmTime, threshold, alarmColor

    def get_project_alarms(self, status) -> Dict:
        """
        return current open project alarm events in dict
        (sensor_id, pt_code): {
                'alarmType': level_1
                'alarmTime': datetime
            }
        """
        try:
            body = {"filter": {"statuses": status}}
            response = requests.post(
                f"{self.cur_user.base_url}/v2/projects/{self.project_id}/alarms/search/en",
                headers=self.cur_user.headers,
                json=body,
                timeout=5,
            )
            response.raise_for_status()
            alarms = response.json()
            project_alarms = {
                (event["entity"]["id"], event["datapoint"]["code"]): {
                    "alarmType": event["alarmType"],
                    "alarmTime": event["createdAt"][:-5],
                }
                for event in alarms["data"]
                if "entity" in event
            }
            return project_alarms
        except requests.exceptions.RequestException as e:
            print("Get project alarms failed: ", e)
            return None

import requests
import pwinput
import pandas as pd


class User:
    """
    user object class
    """

    def __init__(self):
        self.active = False
        self.env = "prod"
        self.area = "North America"
        self.base_url = self.api_url_area(self.env)
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "sxd-application": "beyond-monitoring",
        }
        """
        project_dic = {
            idx: [projectID, projectName]
        }
        """
        self.project_dic = {}

    def api_url_area(self, env):
        """
        return api base_url given user login area
        """
        switch = {
            "North America": "https://api.beyond-monitoring.co/api",
            "Europe": "https://api.beyond-monitoring.com/api",
            "Australia": "https://api.beyond-monitoring.com.au/api",
        }
        return switch.get(env, "Invalid env")

    def select_area(self):
        """
        Function asking user to select area
        """
        print("======= Provide Login Area =========")
        while True:
            areas = {"0": "North America", "1": "Europe", "2": "Australia"}
            for option, detail in areas.items():
                print(f"{option}\t\t{detail}")
            print("===========================")
            try:
                self.area = areas[input("Select user area: ")]
            except KeyError:
                print("Invalid area!\n")
                continue
            self.base_url = self.api_url_area(self.area)
            print(f"Area set to {self.area}.\n")
            break

    def login(self):
        """
        user login function (including 2MFA function)
        """
        data, url = {}, f"{self.base_url}/users/login"
        while True:
            data["email"] = input("Username: ")
            data["password"] = pwinput.pwinput(prompt="Password: ", mask="*")
            try:
                r = requests.post(url, json=data, timeout=5)
                r.raise_for_status()
                rj = r.json()
                if not rj["mfaEnabled"]:
                    self.headers["authorization"] = "Bearer " + rj["token"]
                    print(
                        "====== WARNING!! 2FA account login recommended to avoid potential errors ======"
                    )
                break
            except requests.exceptions.RequestException as e:
                print("Login credential incorrect: ", e)

        # require 2FA authentication
        url = f"{self.base_url}/users/totp-login"
        while "authorization" not in self.headers:
            data["code"] = pwinput.pwinput(
                prompt="Enter your 6-digit authentication code: ", mask="*"
            )
            data["isTotpCode"] = True
            try:
                r = requests.post(url, json=data, timeout=5)
                r.raise_for_status()
                rj = r.json()
                self.headers["authorization"] = "Bearer " + rj["token"]
            except requests.exceptions.RequestException as e:
                print("Invalid 2FA code: ", e)
        # mark user object as login
        self.active = True
        print("\n====== Log in successful :) ======\n")

    def logout(self):
        """
        user logout, wipe all user credential
        """
        # self.env = "prod"
        self.area = "North America"
        self.base_url = self.api_url_area(self.env)
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "sxd-application": "beyond-monitoring",
        }
        self.project_dic = {}
        self.active = False
        print("\n====== (: Log out ======\n")

    def get_user_projects(self):
        """
        get user's projects and return project_dic
        """
        try:
            response = requests.get(
                f"{self.base_url}/projects", headers=self.headers, timeout=5
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print("Get user projects failed: ", e)
        projects = response.json()
        project_data = {
            "ProjectName": [project["name"] for project in projects],
            "ProjectID": [project["id"] for project in projects],
        }
        # create project_df
        project_df = pd.DataFrame(project_data)
        project_df = project_df.sort_values(by=["ProjectName"])
        project_df.insert(
            0,
            "ProjectNo.",
            [str(i) for i in range(1, len(project_df) + 1)],
            True,
        )
        # create project_dic based on project_df
        self.project_dic = dict(
            zip(
                project_df["ProjectNo."],
                project_df[["ProjectID", "ProjectName"]].values.tolist(),
            )
        )
        return project_df

    def list_user_projects(self):
        """
        list user's projects
        """
        project_df = self.get_user_projects()
        print("\n========= Your Available Projects ===========")
        print(project_df.to_string(index=False))
        print("===============================================")

    def api_url_env(self, env):
        """
        return api base_url given user login environment
        """
        switch = {
            "local": "http://localhost:3000/api",
            "staging": "https://staging-api.beyond-monitoring.co/api",
            "qa": "https://qa-api.beyond-monitoring.co/api",
            "rc": "https://rc-api.beyond-monitoring.co/api",
            "pp": "https://pp2-api.beyond-monitoring.co/api",
            "prod": "https://api.beyond-monitoring.co/api",
        }
        return switch.get(env, "Invalid env")

    def select_environment(self):
        """
        Function asking user to select environment
        """
        print("======= Provide Login Info =========")
        while True:
            option = input(
                "** Default environment set to prod, change to another mode? [Y/N]: "
            )
            if option.upper() not in ["Y", "N"]:
                print("Provide a valid option!\n")
                continue
            if option.upper() == "Y":
                self.env = input(
                    "** Provide login environment [staging / qa / rc / pp]: "
                )
                if self.env.lower() not in ["staging", "qa", "rc", "pp", "prod"]:
                    print("Invalid environment!\n")
                    continue
                self.env = self.env.lower()
                self.base_url = self.api_url_env(self.env)
                if self.env == "prod":
                    print("Already in prod mode.\n")
            break

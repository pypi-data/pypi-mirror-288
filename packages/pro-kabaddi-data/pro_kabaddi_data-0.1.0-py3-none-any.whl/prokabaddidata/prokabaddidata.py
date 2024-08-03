# kabaddi_data.py


from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import json


WEBSITE_URL_1_PREFIX = "https://www.prokabaddi.com"


class KabaddiDataAggregator:
    def __init__(self, headless=True):
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)

    def __del__(self):
        self.driver.quit()

    def get_all_team_names(self):
        self.driver.get(f"{WEBSITE_URL_1_PREFIX}/teams")
        elements = self.driver.find_elements(By.CLASS_NAME, "card-text")
        return [element.text.replace("\n", " ") for element in elements]

    def get_all_team_url(self):
        self.driver.get(f"{WEBSITE_URL_1_PREFIX}/stats")
        return [
            i.replace("/players", "")
            for i in [
                i.get_attribute("href")
                for i in self.driver.find_elements(By.TAG_NAME, "a")
                if i is not None
            ]
            if i is not None and "players" in i
        ]

    def get_all_player_team_url(self):
        self.driver.get(f"{WEBSITE_URL_1_PREFIX}/stats")
        return [
            i
            for i in [
                i.get_attribute("href")
                for i in self.driver.find_elements(By.TAG_NAME, "a")
                if i is not None
            ]
            if i is not None and "players" in i
        ]

    def get_players_team_info_and_profile_url(self):
        players_info = []
        urls = self.get_all_player_team_url()
        for url in urls:
            self.driver.get(url)
            try:
                player_profile_urls = [
                    x
                    for x in [
                        i.get_attribute("href")
                        for i in self.driver.find_elements(By.TAG_NAME, "a")
                        if i is not None
                    ]
                    if x is not None and "profile" in x and "/players/" in x
                ]
                player_names = [
                    i.get_attribute("innerText").replace("\n", " ")
                    for i in self.driver.find_elements(By.CLASS_NAME, "squad-name")
                    if i is not None
                ]
                for name, profile_url in zip(player_names, player_profile_urls):
                    players_info.append(
                        {"name": name, "profileURL": profile_url, "teamURL": url}
                    )
            except Exception as e:
                print(f"Error processing URL {url}: {str(e)}")
        return players_info

    def get_stats_from_player_profile(self, profile_url):
        self.driver.get(profile_url)
        sleep(2)
        labels = [
            i.get_attribute("innerText")
            for i in self.driver.find_elements(By.CLASS_NAME, "graph-label")
            if i is not None
        ]
        values = [
            i.get_attribute("innerText")
            for i in self.driver.find_elements(By.CLASS_NAME, "graph-value")
            if i is not None
        ]
        team = (
            self.driver.find_elements(By.CLASS_NAME, "name-section")[0]
            .get_attribute("innerText")
            .replace("\n", " ")
        )
        return {labels[0]: values[0], labels[1]: values[1], "teamName": team}

    def team_season_standings(self, team=None, rank=None):
        """
            Returns the latest season standings.
            Parameters:
            team (str, optional): The name of a specific team to get data for. Case-insensitive.
            rank (int, optional): The rank (1-12) to get the team data for.
            """
        if team is not None and rank is not None:
            return "Please provide either a team name or a rank, but not both. By default, all the teams will be listed."
        self.driver.get("https://www.prokabaddi.com/")
        sleep(2)
        team_name = [i.get_attribute("innerText") for i in self.driver.find_elements(By.CLASS_NAME, "team-name") if
                     i is not None]
        play = [i.get_attribute("innerText") for i in self.driver.find_elements(By.CLASS_NAME, "matches-play") if
                i is not None]
        play = play[::-1][:len(play) - 1][::-1]
        won = [i.get_attribute("innerText") for i in self.driver.find_elements(By.CLASS_NAME, "matches-won") if
               i is not None]
        won = won[::-1][:len(won) - 1][::-1]
        lost = [i.get_attribute("innerText") for i in self.driver.find_elements(By.CLASS_NAME, "matches-lost") if
                i is not None]
        lost = lost[::-1][:len(lost) - 1][::-1]
        draw = [i.get_attribute("innerText") for i in self.driver.find_elements(By.CLASS_NAME, "matches-draw") if
                i is not None]
        draw = draw[::-1][:len(draw) - 1][::-1]
        points = [i.get_attribute("innerText") for i in self.driver.find_elements(By.CLASS_NAME, "points") if i is not None]
        points = points[::-1][:len(points) - 1][::-1]
        team_property_dict = {
            team_name[i].lower(): {
                "TeamName": team_name[i],
                "play": int(play[i]),
                "won": int(won[i]),
                "lost": int(lost[i]),
                "draw": int(draw[i]),
                "points": int(points[i])
            } for i in range(len(team_name))
        }
        if team is None and rank is None:
            return team_property_dict
        if team != None:
            if team.lower() in team_property_dict:
                return team_property_dict.get(team.lower())
            else:
                return "Enter a valid team name!"
        if (rank != None) and (1 <= rank <= 12):
            sorted_teams = sorted(team_property_dict.values(), key=lambda x: x['points'], reverse=True)
            print(f"Rank : {rank}")
            return sorted_teams[int(rank)]
        else:
            return "Enter rank between 1 and 12!"
    def get_all_season_team_stats(self, url):
        self.driver.get(url)
        with open("get_team_performance.js", "r") as f:
            js_code = f.read()
        return self.driver.execute_script(js_code)

    def team_line_up(self):
        return self._tableau_data_extraction(
            "https://public.tableau.com/views/DEMO_PKL_S9/TeamLine-up?%3Adisplay_static_image=y&%3Aembed=true&%3Aembed=y&%3Alanguage=en-US&publish=yes%20&%3AshowVizHome=n&%3AapiID=host0#navType=0&navSrc=Parse",
            5,
        )

    def team_level_stats(self):
        return self._tableau_data_extraction(
            "https://public.tableau.com/views/DEMO_PKL_S9/Teamlevelstats?%3Adisplay_static_image=y&%3Aembed=true&%3Aembed=y&%3Alanguage=en-US&publish=yes%20&%3AshowVizHome=n&%3AapiID=host0#navType=0&navSrc=Parse",
            3,
        )

    def player_performance(self):
        return self._tableau_data_extraction(
            "https://public.tableau.com/views/DEMO_PKL_S9/PlayerPerformance?%3Adisplay_static_image=y&%3Aembed=true&%3Aembed=y&%3Alanguage=en-US&publish=yes%20&%3AshowVizHome=n&%3AapiID=host0#navType=0&navSrc=Parse",
            3,
        )

    def _tableau_data_extraction(self, url, iterations):
        """
        Extract data from the specified Tableau dashboard using Selenium.

        Parameters:
        - url (str): The URL of the Tableau dashboard to be accessed.
        - iterations (int): The number of iterations to perform for data extraction.

        Returns:
        - results (list): A list of data extracted in each iteration.
        """
        self.driver.get(url)
        sleep(10)
        self.driver.find_elements(By.CLASS_NAME, "tabComboBoxNameContainer")[0].click()
        self.driver.find_elements(By.CLASS_NAME, "FICheckRadio")[5].click()

        results = []
        for y in range(1, iterations + 1):
            print(f"Iteration {y} started")
            self.driver.find_elements(By.CLASS_NAME, "FICheckRadio")[y].click()
            sleep(2)
            with open("script.js", "r") as f:
                js_code = f.read()
            data = self.driver.execute_script(js_code)
            results.append(data)
            sleep(7)
            self.driver.save_screenshot(f"screenshot_{y}.png")
            sleep(2)
            try:
                self.driver.execute_script(
                    "document.getElementsByClassName('f1b5ibck')[0].click()"
                )
            except:
                pass
            sleep(2)
            try:
                self.driver.find_elements(By.CLASS_NAME, "tabComboBoxNameContainer")[
                    0
                ].click()
            except:
                pass
            sleep(2)
            try:
                self.driver.find_elements(By.CLASS_NAME, "FICheckRadio")[y].click()
            except:
                pass
            print(f"Iteration {y} completed")

        return results

    def load_data(self, TeamDetails=True, TeamMembers=True, PlayerDetails=True):
        """
    Load specified CSV files into pandas DataFrames based on the provided boolean parameters.

    Parameters:
    - TeamDetails (bool): Loads the 'teamDetails.csv' file. Default is True.
    - TeamMembers (bool): Loads the 'teamMembers.csv' file. Default is True.
    - PlayerDetails (bool): Loads the 'playerDetails.csv' file. Default is True.

    Returns:
    - tuple: A tuple containing the loaded DataFrames in the order (player_details_df, team_details_df, team_members_df).
        """
        default_download_directory = r"C:\Users\KIIT\Downloads"
        if PlayerDetails:
            player_details_df = pd.read_csv(f"{default_download_directory}/playerDetails.csv")
            self.player_details_df = player_details_df
            print("Loaded playerDetails.csv")
        else:
            player_details_df = None

        if TeamDetails:
            team_details_df = pd.read_csv(f"{default_download_directory}/teamDetails.csv")
            self.team_details_df = team_details_df
            print("Loaded teamDetails.csv")
        else:
            team_details_df = None

        if TeamMembers:
            team_members_df = pd.read_csv(f"{default_download_directory}/teamMembers.csv")
            self.team_members_df = team_members_df
            print("Loaded teamMembers.csv")
        else:
            team_members_df = None
        print("loaded all")
        return (player_details_df, team_details_df, team_members_df)

    def get_top_raiders(self, df1, df2, team_name="PatnaPirates", top_n=5):
        """
        Retrieve the top N raiders from a specific team based on their total points.

        Parameters:
        df1 (pd.DataFrame): The first dataframe containing player data.
        df2 (pd.DataFrame): The second dataframe containing additional player data.
        team_name (str, optional): The name of the team to filter by. Defaults to "PatnaPirates".
        top_n (int, optional): The number of top raiders to retrieve. Defaults to 5.

        Returns:
        - Dataframe containing the top N raiders for the specified team.
    """
        
        merged_df = pd.merge(df1, df2, left_on="PlayerName", right_on="PlayerName")
        print("merged")
        print(merged_df.head())
        team_df = merged_df[merged_df['TeamName'] == team_name]
        sorted_df = team_df.sort_values('TotalPoints', ascending=False)
        raiders_df = sorted_df[sorted_df['PlayerProfile'] == 'Raider']
        return raiders_df.head(top_n)


# Usage example
if __name__ == "__main__":
    aggregator = KabaddiDataAggregator()
    team_names = aggregator.get_all_team_names()
    print("Team Names:", team_names)

    standings = aggregator.team_season_standings()
    print("Season Standings:", json.dumps(standings, indent=2))

    # Add more usage examples as needed

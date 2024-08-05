import requests


class GitHubHelper:
    def __init__(self, github_api, access_token):
        """
        Initialize the GitHubHelper class with the GitHub API URL and access token.

        :param github_api: Base URL of the GitHub API (e.g., "https://api.github.com").
        :param access_token: Personal access token for GitHub authentication.
        """
        self.github_api = github_api
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github+json"
        }

    def get_rate_limit(self):
        """
        Get the remaining rate limit for GitHub API requests.

        :return: The remaining rate limit as an integer, or False if an error occurs.
        """
        url = f"{self.github_api}/rate_limit"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            data = response.json()
            remaining = data['rate']['remaining']
            return remaining

        except requests.exceptions.RequestException as e:
            print(f"Error fetching rate limit: {e}")
            return False

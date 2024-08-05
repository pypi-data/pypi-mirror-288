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

    def check_repository(self, owner, repo):
        """
        Check if a GitHub repository exists and handle various error scenarios.

        :param owner: The owner of the repository (username or organization).
        :param repo: The name of the repository.
        :return: A dictionary with 'status' and 'message' keys describing the result.
        """
        url = f"{self.github_api}/repos/{owner}/{repo}"

        try:
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                return {"status": "exists", "message": "Repository exists."}
            elif response.status_code == 404:
                return {"status": "not_found", "message": "Repository not found."}
            elif response.status_code == 403:
                return {"status": "forbidden",
                        "message": "Access forbidden: you may not have the necessary permissions."}
            else:
                return {"status": "error", "message": f"Unexpected error: {response.status_code} - {response.text}"}

        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": f"Request exception: {e}"}
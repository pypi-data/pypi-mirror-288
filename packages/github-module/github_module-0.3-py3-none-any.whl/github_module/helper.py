import requests


class GitHubHelper:
    RATE_LIMIT_THRESHOLD = 10  # Set the threshold for the rate limit

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

        :return: The remaining rate limit as an integer, or -1 if an error occurred.
        """
        url = f"{self.github_api}/rate_limit"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            data = response.json()
            return data['rate']['remaining']

        except requests.exceptions.RequestException:
            return -1

    def check_repository(self, owner, repo):
        """
        Check if a GitHub repository exists and handle various error scenarios.

        :param owner: The owner of the repository (username or organization).
        :param repo: The name of the repository.
        :return: A dictionary with 'status' and 'message' keys describing the result.
        """
        remaining_rate_limit = self.get_rate_limit()

        if remaining_rate_limit == -1:
            return {"status": "error", "message": "Failed to retrieve rate limit."}

        if remaining_rate_limit < self.RATE_LIMIT_THRESHOLD:
            return {"status": "rate_limit_exceeded",
                    "message": f"Rate limit is too low to proceed (remaining: {remaining_rate_limit})."}

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

    def is_repo_read_only(self, owner, repo):
        """
        Check if a GitHub repository is read-only.

        :param owner: The owner of the repository (username or organization).
        :param repo: The name of the repository.
        :return: True if the repository is read-only, False if it is not, or None if there was an error.
        """
        remaining_rate_limit = self.get_rate_limit()

        if remaining_rate_limit == -1:
            return None  # Rate limit check failed

        if remaining_rate_limit < self.RATE_LIMIT_THRESHOLD:
            return None  # Rate limit too low to safely proceed

        url = f"{self.github_api}/repos/{owner}/{repo}"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            repo_data = response.json()
            return not repo_data['permissions']['push']

        except requests.exceptions.RequestException:
            return None  # Error occurred during the request

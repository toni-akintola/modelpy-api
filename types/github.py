class GithubFile:
    def __init__(
        self,
        name: str,
        path: str,
        sha: str,
        size: int,
        url: str,
        html_url: str,
        git_url: str,
        download_url: str,
        type: str,
        links: dict,
    ):
        self.name = name
        self.path = path
        self.sha = sha
        self.size = size
        self.url = url
        self.html_url = html_url
        self.git_url = git_url
        self.download_url = download_url
        self.type = type
        self._links = links


class GithubRepo:
    def __init__(
        self,
        id: int,
        name: str,
        full_name: str,
        description: str,
        html_url: str,
        created_at: str,
        updated_at: str,
        pushed_at: str,
        language: str,
        forks_count: int,
        stargazers_count: int,
        watchers_count: int,
        size: int,
        private: bool,
        owner: dict,
    ):
        self.id = id
        self.name = name
        self.full_name = full_name
        self.description = description
        self.html_url = html_url
        self.created_at = created_at
        self.updated_at = updated_at
        self.pushed_at = pushed_at
        self.language = language
        self.forks_count = forks_count
        self.stargazers_count = stargazers_count
        self.watchers_count = watchers_count
        self.size = size
        self.private = private
        self.owner = owner


class GithubUser:
    def __init__(
        self,
        login: str,
        id: int,
        node_id: str,
        avatar_url: str,
        gravatar_id: str,
        url: str,
        html_url: str,
        followers_url: str,
        following_url: str,
        gists_url: str,
        starred_url: str,
        subscriptions_url: str,
        organizations_url: str,
        repos_url: str,
        events_url: str,
        received_events_url: str,
        type: str,
        site_admin: bool,
        name: str,
        company: str,
        blog: str,
        location: str,
        email: str,
        bio: str,
        twitter_username: str,
        public_repos: int,
        public_gists: int,
        followers: int,
        following: int,
        created_at: str,
        updated_at: str,
    ):
        self.login = login
        self.id = id
        self.node_id = node_id
        self.avatar_url = avatar_url
        self.gravatar_id = gravatar_id
        self.url = url
        self.html_url = html_url
        self.followers_url = followers_url
        self.following_url = following_url
        self.gists_url = gists_url
        self.starred_url = starred_url
        self.subscriptions_url = subscriptions_url
        self.organizations_url = organizations_url
        self.repos_url = repos_url
        self.events_url = events_url
        self.received_events_url = received_events_url
        self.type = type
        self.site_admin = site_admin
        self.name = name
        self.company = company
        self.blog = blog
        self.location = location
        self.email = email
        self.bio = bio
        self.twitter_username = twitter_username
        self.public_repos = public_repos
        self.public_gists = public_gists
        self.followers = followers
        self.following = following
        self.created_at = created_at
        self.updated_at = updated_at

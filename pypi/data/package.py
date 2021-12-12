from typing import Optional


class Package:
    def __init__(
        self,
        package_name: str,
        summary: str,
        description: str,
        home_page: str,
        package_license: str,
        author_name: str,
        maintainers: Optional[list] = None,
    ):
        self.package_name = package_name
        self.id = package_name
        self.summary = summary
        self.description = description
        self.home_page = home_page
        self.license = package_license
        self.author_name = author_name
        self.maintainers = [] if maintainers is None else maintainers

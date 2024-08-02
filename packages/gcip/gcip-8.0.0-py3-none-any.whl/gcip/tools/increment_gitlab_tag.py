import argparse
import os
from typing import Tuple

import gitlab  # type: ignore
import semver  # type: ignore
from gitlab.v4.objects import Project  # type: ignore


# Function to get the latest tag from the repository
def get_latest_tag(project: Project) -> str:
    tags = project.tags.list(order_by="name", sort="desc")
    if tags:
        return str(list(tags)[0].name)
    else:
        return "0.0.0"


# Function to increment the version
def increment_version(version: str, increment_type: str) -> semver.VersionInfo:
    if increment_type == "major":
        return semver.VersionInfo.parse(version).bump_major()
    elif increment_type == "minor":
        return semver.VersionInfo.parse(version).bump_minor()
    elif increment_type == "patch":
        return semver.VersionInfo.parse(version).bump_patch()
    else:
        raise ValueError(
            "Invalid increment type. Choose from 'major', 'minor', 'patch'."
        )


# Function to handle optional 'v' prefix
def handle_version_prefix(version: str) -> Tuple[str, str]:
    prefix = ""
    if version.startswith("v") or version.startswith("V"):
        prefix = version[0]
        version = version[1:]
    return prefix, version


# Main function
def main(
    *,
    gitlab_projects: str,
    private_token_env: str | None,
    job_token_env: str | None,
    increment_type: str,
    gitlab_host: str,
    tag_message: str = "",
) -> None:
    private_token: str | None = None
    job_token: str | None = None
    if private_token_env:
        private_token = os.getenv(private_token_env, "")
    elif job_token_env:
        job_token = os.getenv(job_token_env, "")

    # Create a GitLab instance
    if private_token:
        print("Authenticating with private token.")
        gl = gitlab.Gitlab(gitlab_host, private_token=private_token)
    elif job_token:
        print("Authenticating with job token.")
        gl = gitlab.Gitlab(gitlab_host, job_token=job_token)
    else:
        print("Authenticating with no token token.")
        gl = gitlab.Gitlab(gitlab_host)

    # Split project list into individual projects
    projects = [p.strip() for p in gitlab_projects.split(",")]

    for project in projects:
        # Get the project instance
        project_instance = gl.projects.get(project, lazy=True)

        # Get the latest tag
        latest_tag = get_latest_tag(project_instance)
        print(f"Project: {project}")
        print(f"Latest tag: {latest_tag}")

        # Handle optional 'v' prefix
        latest_tag_prefix, latest_tag_version = handle_version_prefix(latest_tag)

        # Increment the version
        new_version = increment_version(latest_tag_version, increment_type)

        # Combine prefix with new version
        new_tag = f"{latest_tag_prefix}{new_version}"
        print(f"New version: {new_tag}")

        # Create a new tag with optional message
        project_instance.tags.create(
            {
                "tag_name": new_tag,
                "ref": "main",
                "message": tag_message if tag_message else "",
            }
        )
        print("Success.")
        print("-" * 20)

    if tag_message:
        print(f"Tag message: {tag_message}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Increment SemVer tag in GitLab repository."
    )
    parser.add_argument(
        "--gitlab-projects",
        type=str,
        required=True,
        help="Comma-separated list of GitLab project IDs or paths (namespace/project).",
    )
    parser.add_argument(
        "--increment-type",
        type=str,
        required=True,
        choices=["major", "minor", "patch"],
        help="The part of the version to increment.",
    )
    parser.add_argument(
        "--private-token-env",
        type=str,
        help="Environment variable for GitLab private token. If unset or empty, job token  or no token will be used.",
    )
    parser.add_argument(
        "--job-token-env",
        type=str,
        help="Environment variable for GitLab job token. Typically 'CI_JOB_TOKEN'. If unset or empty, private token or no token will be used.",
    )
    parser.add_argument(
        "--gitlab-host",
        type=str,
        default="https://gitlab.com",
        help="The GitLab host URL.",
    )
    parser.add_argument(
        "--tag-message",
        type=str,
        default="",
        help="Optional message to include in the tag.",
    )

    args = parser.parse_args()
    main(
        gitlab_projects=args.gitlab_projects,
        private_token_env=args.private_token_env,
        job_token_env=args.job_token_env,
        increment_type=args.increment_type,
        gitlab_host=args.gitlab_host,
        tag_message=args.tag_message,
    )

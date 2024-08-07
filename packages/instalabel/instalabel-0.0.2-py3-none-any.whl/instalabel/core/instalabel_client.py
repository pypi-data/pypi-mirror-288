import os

import instalabel.client
from instalabel.client.models.task_enum import TaskEnum
from instalabel.client.rest import ApiException
from instalabel.config import INSTALABEL_CLIENT_CONFIGURATION as configuration
from instalabel.core.project import Project


class InstaLabel:
    def __init__(self):
        return

    def login(self, username: str, password: str):
        with instalabel.client.ApiClient(configuration) as api_client:
            api_instance = instalabel.client.AuthApi(api_client)
            try:
                api_response = (
                    api_instance.login_for_access_token_api_v1_auth_token_post(
                        username, password
                    )
                )
                configuration.access_token = api_response.access_token
                os.environ["ACCESS_TOKEN"] = api_response.access_token

            except ApiException as e:
                print(
                    "Exception when calling AuthApi->login_for_access_token_api_v1_auth_token_post: %s\n"
                    % e
                )

    def get_projects(self):
        with instalabel.client.ApiClient(configuration) as api_client:
            api_instance = instalabel.client.ProjectsApi(api_client)
            try:
                api_response = api_instance.read_projects_api_v1_projects_get()

                # Create a dictionary of projects with project_id as key
                projects = {
                    project.project_id: Project(project) for project in api_response
                }

                # Print a summary of projects
                if projects:
                    print("Retrieved projects:")
                    for project_id, project_obj in projects.items():
                        print(
                            f"Project ID: {project_id}, Name: {project_obj.name}, Task: {project_obj.task.value}"
                        )
                else:
                    print("No projects found.")

                return projects
            except Exception as e:
                print(
                    "Exception when calling ProjectsApi->read_projects_api_v1_projects_get: %s\n"
                    % e
                )

    def get_project(self, project_id: str):

        with instalabel.client.ApiClient(configuration) as api_client:

            api_instance = instalabel.client.ProjectsApi(api_client)
            project_id = project_id

            try:
                # Read Project
                api_response = api_instance.read_project_api_v1_projects_project_id_get(
                    project_id
                )

                return Project(api_response)

            except Exception as e:
                print(
                    "Exception when calling ProjectsApi->read_project_api_v1_projects_project_id_get: %s\n"
                    % e
                )

    def create_project(
        self, project_name: str, task: TaskEnum, project_description: str
    ):

        with instalabel.client.ApiClient(configuration) as api_client:
            api_instance = instalabel.client.ProjectsApi(api_client)

            # project_ = instalabel.client.Project
            project_create = instalabel.client.ProjectCreate(
                project_name=project_name,
                task=task,
                project_description=project_description,
            )

            try:
                # Create Project
                api_response = api_instance.create_project_api_v1_projects_post(
                    project_create
                )

                return Project(api_response)

            except Exception as e:
                print(
                    "Exception when calling ProjectsApi->create_project_api_v1_projects_post: %s\n"
                    % e
                )

    def __str__(self):
        return "InstaLabel Client"

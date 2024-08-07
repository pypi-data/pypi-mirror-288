<h1 align="center">
  <br>
  <a href="https://www.instalabel.ai/"><img src="https://cdn.prod.website-files.com/6667ef7ab453d64c4dd92256/6667febf76fce14f04c2bfb4_logo.svg"  alt="InstaLabel Inc." style="width: 100%;"></a>
  <br>
</h1>

# InstaLabel Python SDK

Welcome to the InstaLabel SDK! This SDK provides a convenient way to interact with the InstaLabel API, allowing you to manage projects, upload images, and retrieve information about your data. Below, you'll find detailed instructions on how to set up and use the SDK.

## Table of Contents

1. [Installation](#installation)
2. [Getting Started](#getting-started)
3. [Usage](#usage)
   - [Authentication](#authentication)
   - [Projects](#projects)
     - [Creating a Project](#creating-a-project)
     - [Retrieving Projects](#retrieving-projects)
     - [Updating a Project](#updating-a-project)
   - [Images](#images)
     - [Uploading a Single Image](#uploading-a-single-image)
     - [Uploading Multiple Images](#uploading-multiple-images)
     - [Uploading Images from a Directory](#uploading-images-from-a-directory)
     - [Retrieving Project Images](#retrieving-project-images)
4. [Examples](#examples)
5. [Contributing](#contributing)
6. [License](#license)

## Installation

To install the InstaLabel SDK, simply use pip:

```bash
pip install instalabel
```

## Getting Started

To start using the SDK, you need to import the necessary modules and create an instance of the `InstaLabel` class.

```python
from instalabel import InstaLabel
```

## Usage

### Authentication

Before making any API requests, you need to authenticate yourself. Use the `login` method to obtain an access token.

```python
il = InstaLabel()
il.login(username="your_username", password="your_password")
```

### Projects

#### Creating a Project

To create a new project, use the `create_project` method. You need to provide the project name, task type, and an optional description.

```python
new_project = il.create_project(
    project_name="New Project",
    task="semantic segmentation",  # Replace with your desired task type
    project_description="This is a sample project"
)
print(new_project)
```

#### Retrieving Projects

You can retrieve all projects associated with your account using the `get_projects` method.

```python
projects = il.get_projects()
```

To retrieve a specific project, use the `get_project` method with the project ID.

```python
project = il.get_project(project_id="project_id_here")
print(project)
```

#### Updating a Project

To update the details of an existing project, use the `update_project` method on a `Project` instance.

```python
project.update_project(
    project_name="Updated Project Name",
    project_description="Updated description"
)
```

### Images

#### Uploading a Single Image

To upload a single image to a project, use the `upload_single_image` method.

```python
image = project.upload_single_image(file_path="path_to_image.jpg")
print(image)
```

#### Uploading Multiple Images

You can upload multiple images by providing a list of file paths to the `upload_images` method.

```python
image_paths = ["path_to_image1.jpg", "path_to_image2.jpg"]
project.upload_images(image_paths=image_paths)
```

#### Uploading Images from a Directory

To upload all images from a directory, use the `upload_directory` method. It will automatically find all supported image files.

```python
project.upload_directory(dataset_path="path_to_directory")
```

#### Retrieving Project Images

To retrieve all images associated with a project, use the `get_images` method on a `Project` instance.

```python
images = project.get_images()
for image in images:
    print(image)
```

## Examples

Here are some practical examples of using the SDK for common tasks:

1. **Authenticate and Retrieve All Projects**

   This example demonstrates how to authenticate and list all projects associated with your account.

   ```python
   from instalabel import InstaLabel

   # Initialize InstaLabel client
   il = InstaLabel()

   # Authenticate with your credentials
   il.login(username="your_username", password="your_password")

   # Retrieve and print all projects
   projects = il.get_projects()
   for project_id, project in projects.items():
       print(f"Project ID: {project_id}, Name: {project.name}, Task: {project.task.value}")
   ```

2. **Create a New Project and Upload a Directory of Images**

   This example shows how to create a new project and upload all images from a specified directory.

   ```python
   from instalabel import InstaLabel

   # Initialize InstaLabel client
   il = InstaLabel()

   # Authenticate with your credentials
   il.login(username="your_username", password="your_password")

   # Create a new project
   new_project = il.create_project(
       project_name="Image Classification Project",
       task="object detection",
       project_description="A project for image classification tasks."
   )

   # Upload all images from a directory
   dataset_directory = "path/to/your/image/directory"
   new_project.upload_directory(dataset_path=dataset_directory)

   # Output the uploaded project details
   print(f"Project created: {new_project.name} with ID {new_project.id}")
   ```

3. **Retrieve and Print All Images from a Project**

   This example retrieves all images from a specific project and prints their details.

   ```python
   from instalabel import InstaLabel

   # Initialize InstaLabel client
   il = InstaLabel()

   # Authenticate with your credentials
   il.login(username="your_username", password="your_password")

   # Retrieve a specific project
   project_id = "your_project_id_here"
   project = il.get_project(project_id=project_id)

   # Retrieve and print all images in the project
   images = project.get_images()
   for image in images:
       print(f"Image ID: {image.id}, Filename: {image.filename}, Status: {image.status}")
   ```

---

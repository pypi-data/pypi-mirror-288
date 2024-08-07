import instalabel.client
from instalabel.client.models.image_response import ImageResponse
from instalabel.config import INSTALABEL_CLIENT_CONFIGURATION as configuration


class Image:
    def __init__(self, image: ImageResponse):
        self.id = image.image_id
        self.project_id = image.project_id
        self.user_id = image.user_id
        self.filename = image.filename
        self.status = image.status
        self.annotations_count = image.annotations_count
        self.annotations = image.annotations
        self.created_at = image.created_at
        self.updated_at = image.updated_at
        self.presigned_url = image.presigned_url

    def get_image(self):
        # Enter a context with an instance of the API client
        with instalabel.client.ApiClient(configuration) as api_client:
            # Create an instance of the API class
            api_instance = instalabel.client.ImagesApi(api_client)
            image_id = self.id
            project_id = self.project_id

            try:
                # Get Image
                api_response = api_instance.get_image_api_v1_images_image_id_get(
                    image_id, project_id
                )

                # Update the image object with the response
                self.user_id = api_response.user_id
                self.filename = api_response.filename
                self.status = api_response.status
                self.annotations_count = api_response.annotations_count
                self.annotations = api_response.annotations
                self.created_at = api_response.created_at
                self.updated_at = api_response.updated_at
                self.presigned_url = api_response.presigned_url

            except Exception as e:
                print(
                    "Exception when calling ImagesApi->get_image_api_v1_images_image_id_get: %s\n"
                    % e
                )

    def __str__(self):
        return (
            f"Image(ID: {self.id}, Filename: {self.filename}, Status: {self.status}, "
            f"Annotation Count: {self.annotations_count}, Created At: {self.created_at})"
        )

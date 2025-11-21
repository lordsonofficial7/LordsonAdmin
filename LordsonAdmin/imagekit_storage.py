import os
import base64
from django.core.files.storage import Storage
from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions


class ImageKitStorage(Storage):

    def __init__(self):
        self.imagekit = ImageKit(
            private_key=os.getenv("IMAGEKIT_PRIVATE_KEY"),
            public_key=os.getenv("IMAGEKIT_PUBLIC_KEY"),
            url_endpoint=os.getenv("IMAGEKIT_URL_ENDPOINT")
        )

    def _save(self, name, content):

        # ----------------------------------------------------------
        # 1️⃣ Read file bytes (binary)
        # ----------------------------------------------------------
        file_bytes = content.read()

        # ----------------------------------------------------------
        # 2️⃣ Convert binary → Base64 string (needed for old SDK)
        # ----------------------------------------------------------
        encoded_file = base64.b64encode(file_bytes).decode("utf-8")

        # ----------------------------------------------------------
        # 3️⃣ Create options (must be UploadFileRequestOptions)
        # ----------------------------------------------------------
        options = UploadFileRequestOptions(
            folder="lordson/",
            use_unique_file_name=True,
            is_private_file=False
        )

        # ----------------------------------------------------------
        # 4️⃣ Upload to ImageKit
        # ----------------------------------------------------------
        upload_result = self.imagekit.upload_file(
            file=encoded_file,               # BASE64 STRING → WORKS!
            file_name=name.replace(" ", "_"),  # Clean filename
            options=options,
        )

        # Debug print
        print("\nUpload Raw Response:", upload_result.response_metadata.raw, "\n")

        # ----------------------------------------------------------
        # 5️⃣ Validate URL
        # ----------------------------------------------------------
        raw = upload_result.response_metadata.raw
        uploaded_url = raw.get("url")

        if not uploaded_url:
            raise Exception("ImageKit did not return a public URL")

        return uploaded_url.strip()   # Final URL returned

    def exists(self, name):
        return False

    def url(self, name):
        return name

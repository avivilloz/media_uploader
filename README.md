# Media Uploader

Media Uploader is a Python package that simplifies the process of uploading various types of media to different online platforms.

## Description:

Media Uploader is a versatile Python package designed to streamline the process of uploading media content to various online platforms. This package provides a unified interface for handling different types of media uploads, including videos, images, and audio files, to popular websites and services.

Key features of Media Uploader include:
- Support for Multiple Platforms: Easily upload media to various online services with a consistent interface.
- Easy Authentication: Simplified OAuth 2.0 authentication process with token management for secure and efficient API access.
- Customizable Upload Options: Extensive parameter support for tailoring uploads to specific requirements, including privacy settings, metadata, and scheduling.
- Thumbnail Management: Built-in functionality to set custom thumbnails for uploaded content.
- Enum-Based Categorization: Utilizes enum classes for clear and type-safe specification of categories, privacy settings, and licenses.
- Quota-Aware Design: Implements best practices to minimize API quota usage and optimize upload processes.
- Extensible Architecture: Designed with modularity in mind, allowing for easy addition of new platform integrations and features.

Media Uploader is ideal for developers, content creators, and businesses looking to automate and simplify their media upload workflows across various online platforms. Whether you're building a content management system, a social media tool, or just need a reliable way to programmatically upload media, Media Uploader provides the tools and flexibility to meet your needs.

## How to install:

Run the following command in your python venv:

```sh
pip install git+https://github.com/avivilloz/media_uploader.git@main#egg=media_uploader
```

Or add the following line to your project's `requirement.txt` file:

```
git+https://github.com/avivilloz/media_uploader.git@main#egg=media_uploader
```

And run the following command:

```sh
pip install -r requirements.txt
```

## How to use:

### YoutubeUploader

```python
from media_uploader.youtube import (
    YoutubeUploader,
    YoutubeCategory,
    YoutubePrivacyStatus,
    YoutubeLicense,
)


uploader = YoutubeUploader(client_secrets_file="client_secret.json")
uploader.authenticate()

response = uploader.upload_video(
    file_path="video.mp4",
    title="My Awesome Video",
    description="This is a great video I made",
    category=YoutubeCategory.ENTERTAINMENT,
    privacy_status=YoutubePrivacyStatus.PUBLIC,
    tags=["awesome", "video"],
    default_language="en",
    embeddable=True,
    license=YoutubeLicense.YOUTUBE,
    public_stats_viewable=True,
    made_for_kids=False,
)
```
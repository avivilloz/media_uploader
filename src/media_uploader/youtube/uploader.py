import os
import logging
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from enums import YoutubePrivacyStatus, YoutubeCategory, YoutubeLicense

__all__ = ["YoutubeUploader"]

LOG = logging.getLogger(__name__)


class YoutubeUploader:
    def __init__(
        self,
        client_secrets_file="client_secrets.json",
        token_file_path: str = "youtube_token.json",
        local_server_port: int = 8081,
    ):
        self.client_secrets_file = client_secrets_file
        self.token_file_path = token_file_path
        self.local_server_port = local_server_port
        self.scopes = ["https://www.googleapis.com/auth/youtube.upload"]
        self.youtube = None

    def authenticate(self):
        """
        Authenticate the user and create the YouTube API client.
        This method now implements token saving and reusing.
        """
        creds = None
        if os.path.exists(self.token_file_path):
            LOG.info(f"Loading credentials from {self.token_file_path}")
            creds = Credentials.from_authorized_user_file(
                self.token_file_path, self.scopes
            )

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                LOG.info("Refreshing expired credentials")
                creds.refresh(Request())
            else:
                LOG.info("Authenticating using OAuth flow")
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secrets_file, self.scopes
                )
                creds = flow.run_local_server(port=self.local_server_port)

            LOG.info(f"Saving new credentials to {self.token_file_path}")
            with open(self.token_file_path, "w") as token:
                token.write(creds.to_json())

        LOG.info("Building YouTube service")
        self.youtube = build("youtube", "v3", credentials=creds)

    def upload_video(
        self,
        file_path: str,
        title: str,
        description: str,
        category: YoutubeCategory,
        privacy_status: YoutubePrivacyStatus,
        tags: list = None,
        default_language: str = None,
        embeddable: bool = True,
        license: YoutubeLicense = YoutubeLicense.YOUTUBE,
        public_stats_viewable: bool = True,
        publish_at: str = None,
        recording_date: str = None,
        made_for_kids: bool = False,
    ):
        """
        Upload a video to YouTube.

        Parameters:
        - file_path (str): Path to the video file.
        - title (str): Title of the video (up to 100 characters).
        - description (str): Description of the video (up to 5000 characters).
        - category (YouTubeCategory): YouTube video category.
        - privacy_status (PrivacyStatus): Privacy status of the video.
        - tags (list): List of tags for the video (optional, up to 500 characters total).
        - default_language (str): Default language of the video's title and description (optional).
        - embeddable (bool): Whether the video can be embedded on other sites (default True).
        - license (License): Video license (default License.YOUTUBE).
        - public_stats_viewable (bool): Whether video statistics are publicly viewable (default True).
        - publish_at (str): Scheduled publishing time in ISO 8601 format (optional).
        - recording_date (str): Date when the video was recorded in ISO 8601 format (optional).
        - made_for_kids (bool): Whether the video is made for kids (default False).

        Returns:
        - dict: Response from the YouTube API containing video details.
        """
        LOG.info(f"Starting video upload: {title}")
        body = {
            "snippet": {
                "title": title,
                "description": description,
                "categoryId": category.value,
                "tags": tags or [],
                "defaultLanguage": default_language,
            },
            "status": {
                "privacyStatus": privacy_status.value,
                "embeddable": embeddable,
                "license": license.value,
                "publicStatsViewable": public_stats_viewable,
                "publishAt": publish_at,
                "recordingDate": recording_date,
                "selfDeclaredMadeForKids": made_for_kids,
            },
        }

        media = MediaFileUpload(file_path)
        request = self.youtube.videos().insert(
            part="snippet,status", body=body, media_body=media
        )

        LOG.info(f"Uploading video file: {file_path}")
        response = request.execute()
        LOG.info(f"Video uploaded successfully: {response.get('id')}")
        return response

    def set_thumbnail(self, video_id, thumbnail_path):
        """
        Set a custom thumbnail for a video.

        Parameters:
        - video_id (str): ID of the video to update.
        - thumbnail_path (str): Path to the thumbnail image file.

        Returns:
        - dict: Response from the YouTube API containing thumbnail details.
        """
        LOG.info(f"Setting thumbnail for video ID: {video_id}")
        media = MediaFileUpload(thumbnail_path)
        response = (
            self.youtube.thumbnails().set(videoId=video_id, media_body=media).execute()
        )
        LOG.info(f"Thumbnail set successfully for video ID: {video_id}")
        return response

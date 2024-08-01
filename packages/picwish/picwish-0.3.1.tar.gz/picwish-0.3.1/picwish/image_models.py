from dataclasses import dataclass
from pathlib import Path

from httpx import AsyncClient


@dataclass(frozen=True)
class BaseImage:
    """
    Base class for processed images.
    """
    _http: AsyncClient
    url: str

    async def get_bytes(self) -> bytes:
        """
        Fetches the image bytes from the URL.

        :return: The content of the image in bytes.
        :rtype: bytes
        """
        response = await self._http.get(self.url)
        return response.content

    async def download(self, output: str) -> None:
        """
        Downloads the image and saves it to the specified file path.

        :param output: The file path where the image will be saved.
        :type output: str
        """
        Path(output).write_bytes(await self.get_bytes())


@dataclass(frozen=True)
class EnhancedImage(BaseImage):
    """
    Represents an enhanced image.

    :ivar url: The URL of the enhanced image.
    :type url: str
    :ivar watermark: Indicates whether the image has a watermark.
    :type watermark: bool
    :param face_enhanced: Indicates whether the image has been enhanced for faces.
    :type face_enhanced: bool
    """
    watermark: bool
    face_enhanced: bool


@dataclass(frozen=True)
class BackgroundRemovedImage(BaseImage):
    """
    Represents an enhanced image.

    :ivar url: The URL of the enhanced image.
    :type url: str
    :ivar watermark: Indicates whether the image has a watermark.
    :type watermark: bool
    :param mask: The URL of the mask used for background removal.
    :type mask: str
    """
    watermark: bool
    mask: str

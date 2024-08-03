# -*- coding: utf-8 -*-
from __future__ import annotations

from enum import Enum

from common_image_tools.tool import opencv_built_with_gstreamer
from loguru import logger


class OpencvBackendMode(Enum):
    """Enum class to define the OpenCV backend mode for the video source"""

    # Use gstreamer backend if available, otherwise use the default OpenCV backend
    AUTO = 0

    # The default OpenCV backend is used
    OPENCV_DEFAULT = 1

    # Only for Jetson devices, the gstreamer pipeline uses a plugin for hardware acceleration
    OPENCV_GSTREAMER_JETSON = 2


class VideoSource:
    def __init__(
        self,
        source,
        target_frame_height: int = None,
        target_frame_width: int = None,
        target_fps: int | None = None,
        opencv_backend: OpencvBackendMode = OpencvBackendMode.AUTO,
    ):
        """
        The VideoSource class is used to parse the video source and set the target shape of the video frames.

        The parsed source is used to create the OpenCV VideoCapture object and can be accessed with the parsed_source
        property.

        Args:
            source: The video source, it can be a rtsp link, a video file or a webcam number
            target_frame_height: The target height of the video frames
            target_frame_width: The target width of the video frames
            opencv_backend: The OpenCV backend mode to use, by default it is set to AUTO
        """

        self.unparsed_source = source
        self.target_shape: tuple[int, int] | None = (target_frame_height, target_frame_width)
        self.target_fps = target_fps

        if opencv_backend == OpencvBackendMode.AUTO:
            if opencv_built_with_gstreamer():
                self.opencv_backend = OpencvBackendMode.OPENCV_GSTREAMER_JETSON
            else:
                self.opencv_backend = OpencvBackendMode.OPENCV_DEFAULT
        else:
            self.opencv_backend = opencv_backend

        logger.debug(f"Using {self.opencv_backend} OpenCV backend")

    @property
    def parsed_source(self):
        """
        Parse the video source and return the OpenCV VideoCapture object

        Returns:
            The parsed video source with the target shape and the OpenCV backend mode
        """
        if self.opencv_backend == OpencvBackendMode.OPENCV_GSTREAMER_JETSON:
            if "rtsp" in str(self.unparsed_source):
                parsed_source = f"uridecodebin uri={self.unparsed_source} ! nvvidconv ! "

            elif ".mp4" in str(self.unparsed_source):
                parsed_source = f"filesrc location={self.unparsed_source} ! decodebin ! nvvidconv ! "

            elif str(self.unparsed_source).isdigit():
                logger.warning("The webcam video source is experimental")

                # On linux, the webcam is at /dev/videoX where X is the number of the webcam
                adapted_source = f"/dev/video{self.unparsed_source}"

                raise NotImplementedError

            elif "/dev/video" in str(self.unparsed_source):
                if not all(self.target_shape):
                    raise ValueError("The target shape must be set for the webcam video source")

                if not self.target_fps:
                    raise ValueError("The target fps must be set for the webcam video source")

                return (
                    f"v4l2src device={self.unparsed_source} ! "
                    f"image/jpeg, format=MJPG, width={self.target_shape[1]}, height={self.target_shape[0]}, "
                    f"framerate={self.target_fps}/1 ! nvv4l2decoder mjpeg=1 ! nvvidconv ! video/x-raw,format=BGRx ! "
                    f"appsink drop=1"
                )

            else:
                logger.error("The video source is not supported")
                raise ValueError(f"The video source {self.unparsed_source} is not supported")

            parsed_source += "video/x-raw(memory:NVMM) ! nvvidconv ! video/x-raw,format=BGRx ! "

            if self.target_fps is not None:
                parsed_source += f"videorate ! video/x-raw,framerate={self.target_fps}/1 ! "

            parsed_source += "videoconvert ! video/x-raw, format=BGR"

            if all(self.target_shape):
                parsed_source += f", width={self.target_shape[1]}, height={self.target_shape[0]}"

            parsed_source += " ! appsink drop=1"

            return parsed_source

        elif self.opencv_backend == OpencvBackendMode.OPENCV_DEFAULT:
            if str(self.unparsed_source).isdigit():
                return int(self.unparsed_source)
            else:
                return self.unparsed_source

    def __eq__(self, other):
        return (
            self.unparsed_source == other.unparsed_source
            and self.target_shape == other.target_shape
            and self.target_fps == other.target_fps
        )

    def __ne__(self, other):
        return (
            self.unparsed_source != other.unparsed_source
            or self.target_shape != other.target_shape
            or self.target_fps != other.target_fps
        )

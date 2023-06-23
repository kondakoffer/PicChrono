import os
import shutil
from datetime import datetime
from PIL import Image, UnidentifiedImageError
from PIL.ExifTags import Base
import enum

ALLOWED_EXTENSIONS = (".JPG", ".JPEG", ".PNG", ".GIF", ".BMP")
DEFAULT_SOURCE_DIR = os.curdir
DEFAULT_DESTINATION_DIR = os.curdir
DEFAULT_ERROR_DIR = os.curdir


class ExifDateTags(enum.IntEnum):
    DATE_TIME_TAG_ID = 0x0132  # 306:      Exif tag ID for date and time
    DATE_TIME_ORIGIGNAL_TAG_ID = 0x9003  # 36867:    Exif tag ID for date and time of original image (time when image was taken)
    DATE_TIME_DIGITIZED_TAG_ID = 0x9004  # 36868:    Exif tag ID for date and time of digital image (time when image was stored as digital data)


class Renamer:
    def __init__(self):
        pass

    #
    def rename(
        self,
        source_dir: str | os.PathLike = DEFAULT_SOURCE_DIR,
        destination_dir: str | os.PathLike = DEFAULT_DESTINATION_DIR,
        error_dir: str | os.PathLike = DEFAULT_ERROR_DIR,
    ):
        """
        Renames all files in the directory.
        """
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        if not os.path.exists(error_dir):
            os.makedirs(error_dir)
        for filename in os.listdir(source_dir):
            self.rename_image(
                filepath=os.path.join(source_dir, filename),
                destination_dir=destination_dir,
                error_dir=error_dir,
            )
        return True

    #
    def rename_image(
        self,
        filepath: str | os.PathLike,
        destination_dir: str | os.PathLike = DEFAULT_DESTINATION_DIR,
        error_dir: str | os.PathLike = DEFAULT_ERROR_DIR,
    ) -> os.PathLike:
        """
        Renames one specific image based on the EXIF data.
        """
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        if not os.path.exists(error_dir):
            os.makedirs(error_dir)
        f_path, f_ext = os.path.splitext(filepath)
        f_ext = f_ext.upper()
        try:
            with Image.open(filepath) as img:
                exif_date_times = self._get_exif_datetimes(img)
                if len(exif_date_times) == 0:
                    f_path = os.path.join(error_dir, os.path.basename(filepath))
                    shutil.copy2(filepath, f_path)
                    return f_path
                # date_time[2] is the date time string see return of _get_exif_datetimes
                min_date_time = self._get_minimal_datetime(
                    [date_time[2] for date_time in exif_date_times]
                )
                f_timestamp = min_date_time.strftime("%Y-%m-%d_%H-%M-%S")
                f_name = f_timestamp + f_ext
                f_path = os.path.join(destination_dir, f_name)
                i = 0
                f_appendix = ""
                while os.path.exists(f_path):
                    i += 1
                    f_appendix = f"_{i:03d}"
                    f_name = f_timestamp + f_appendix + f_ext
                    f_path = os.path.join(destination_dir, f_name)
                shutil.copy2(filepath, f_path)
                return f_path
        except UnidentifiedImageError:
            f_path = os.path.join(error_dir, os.path.basename(filepath))
            shutil.copy2(filepath, f_path)
            return f_path

    #
    def _get_exif_datetimes(self, img: Image) -> list[tuple[int, str, str]]:
        exif_data = img.getexif()
        date_times = []
        for tag_id in exif_data:
            if tag_id in list(ExifDateTags):
                tag_name = Base(tag_id).name
                data = exif_data.get(tag_id)
                date_times.append((tag_id, tag_name, data))
        return date_times

    #
    def _get_minimal_datetime(self, date_times: list[str]) -> str:
        """
        Returns the minimal date time from a list of date times.
        """
        minimal_date_time = None
        for date_time in date_times:
            date_time = datetime.strptime(date_time, "%Y:%m:%d %H:%M:%S")
            if minimal_date_time is None:
                minimal_date_time = date_time
            elif minimal_date_time > date_time:
                minimal_date_time = date_time
        return minimal_date_time

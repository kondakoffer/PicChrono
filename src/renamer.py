import os
from datetime import datetime
from PIL import Image
from PIL.ExifTags import Base
import base64
import enum

ALLOWED_EXTENSIONS = ('.JPG', '.JPEG', '.PNG', '.GIF', '.BMP')
DEFAULT_SOURCE_DIR = os.curdir
DEFAULT_DESTINATION_DIR = os.curdir

class ExifDateTags(enum.IntEnum):
    DATE_TIME_TAG_ID = 0x0132               # 306:      Exif tag ID for date and time
    DATE_TIME_ORIGIGNAL_TAG_ID = 0x9003     # 36867:    Exif tag ID for date and time of original image (time when image was taken)
    DATE_TIME_DIGITIZED_TAG_ID = 0x9004     # 36868:    Exif tag ID for date and time of digital image (time when image was stored as digital data)


class Renamer:
    def __init__(self,source_dir=DEFAULT_SOURCE_DIR, destination_dir=DEFAULT_DESTINATION_DIR) -> None:
        self.source_dir = os.path.abspath(source_dir)
        self.destination_dir = os.path.abspath(destination_dir)

    @classmethod
    def comandline_setup(cls):
        """
        Providing a base setup to use the Renamer via the comandline.
        """
        source_dir = input('Input the directory where files have to be renamed:\n')
        source_dir = os.path.abspath(source_dir)
        if os.path.isdir(source_dir):
            print(f'Dir "{source_dir}" exists')

        return cls(source_dir=source_dir)

    #
    def rename(self):
        """
        Renames all files in the directory.
        """
        print('Renaming files')
        for filename in os.listdir(self.source_dir):
            print(f'\nRenaming {filename} ...')
            self.rename_image(os.path.join(self.source_dir, filename))
            # TODO:
            #   - Error handling

    # 
    def rename_image(self, filepath:str):
        """
        Renames one specific image based on the EXIF data.
        """
        try:
            abspath = os.path.abspath(filepath)
        except FileNotFoundError:
            print(f'File {filepath} not found')
            return False    # Specify Error code "FIlE_NOT_FOUND"
        if not os.path.isfile(abspath):
            print(f'The given filename {filepath} is not a file')
            return False    # Specify Error code "NOT_A_FILE"
        if not abspath.endswith(ALLOWED_EXTENSIONS):
            print(f'The given filename {filepath} has an unsupported file extension ({abspath.split(".")[-1]})')
            return False
        with Image.open(abspath) as img:
            exif_date_times = self._get_exif_datetimes(img)
            print(exif_date_times)
            # TODO:
            #     - Select minimal date time, handle case for no dates
            #     - Create new filename, handle case for time stamp already taken
            #     - Rename file
            #
            # Expected handling for no dates:
            #     - Move file to a folder "_sort_manually"

    #
    def _get_exif_datetimes(self, img:Image) -> list[tuple[int, str, str]]:
        exif_data = img.getexif()
        date_times = []
        for tag_id in exif_data:
            if tag_id in list(ExifDateTags):         
                tag_name = Base(tag_id).name
                data = exif_data.get(tag_id)
                date_times.append((tag_id, tag_name, data))
        return date_times


# if __name__ == '__main__':
#     print('Welcome to the Renamer!\n')
#     ren = Renamer.comandline_setup()
#     ren.rename()

if __name__ == '__main__':
    ren = Renamer(source_dir='test_files')
    print(ren.rename())


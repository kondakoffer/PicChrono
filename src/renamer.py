import os
from datetime import datetime
import PIL.Image
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
        self.source_dir = source_dir
        self.destination_dir = destination_dir

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

    def rename(self):
        """
        Renames all files in the directory.
        """
        print('Renaming files')
        for filename in os.listdir(self.source_dir):
            if filename.endswith(ALLOWED_EXTENSIONS):
                print(f'\nRenaming {filename} ...')

                # # Get the metadata change time
                # c_date = os.path.getctime(os.path.join(self.source_dir, filename))
                # print(f"Creation date: {c_date}")
                # print(datetime.utcfromtimestamp(c_date).strftime('%Y-%m-%d %H:%M:%S'))

                # Get the last modification time
                m_date = os.path.getmtime(os.path.join(self.source_dir, filename))
                print(f"Modified date: {m_date}")
                print(datetime.utcfromtimestamp(m_date).strftime('%Y-%m-%d %H:%M:%S'))
            else:
                print(f'\nFile {filename} has an unsupported file extension')

    #
    def _get_exif_datetimes(self, filename:str) -> list[tuple[int, str, str]]:
        f = os.path.abspath(filename)
        img = PIL.Image.open(f)
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
    ren = Renamer()
    print(ren._get_exif_dates("test_files/_DSC2428.JPG"))


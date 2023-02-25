import os
from datetime import datetime
import PIL.Image
from PIL.ExifTags import Base
import base64


ALLOWED_EXTENSIONS = ('.JPG', '.JPEG', '.PNG', '.GIF', '.BMP')
DEFAULT_SOURCE_DIR = os.curdir
DEFAULT_DESTINATION_DIR = os.curdir

DATE_TIME_TAG_ID = 306
DATE_TIME_ORIGIGNAL_TAG_ID = 36867
PREVIEW_DATE_TIME_TAG_ID = 50971


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

    # FIXME
    def _get_exif_data(self, filename:str):
        f = os.path.abspath(filename)
        img = PIL.Image.open(f)
        exif_data = img.getexif()

        for tag_id in exif_data:
            # get the tag name, instead of human unreadable tag id
            if tag_id == 50341:
                print(f"{tag_id}: {type(exif_data.get(tag_id))}")
                continue
            # tag = Base(tag_id).name
            data = exif_data.get(tag_id)
            # decode bytes 
            if isinstance(data, bytes):
                # data = data.partition(b" ")[1]
                # print(data.partition(b" "))
                data = data.decode("mac-roman")
                # data = data.decode('latin-1')
            print(f"{tag_id}: {data}")

    # FIXME
    def get_exif_datetime(self, filename):
        date_time_tag_id = 36867
        f = os.path.abspath(filename)
        img = PIL.Image.open(f)
        exif_data = img.getexif()
        date_time = exif_data.get(DATE_TIME_TAG_ID)
        return date_time

# if __name__ == '__main__':
#     print('Welcome to the Renamer!\n')
#     ren = Renamer.comandline_setup()
#     ren.rename()

if __name__ == '__main__':
    ren = Renamer()
    print(ren._get_exif_data("test_files/_DSC2428.JPG"))


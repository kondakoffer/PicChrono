import os
import shutil
from datetime import datetime
from PIL import Image, UnidentifiedImageError
from PIL.ExifTags import Base
import enum

ALLOWED_EXTENSIONS = ('.JPG', '.JPEG', '.PNG', '.GIF', '.BMP')
DEFAULT_SOURCE_DIR = os.curdir
DEFAULT_DESTINATION_DIR = os.curdir
DEFAULT_ERROR_DIR = os.curdir

class ExifDateTags(enum.IntEnum):
    DATE_TIME_TAG_ID = 0x0132               # 306:      Exif tag ID for date and time
    DATE_TIME_ORIGIGNAL_TAG_ID = 0x9003     # 36867:    Exif tag ID for date and time of original image (time when image was taken)
    DATE_TIME_DIGITIZED_TAG_ID = 0x9004     # 36868:    Exif tag ID for date and time of digital image (time when image was stored as digital data)


class Renamer:
    def __init__(self,source_dir=DEFAULT_SOURCE_DIR, destination_dir=DEFAULT_DESTINATION_DIR, error_dir=DEFAULT_ERROR_DIR) -> None:
        self.source_dir = os.path.abspath(source_dir)
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        self.destination_dir = os.path.abspath(destination_dir)
        if not os.path.exists(error_dir):
            os.makedirs(error_dir)
        self.error_dir = os.path.abspath(error_dir)

    @classmethod
    def comandline_setup(cls):
        """
        Providing a base setup to use the Renamer via the comandline.
        """
        source_dir = input('Input the directory where files have to be renamed:\n')
        source_dir = os.path.abspath(source_dir)
        if os.path.isdir(source_dir):
            print(f'Dir "{source_dir}" exists')

        destination_dir = input('Input the directory where the file should be stored after they are renamed:\n')
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
            print(f'Dir "{destination_dir}" created')
        destination_dir = os.path.abspath(destination_dir)
        return cls(source_dir=source_dir)

    #
    def rename(self):
        """
        Renames all files in the directory.
        """
        print(f'Source directory: {self.source_dir}')
        print(f'Destination directory: {self.destination_dir}')
        print(f'Error directory: {self.error_dir}')

        print('Total number of files: ', len(os.listdir(self.source_dir)))
        for filename in os.listdir(self.source_dir):
            print(f'\nRenaming {filename} ...')
            self.rename_image(os.path.join(self.source_dir, filename))
        print('\n--------------------------')
        print('Number of files in destination directory: ', len(os.listdir(self.destination_dir)))
        print('Number of files in error directory: ', len(os.listdir(self.error_dir)))

    # 
    def rename_image(self, filepath:str):
        """
        Renames one specific image based on the EXIF data.
        """
        f_path, f_ext = os.path.splitext(filepath)
        f_ext = f_ext.upper()
        try:
            with Image.open(filepath) as img:
                exif_date_times = self._get_exif_datetimes(img)
                if len(exif_date_times) == 0:
                    f_path = os.path.join(self.error_dir, os.path.basename(filepath))
                    shutil.copy2(filepath, f_path)
                    return f_path
                # date_time[2] is the date time string see return of _get_exif_datetimes
                min_date_time = self._get_minimal_datetime([date_time[2] for date_time in exif_date_times])
                f_timestamp = min_date_time.strftime("%Y-%m-%d_%H-%M-%S")
                f_name = f_timestamp+f_ext
                f_path = os.path.join(self.destination_dir, f_name)
                i = 1
                f_appendix = ''
                while os.path.exists(f_path):
                    f_appendix = f'_{i:03d}'
                    f_name = f_timestamp+f_appendix+f_ext
                    f_path = os.path.join(self.destination_dir, f_name)
                shutil.copy2(filepath, f_path)
                return f_path
        except UnidentifiedImageError:
            f_path = os.path.join(self.error_dir, os.path.basename(filepath))
            shutil.copy2(filepath, f_path)
            return f_path


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

    #
    def _get_minimal_datetime(self, date_times:list[str]) -> str:
        """
        Returns the minimal date time from a list of date times.
        """
        minimal_date_time = None
        for date_time in date_times:
            date_time = datetime.strptime(date_time, '%Y:%m:%d %H:%M:%S')
            if minimal_date_time is None:
                minimal_date_time = date_time
            elif minimal_date_time > date_time:
                minimal_date_time = date_time
        print(f'Minimal date time: {minimal_date_time}')
        return minimal_date_time
    

if __name__ == '__main__':
    ren = Renamer(source_dir='tests/test_files', destination_dir='tests/test_files_renamed', error_dir='tests/test_files_error')
    ren.rename()

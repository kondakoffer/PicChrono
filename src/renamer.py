import os
from datetime import datetime

ALLOWED_EXTENSIONS = ('.JPG', '.JPEG', '.PNG', '.GIF', '.BMP')
DEFAULT_SOURCE_DIR = os.curdir
DEFAULT_DESTINATION_DIR = os.curdir


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


if __name__ == '__main__':
    print('Welcome to the Renamer!\n')
    ren = Renamer.comandline_setup()
    ren.rename()
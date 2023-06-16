"""Tests for the renamer class."""
import pytest
import warnings

import os
import shutil

from PIL import Image, UnidentifiedImageError

from ImageRename.renamer import *

TEST_SOURCE_DIR = 'tests/test_files'
TEST_DESTINATION_DIR = 'tests/test_files_renamed'
TEST_ERROR_DIR = 'tests/test_files_error'



def setup_module(module):
    """Setup for tests."""
    # Make sure that the test destination and error directories are empty
    shutil.rmtree(TEST_DESTINATION_DIR)
    shutil.rmtree(TEST_ERROR_DIR)

def teardown_module(module):
    """Teardown for tests."""
    print('\nTeardown')

renamer = Renamer(source_dir=TEST_SOURCE_DIR, destination_dir=TEST_DESTINATION_DIR, error_dir=TEST_ERROR_DIR)
class TestGroup_RenamerSetup:
    """Tests for the constructor and classmethods of the Renamer class."""

    @pytest.mark.parametrize(
        'source_dir,destination_dir,error_dir',
        [
            ( # Standard test directories
                TEST_SOURCE_DIR, TEST_DESTINATION_DIR, TEST_ERROR_DIR
            ),
            # TODO: Test for non existing directories
            # TODO: Test for unreadable directories
            # TODO: Test for existing parent directoriy
            # TODO: Test for root directory (no parent directory)
            # TODO: Test for unpermitted directories (e.g. system directories, unwritable directories, forbidden characters in directory name)
            # TODO: Test for alias (~, and other aliases)

        ]
    )
    def test_init(self, source_dir, destination_dir, error_dir):
        """Test for the constructor of the Renamer class."""
        renamer = Renamer(source_dir, destination_dir, error_dir)
        assert renamer.source_dir == os.path.abspath(source_dir)
        assert renamer.destination_dir == os.path.abspath(destination_dir)
        assert renamer.error_dir == os.path.abspath(error_dir)
        assert os.path.exists(renamer.source_dir)
        assert os.path.exists(renamer.destination_dir)
        assert os.path.exists(renamer.error_dir)

class TestGroup_GetMinimalDateTime:
    """Tests for the _get_minimal_datetime function."""

    @pytest.mark.parametrize(
        'date_times,expected_minimal_date_time',
        [
            ( # Test for correct format (ordered)
                [
                    '2019:01:01 00:00:00', 
                    '2019:01:01 00:00:01', 
                    '2019:01:01 00:00:02'
                ], 
                datetime.strptime('2019:01:01 00:00:00', '%Y:%m:%d %H:%M:%S')
            ),
            (   # Test for correct format (unordered)
                [
                    '2019:01:01 00:00:02',
                    '2019:01:01 00:00:01', 
                    '2019:01:01 00:00:00'
                ],
                datetime.strptime('2019:01:01 00:00:00', '%Y:%m:%d %H:%M:%S')                             
            ),
            ( # Test for wrong format
                [
                    '2019:01:01 00:00:0',
                    '2019:01:01 00:00:1',
                    '2019:01:01 00:00:2',
                    '2019:01:01 00:00:0'
                ],
                datetime.strptime('2019:01:01 00:00:00', '%Y:%m:%d %H:%M:%S')
            ),
            ( # Test for empty list
                [], None
            ),
            # (
            #     None, pytest.param(TypeError)
            # ),
        ]
    )

    def test_get_minimal_datetime(self, date_times, expected_minimal_date_time):
        minimal_date_time = renamer._get_minimal_datetime(date_times)
        assert minimal_date_time == expected_minimal_date_time

    def test_none(self):
        with pytest.raises(TypeError):
            date_times = None
            minimal_date_time = renamer._get_minimal_datetime(date_times)

    def test_non_existing_date(self):
        with pytest.raises(ValueError):
            date_times = ['1900:02:29 00:00:01'] # 1900 is not a leap year
            minimal_date_time = renamer._get_minimal_datetime(date_times)


class TestGroup_GetExifDateTime():
    """Tests for _get_exif_datetimes function."""
    
    @pytest.mark.parametrize(
        'test_file_path,expected_date_times', 
        [(
            "tests/test_files/standard.JPG",
            [(306, 'DateTime', '2023:02:08 12:05:33')] 
        )]
    )

    def test_get_exif_datetimes(self, test_file_path, expected_date_times):
        with Image.open(test_file_path) as img:
            # Select a file which has date times for all three EXIF_Tags
            warnings.warn(UserWarning("Use a testfile which has date times for all checked EXIF Tags"))
            date_times = renamer._get_exif_datetimes(img)
            assert date_times == expected_date_times


class TestGroup_RenameImage:
    """Tests for rename_image function"""

    @pytest.mark.parametrize(
        'test_file_path,expected_new_path',
        [
            ( # Test standard file
                'tests/test_files/standard.JPG','2023:02:08 12:05:33'
            )
            # TODO: Test for file with no date time
            # TODO: Test for unsupported file format
            # TODO: Test for non existing file
            # TODO: Test for unreadable directories
            # TODO: Test for file in parent directoriy
            # TODO: Test for root directory (no parent directory)
            # TODO: Test for unreachable path (e.g. too long)
            # TODO: Test for Alias (~, and other aliases)
            # TODO: Test for unpermitted file (e.g. sys file, no read permisssion, in directory name) (move to error directory, or skip?)
            # TODO: Test for file with new name already existing (add number to name)
            # TODO: Test for not an Image (PIL Error)
        ]
    )

    def test_rename_image(self, test_file_path, expected_new_path):
        pass

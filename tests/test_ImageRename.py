"""Tests for the renamer class."""
import pytest
import warnings

import os
from PIL import Image, UnidentifiedImageError

from ImageRename.renamer import *

renamer = Renamer(
    source_dir='test_files', 
    destination_dir='test_files_renamed', 
    error_dir='test_files_error'
    )



class TestGroup_MinimalDateTime:
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

    # def test_no_date_time_found(self):
    #     # There currently is no file without date_times
    #     warnings.warn(UserWarning("Provide a testfile which has no date-times in any checked EXIF Tag"))
    #     return
    #     with Image.open("tests/test_files/no_exif_datetime.JPG") as img:
    #         date_times = renamer._get_exif_datetimes(img)
    #         assert date_times == []

    # def test_file_format_not_supported(self):
    #     warnings.warn(UserWarning("More a test for rename_image function"))
    #     with pytest.raises(UnidentifiedImageError):
    #         with Image.open('tests/test_files/wrong_file_format.TXT') as img:
    #             date_times = renamer._get_exif_datetimes(img)

    # def test_none(self):
    #     pass

class TestGroup_RenameImage:
    """Tests for rename_image function"""

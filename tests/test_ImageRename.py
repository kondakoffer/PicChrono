"""Tests for the renamer class."""
import pytest

import os
from PIL import Image

from ImageRename.renamer import *

renamer = Renamer(
    source_dir='test_files', 
    destination_dir='test_files_renamed', 
    error_dir='test_files_error'
    )



class TestGroup_MinimalDateTime:
    """Tests for the _get_minimal_datetime function."""

    def test_get_minimal_datetime(self):
        date_times = ['2019:01:01 00:00:00', '2019:01:01 00:00:01', '2019:01:01 00:00:02']
        minimal_date_time = renamer._get_minimal_datetime(date_times)
        assert minimal_date_time == datetime.strptime('2019:01:01 00:00:00', '%Y:%m:%d %H:%M:%S')

    def test_wrong_format(self):
        date_times = ['2018:01:01 00:00:0', '2019:01:01 00:00:1', '2019:01:01 00:00:2', '2019:01:01 00:00:0']
        minimal_date_time = renamer._get_minimal_datetime(date_times)
        print(minimal_date_time)
        assert minimal_date_time == datetime.strptime('2018:01:01 00:00:00', '%Y:%m:%d %H:%M:%S')

    def test_empty_list(self):
        date_times = []
        minimal_date_time = renamer._get_minimal_datetime(date_times)
        assert(minimal_date_time is None)

    def test_none(self):
        with pytest.raises(TypeError):
            date_times = None
            minimal_date_time = renamer._get_minimal_datetime(date_times)

    def test_non_existing_date(self):
        with pytest.raises(ValueError):
            date_times = ['1900:02:29 00:00:01'] # 1900 is not a leap year
            minimal_date_time = renamer._get_minimal_datetime(date_times)

class TestGroup_GetExifDateTime:
    """Tests for _get_exif_datetimes function."""

    # @pytest.mark.parametrize(
            # ("standard_img")
            # [
            #     ('test_files/_DSC2428.JPG')
            #     # Date Time: 8. Feb 2023 at 12:05:33
            # ]
    # )

    def test_get_exif_datetimes(self):
        img = Image.open('tests/test_files/_DSC2428.JPG')
        date_times = renamer._get_exif_datetimes(img=img)
        assert date_times == [(306, 'DateTime', '2023:02:08 12:05:33')]

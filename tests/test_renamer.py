"""Tests for the renamer class."""
import pytest
import warnings

import os
import shutil

from PIL import Image, UnidentifiedImageError

from pic_chrono.renamer import *

TEST_SOURCE_DIR = "tests/test_files"
TEST_DESTINATION_DIR = "tests/test_files_renamed"
TEST_ERROR_DIR = "tests/test_files_error"

renamer = Renamer()


def delete_content(folder):
    """Deletes all files in a folder."""
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))


def setup_module(module):
    """Setup for tests."""
    # Make sure that the test destination and error directories are exist and are empty
    if os.path.exists(TEST_DESTINATION_DIR):
        delete_content(TEST_DESTINATION_DIR)
    else:
        os.mkdir(TEST_DESTINATION_DIR)
    if os.path.exists(TEST_ERROR_DIR):
        delete_content(TEST_ERROR_DIR)
    else:
        os.mkdir(TEST_ERROR_DIR)


def teardown_module(module):
    """Teardown for tests."""
    # Make sure that the test destination and error directories are deleted
    shutil.rmtree(TEST_DESTINATION_DIR)
    shutil.rmtree(TEST_ERROR_DIR)


class TestGroup_GetMinimalDateTime:
    """Tests for the _get_minimal_datetime function."""

    @pytest.mark.parametrize(
        "date_times,expected_minimal_date_time",
        [
            (  # Test for correct format (ordered)
                ["2019:01:01 00:00:00", "2019:01:01 00:00:01", "2019:01:01 00:00:02"],
                datetime.strptime("2019:01:01 00:00:00", "%Y:%m:%d %H:%M:%S"),
            ),
            (  # Test for correct format (unordered)
                ["2019:01:01 00:00:02", "2019:01:01 00:00:01", "2019:01:01 00:00:00"],
                datetime.strptime("2019:01:01 00:00:00", "%Y:%m:%d %H:%M:%S"),
            ),
            (  # Test for wrong format
                [
                    "2019:01:01 00:00:0",
                    "2019:01:01 00:00:1",
                    "2019:01:01 00:00:2",
                    "2019:01:01 00:00:0",
                ],
                datetime.strptime("2019:01:01 00:00:00", "%Y:%m:%d %H:%M:%S"),
            ),
            ([], None),  # Test for empty list
            # (
            #     None, pytest.param(TypeError)
            # ),
        ],
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
            date_times = ["1900:02:29 00:00:01"]  # 1900 is not a leap year
            minimal_date_time = renamer._get_minimal_datetime(date_times)


class TestGroup_GetExifDateTime:
    """Tests for _get_exif_datetimes function."""

    @pytest.mark.parametrize(
        "test_file_path,expected_date_times",
        [("tests/test_files/standard.JPG", [(306, "DateTime", "2023:02:08 12:05:33")])],
    )
    def test_get_exif_datetimes(self, test_file_path, expected_date_times):
        with Image.open(test_file_path) as img:
            # Select a file which has date times for all three EXIF_Tags
            warnings.warn(
                UserWarning(
                    "Use a testfile which has date times for all checked EXIF Tags"
                )
            )
            date_times = renamer._get_exif_datetimes(img)
            assert date_times == expected_date_times


class TestGroup_RenameImage:
    """Tests for rename_image function"""

    @classmethod
    def setup_class(cls):
        """Setup for test class"""
        # Make sure that the test destination and error directories are empty
        shutil.rmtree(TEST_DESTINATION_DIR)
        shutil.rmtree(TEST_ERROR_DIR)

    @classmethod
    def teardown_class(cls):
        """Teardown for test class"""
        # Make sure that the test destination and error directories are empty
        if os.path.exists(TEST_DESTINATION_DIR):
            delete_content(TEST_DESTINATION_DIR)
        if os.path.exists(TEST_ERROR_DIR):
            delete_content(TEST_ERROR_DIR)

    @pytest.mark.parametrize(
        "test_file_path,destination_dir,error_dir,expected_new_path",
        [
            (  # Test standard file
                os.path.join("tests", "test_files", "standard.JPG"),
                TEST_DESTINATION_DIR,
                TEST_ERROR_DIR,
                os.path.join(TEST_DESTINATION_DIR, "2023-02-08_12-05-33.JPG"),
            ),
            (  # Test file with new name already existing
                "tests/test_files/standard_copy.JPG",
                TEST_DESTINATION_DIR,
                TEST_ERROR_DIR,
                os.path.join(TEST_DESTINATION_DIR, "2023-02-08_12-05-33_001.JPG"),
            ),
            (  # Test file not an image
                "tests/test_files/not_an_image.TXT",
                TEST_DESTINATION_DIR,
                TEST_ERROR_DIR,
                os.path.join(TEST_ERROR_DIR, "not_an_image.TXT"),
            ),
            (  # Test file with no date time
                "tests/test_files/no_date_time.JPG",
                TEST_DESTINATION_DIR,
                TEST_ERROR_DIR,
                os.path.join(TEST_ERROR_DIR, "no_date_time.JPG"),
            ),
        ],
    )
    def test_rename_image(
        self, test_file_path, destination_dir, error_dir, expected_new_path
    ):
        f_path = renamer.rename_image(
            filepath=test_file_path,
            destination_dir=destination_dir,
            error_dir=error_dir,
        )
        with open(f_path, "rb") as img1:
            with open(test_file_path, "rb") as img2:
                # Check if the images are identical
                assert img1.read() == img2.read()
        assert os.path.abspath(f_path) == os.path.abspath(expected_new_path)
        assert os.path.exists(f_path)
        assert os.path.exists(test_file_path)


class TestGroup_Rename:
    """Tests for rename function."""

    @classmethod
    def setup_class(cls):
        """Setup for test class"""
        # Make sure that the test destination and error directories are empty
        shutil.rmtree(TEST_DESTINATION_DIR)
        shutil.rmtree(TEST_ERROR_DIR)

    @classmethod
    def teardown_class(cls):
        """Teardown for test class"""
        # Make sure that the test destination and error directories are empty
        if os.path.exists(TEST_DESTINATION_DIR):
            delete_content(TEST_DESTINATION_DIR)
        if os.path.exists(TEST_ERROR_DIR):
            delete_content(TEST_ERROR_DIR)

    @pytest.mark.parametrize(
        "source_dir,destination_dir,error_dir",
        [
            (  # Standard test directories
                TEST_SOURCE_DIR,
                TEST_DESTINATION_DIR,
                TEST_ERROR_DIR,
            ),
        ],
    )
    def test_rename(self, source_dir, destination_dir, error_dir):
        assert renamer.rename(
            source_dir=source_dir, destination_dir=destination_dir, error_dir=error_dir, recursive=True
        )
        assert os.path.exists(TEST_DESTINATION_DIR)
        assert os.path.exists(TEST_ERROR_DIR)
        assert len(os.listdir(TEST_SOURCE_DIR)) == len(
            os.listdir(TEST_DESTINATION_DIR)
        ) + len(os.listdir(TEST_ERROR_DIR))

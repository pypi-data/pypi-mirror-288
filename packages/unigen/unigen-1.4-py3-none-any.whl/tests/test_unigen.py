import os
import random
import pytest

from abc import abstractmethod
from typing import Any, Callable, Optional, get_args

# REMOVE
import sys

sys.path.append(os.getcwd())
# REMOVE

from tests.test_utils import (
    copy_base_samples,
    generate_random_japanese_string,
    generate_random_list_containing_random_strings,
    generate_random_number_between_inclusive,
    generate_random_string,
    get_test_file_path,
    getRandomCoverImageData,
    select_random_keys_from_list,
)
from unigen.types.picture import PICTURE_NAME_TO_NUMBER, PICTURE_TYPE, Picture
from unigen.wrapper.audio_manager import IAudioManager


class IUnigenTester:
    single_cover_test = False

    @pytest.fixture(scope="module", autouse=True)
    @classmethod
    def setUpClass(cls):
        # Code to run once before any tests in this class
        print(f"\nTesting {cls.get_extension()}")
        copy_base_samples()

    @pytest.fixture(autouse=True)
    def setUp(self):
        self.audio = self.create_audio_manager()

    @classmethod
    @abstractmethod
    def create_audio_manager(cls) -> IAudioManager:
        """Should return an audiomanager of the type which is being tested. This should be overridden by child classes if required"""

    @classmethod
    @abstractmethod
    def get_extension(cls) -> str:
        """Return the extension of the class to be tested"""

    @classmethod
    def get_filepath(cls) -> str:
        """Return the filepath of the file to be tested"""
        return get_test_file_path(cls.get_extension())

    @classmethod
    def is_single_cover_test(cls) -> bool:
        """
        if extension only supports one artwork, the child class should override this and return True
        this can also be overridden for optimization, this will only test for one cover embed, hence greatly reducing test run time if files are saved beforehand
        """
        return False

    def test_title(self):
        test_arr = ["title1", "title2", "title3", generate_random_string(5, 20), generate_random_japanese_string(8, 32)]
        self._test_equality_list_arg(self.audio.setTitle, self.audio.getTitle, test_arr)

    def test_album(self):
        test_arr = ["album1", "album2", generate_random_string(5, 20), "album4", generate_random_japanese_string(8, 32), generate_random_string(50, 200)]
        self._test_equality_list_arg(self.audio.setAlbum, self.audio.getAlbum, test_arr)

    def test_track_disc_number(self):
        disc, tot_discs, track, tot_tracks = 2, 5, 9, 55
        self.audio.setDiscNumbers(disc, tot_discs)
        self.audio.setTrackNumbers(track, tot_tracks)
        self.assertEqual(disc, self.audio.getDiscNumber())
        self.assertEqual(tot_discs, self.audio.getTotalDiscs())
        self.assertEqual(track, self.audio.getTrackNumber())
        self.assertEqual(tot_tracks, self.audio.getTotalTracks())
        for _ in range(100):
            disc = generate_random_number_between_inclusive(1, 100)
            tot_discs = generate_random_number_between_inclusive(disc + 1, 200)

            track = generate_random_number_between_inclusive(1, 100)
            tot_tracks = generate_random_number_between_inclusive(track + 1, 200)

            self.audio.setDiscNumbers(disc, tot_discs)
            self.audio.setTrackNumbers(track, tot_tracks)
            self.assertEqual(disc, self.audio.getDiscNumber())
            self.assertEqual(tot_discs, self.audio.getTotalDiscs())
            self.assertEqual(track, self.audio.getTrackNumber())
            self.assertEqual(tot_tracks, self.audio.getTotalTracks())

    def test_comment(self):
        test_arr = ["comment1", "find this album at vgmdb.net/damn_son", generate_random_string(5, 20), "album4", generate_random_japanese_string(8, 32), generate_random_string(50, 200)]
        self._test_equality_list_arg(self.audio.setComment, self.audio.getComment, test_arr)

    def test_date(self):
        test_arr = ["2001-7-3", "567-  4 /  14 ", "2023-9 -  4 ", "2023- 9", "1969 ", "  2007/11-6"]
        expected_arr = ["2001-07-03", "0567-04-14", "2023-09-04", "2023-09", "1969", "2007-11-06"]
        for i, x in enumerate(test_arr):
            self.audio.setDate(x)
            self.assertEqual(self.audio.getDate(), expected_arr[i])

    def test_catalog(self):
        test_arr = ["KSLA-0211", "UNCD-0021~0025", generate_random_string(10, 10)]
        self._test_equality_list_arg(self.audio.setCatalog, self.audio.getCatalog, test_arr)

    def test_custom_tags(self):
        key = "MY_TAG"

        def generateValueList():
            return [generate_random_string(5, 35), "My_value", "testing  ...", "damn son ", generate_random_japanese_string(10, 20), generate_random_string(5, 15), "last custom tag"]

        self._test_equality_custom_tag(key, generateValueList())
        self._test_equality_list_arg(self.audio.setCatalog, self.audio.getCatalog, generateValueList())
        self._test_equality_list_arg(self.audio.setDiscName, self.audio.getDiscName, generateValueList())
        self._test_equality_list_arg(self.audio.setBarcode, self.audio.getBarcode, generateValueList())

    def test_all_custom_tags(self):
        NUM_KEYS_TO_TEST = random.randint(5, 20)
        LIST_SIZE_BOUNDS = (random.randint(1, 10), random.randint(10, 20))
        STRING_SIZE_BOUNDS = (random.randint(1, 10), random.randint(10, 20))

        def create_random_list_internal():
            return generate_random_list_containing_random_strings(LIST_SIZE_BOUNDS[0], LIST_SIZE_BOUNDS[1], STRING_SIZE_BOUNDS[0], STRING_SIZE_BOUNDS[1])

        custom_tags_inserted: dict[str, list[str]] = {}
        for _ in range(NUM_KEYS_TO_TEST):
            key = generate_random_string(STRING_SIZE_BOUNDS[0], STRING_SIZE_BOUNDS[1])
            custom_tags_inserted[key] = create_random_list_internal()
            self.audio.setCustomTag(key, custom_tags_inserted[key])
        # the following fields are inserted as custom fields but they are not returned by getAllCustomTags function because they are defined manually
        barcode = create_random_list_internal()
        self.audio.setBarcode(barcode)
        catalog = create_random_list_internal()
        self.audio.setCatalog(catalog)
        custom_tags_received = self.audio.getAllCustomTags()
        custom_tags_received = {key.lower(): value for key, value in custom_tags_received.items()}

        for tag_inserted, value_inserted in custom_tags_inserted.items():
            tag_inserted = tag_inserted.lower()
            self.assertTrue(tag_inserted in custom_tags_received, f"{tag_inserted} was not inserted in the audio file as a custom tag")
            self.assertListEqual(custom_tags_received[tag_inserted], value_inserted, f"custom tag values are not matching:\ninserted: {value_inserted}\nreceived: {custom_tags_received[tag_inserted]}")

            custom_tags_received.pop(tag_inserted.lower())
        self.assertTrue(len(custom_tags_received) == 0, f"extra custom tags which should not have appeared: {custom_tags_received}")

    def test_getting_information(self):
        self.assertIsInstance(self.audio.printInfo(), str)

    def test_setting_deleting_front_cover(self):
        self.audio.setPictureOfType(getRandomCoverImageData(), "Cover (front)")
        self.assertTrue(self.audio.hasPictureOfType("Cover (front)"))

        self.audio.deletePictureOfType("Cover (front)")
        self.assertFalse(self.audio.hasPictureOfType("Cover (front)"))

    def test_setting_multiple_pictures(self):
        """This test is not for m4a files because they don't support multiple pictures"""
        chosen_picture_types: list[PICTURE_TYPE] = list(get_args(PICTURE_TYPE))
        if self.single_cover_test:
            chosen_picture_types = [random.choice(chosen_picture_types)]
        else:
            chosen_picture_types = select_random_keys_from_list(chosen_picture_types)
        for picture_type in chosen_picture_types:
            self.audio.setPictureOfType(getRandomCoverImageData(), picture_type)

        for picture_type in chosen_picture_types:
            self.assertTrue(self.audio.hasPictureOfType(picture_type))

    def test_getting_all_pictures(self):
        """This test is not for m4a files because they don't support multiple pictures"""
        chosen_picture_types: list[PICTURE_TYPE] = list(get_args(PICTURE_TYPE))
        if self.is_single_cover_test():
            chosen_picture_types = ["Cover (front)"]
        else:
            chosen_picture_types = select_random_keys_from_list(chosen_picture_types)
        set_pictures: list[Picture] = []
        for picture_type in chosen_picture_types:
            image_data = getRandomCoverImageData()
            set_pictures.append(Picture(picture_type=PICTURE_NAME_TO_NUMBER[picture_type], data=image_data))
            self.audio.setPictureOfType(image_data, picture_type)

        get_pictures: list[Picture] = self.audio.getAllPictures()
        # for i in range(len(get_pictures)):
        #     save_image(get_pictures[i].data, f"get_picture_{get_pictures[i].picture_type_name}_{self.get_extension()}.jpg")
        #     save_image(set_pictures[i].data, f"set_picture_{set_pictures[i].picture_type_name}_{self.get_extension()}.jpg") # For debugging, remove later
        self.assertListEqual(set_pictures, get_pictures)

    def test_get_metadata(self):
        # add a bunch of tags to the audio file by calling tag specific tests. Hacky way but it gets the job done :)
        self.test_album()
        self.test_title()
        self.test_track_disc_number()
        self.test_comment()
        self.test_date()
        self.test_catalog()
        self.test_setting_multiple_pictures()

        metadata = self.audio.getMetadata()
        self.assertEqual(metadata.file_path, self.get_filepath())
        self.assertEqual(metadata.file_name, os.path.basename(self.get_filepath()))
        self.assertEqual(metadata.extension, "." + self.get_extension())

        tags = metadata.tags
        audio = self.audio

        self.assertListEqual(tags.album, audio.getAlbum())
        self.assertListEqual(tags.title, audio.getTitle())
        self.assertEqual(tags.track_number, audio.getTrackNumber())
        self.assertEqual(tags.total_tracks, audio.getTotalTracks())
        self.assertEqual(tags.disc_number, audio.getDiscNumber())
        self.assertEqual(tags.total_discs, audio.getTotalDiscs())
        self.assertListEqual(tags.comment, audio.getComment())
        self.assertListEqual(tags.catalog, audio.getCatalog())
        self.assertListEqual(tags.pictures, audio.getAllPictures())

    def test_xx_save(self):
        """xx is prepended so that the audio file is saved at the end"""
        self.audio.save()

    def _test_equality_list_arg(self, setter: Callable[[list[Any]], None], getter: Callable[[], list[Any]], setter_arg: list[Any], expected: Optional[list[Any]] = None):
        if not expected:
            expected = setter_arg

        setter([])
        self.assertEqual([], getter())

        setter(setter_arg[0:1])
        self.assertEqual(expected[0:1], getter())

        setter(setter_arg)
        self.assertEqual(expected, getter())

    def _test_equality_custom_tag(self, key: str, val: list[str], expected: Optional[list[str]] = None):
        if not expected:
            expected = val

        self.audio.setCustomTag(key, [])
        self.assertEqual(self.audio.getCustomTag(key), [])

        self.audio.setCustomTag(key, val[0:1])
        self.assertEqual(self.audio.getCustomTag(key), expected[0:1])

        self.audio.setCustomTag(key, val)
        self.assertEqual(self.audio.getCustomTag(key), expected)

    def assertTrue(self, expr, msg=None):
        assert expr is True, msg or f"Expected True but got {expr}"

    def assertFalse(self, expr, msg=None):
        assert expr is False, msg or f"Expected False but got {expr}"

    def assertEqual(self, actual, expected, msg=None):
        assert actual == expected, msg or f"Expected {expected} but got {actual}"

    def assertIsInstance(self, obj, cls, msg=None):
        assert isinstance(obj, cls), msg or f"Expected {obj} to be an instance of {cls}, but got {type(obj)}"

    def assertListEqual(self, list1, list2, msg=None):
        assert list1 == list2, msg or f"Expected lists to be equal: {list1} != {list2}"


if __name__ == "__main__":
    pytest.main()

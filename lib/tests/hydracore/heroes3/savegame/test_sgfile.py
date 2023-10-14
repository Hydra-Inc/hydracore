import os
import pytest
import tempfile

from hydracore.format.heroes3 import Heroes3SaveGameFile


def test_gzip_decode():
    Heroes3SaveGameFile(
        'data/heroes3/savegames/hota_v1.6/game_inferno_xeron_jo.GM1')


def test_gzip_decode_encode():
    sgf = Heroes3SaveGameFile(
        'data/heroes3/savegames/hota_v1.6/game_inferno_xeron_jo.GM1')
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, 'game.gm1')
        sgf.save(path)
        sgf2 = Heroes3SaveGameFile(path)
        assert sgf.binary_data == sgf2.binary_data


def test_non_heroes3_gzip_file():
    with pytest.raises(ValueError):
        Heroes3SaveGameFile('data/heroes3/savegames/misc/test.txt.gz')

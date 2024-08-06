import time
import os, subprocess, io
import pytest
import numpy as np
# import whisper
from scipy.signal import correlate

from audiosample import AudioSample

@pytest.fixture(scope='session')
def data_dir(tmp_path_factory):
    return tmp_path_factory.mktemp('audiosample_data')

@pytest.fixture(scope='session')
def small_mp3_file(data_dir):
    return os.path.abspath(f'{__file__}/../assets/audio_files/test.mp3')

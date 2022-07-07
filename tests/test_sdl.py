import pickle
import pytest
import urllib.request
from src.sdl import SerialDownloader


@pytest.fixture
def serial_list_zf1():
    with open('./assets/serial_list_zf1.pkl', mode='rb') as f:
        return pickle.load(f)


@pytest.fixture
def serial_list_zf2():
    with open('./assets/serial_list_zf2.pkl', mode='rb') as f:
        return pickle.load(f)


@pytest.fixture
def serial_list_zf3():
    with open('./assets/serial_list_zf3.pkl', mode='rb') as f:
        return pickle.load(f)


@pytest.fixture
def url_list():
    with open('./assets/url_list.pkl', mode='rb') as f:
        return pickle.load(f)


def test_get_prefix():
    out = '/tmp/sdl'
    url = 'https://example.com/dir1-100/dir2-200/dir5000/prefix500.pdf'
    sd = SerialDownloader(url=url, out_dir=out, start='001')
    assert sd.prefix == 'prefix'

    url = 'https://example.com/dir1-100/dir2-200/dir5000/500.pdf'
    sd = SerialDownloader(url=url, out_dir=out, start='001')
    assert sd.prefix == ''


def test_get_suffix():
    out = '/tmp/sdl'
    url = 'https://example.com/dir1-100/dir2-200/dir5000/prefix500arg.pdf'
    sd = SerialDownloader(url=url, out_dir=out, start='001')
    assert sd.suffix == 'arg'

    url = 'https://example.com/dir1-100/dir2-200/dir5000/prefix500.pdf'
    sd = SerialDownloader(url=url, out_dir=out, start='001')
    assert sd.suffix == ''


def test_get_start_num():
    out = '/tmp/sdl'
    url = 'https://example.com/dir1-100/dir2-200/dir5000/prefix500suffix.pdf'
    sd = SerialDownloader(url=url, out_dir=out, start='001')
    assert sd.start_num == 1

    sd = SerialDownloader(url=url, out_dir=out, start='005')
    assert sd.start_num == 5

    sd = SerialDownloader(url=url, out_dir=out, start='10')
    assert sd.start_num == 10


def test_get_zero_fill():
    out = '/tmp/sdl'
    url = 'https://example.com/dir1-100/dir2-200/dir5000/prefix500suffix.pdf'
    sd = SerialDownloader(url=url, out_dir=out, start='001')
    assert sd.zerofill == 3

    sd = SerialDownloader(url=url, out_dir=out, start='01')
    assert sd.zerofill == 2

    sd = SerialDownloader(url=url, out_dir=out, start='1')
    assert sd.zerofill == 1


def test_get_end_num():
    out = '/tmp/sdl'
    url = 'https://example.com/dir1-100/dir2-200/dir5000/prefix500suffix.pdf'
    sd = SerialDownloader(url=url, out_dir=out, start='001')
    assert sd.end_num == 500


def test_get_file_idx_from_url():
    out = '/tmp/sdl'
    url = 'https://example.com/dir1-100/dir2-200/dir5000/prefix500suffix.pdf'
    sd = SerialDownloader(url=url, out_dir=out, start='001')
    assert sd._get_file_idx_from_url(url) == 500


def test_get_extension():
    out = '/tmp/sdl'
    url = 'https://example.com/dir1-100/dir2-200/dir5000/prefix500suffix.pdf'
    sd = SerialDownloader(url=url, out_dir=out, start='001')
    assert sd.extension == '.pdf'


def test_get_str_end_num():
    out = '/tmp/sdl'
    url = 'https://example.com/dir1-100/dir2-200/dir5000/prefix500suffix.pdf'
    sd = SerialDownloader(url=url, out_dir=out, start='001')
    assert sd.end_num == 500

    url = 'https://example.com/dir1-100/dir2-200/dir5000/prefix10suffix.pdf'
    sd = SerialDownloader(url=url, out_dir=out, start='001')
    assert sd.end_num == 10

    url = 'https://example.com/dir1-100/dir2-200/dir5000/prefix0suffix.pdf'
    sd = SerialDownloader(url=url, out_dir=out, start='001')
    assert sd.end_num == 0


def test_make_serial_num_list(serial_list_zf1, serial_list_zf2, serial_list_zf3):
    out = '/tmp/sdl'
    url = 'https://example.com/dir1-100/dir2-200/dir5000/prefix500suffix.pdf'
    sd = SerialDownloader(url=url, out_dir=out, start='1')
    assert sd._make_serial_num_list() == serial_list_zf1
    # # to pickle
    # with open('./assets/serial_list_zf1.pkl', mode='wb') as f:
    #     pickle.dump(serial_list_zf1, f)

    url = 'https://example.com/dir1-100/dir2-200/dir5000/prefix500suffix.pdf'
    sd = SerialDownloader(url=url, out_dir=out, start='01')
    assert sd._make_serial_num_list() == serial_list_zf2
    # # to pickle
    # with open('./assets/serial_list_zf2.pkl', mode='wb') as f:
    #     pickle.dump(serial_list_zf2, f)

    url = 'https://example.com/dir1-100/dir2-200/dir5000/prefix500suffix.pdf'
    sd = SerialDownloader(url=url, out_dir=out, start='001')
    assert sd._make_serial_num_list() == serial_list_zf3
    # # to pickle
    # with open('./assets/serial_list_zf3.pkl', mode='wb') as f:
    #     pickle.dump(serial_list_zf3, f)


def test__make_url(url_list):
    out = '/tmp/sdl'
    url = 'https://example.com/dir1-100/dir2-200/dir5000/prefix500suffix.pdf'
    sd = SerialDownloader(url=url, out_dir=out, start='001')
    serial_list = sd._make_serial_num_list()
    assert sd._make_url(serial_list) == url_list
    # # to pickle
    # url_list = sd._make_url(serial_list)
    # with open('./assets/url_list.pkl', mode='wb') as f:
    #     pickle.dump(url_list, f)

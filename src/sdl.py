import os
import re
import time
import pathlib
import argparse
import urllib.request
import urllib.error
from typing import List


class SerialDownloader:
    def __init__(self, url: str, out_dir: str, start: str):
        p = pathlib.Path(url)
        self.target_dir = '/'.join(url.split('/')[:-1])
        self.start_num = self._get_start_num(start)
        self.end_num = self._get_end_num(p.name)
        self.prefix = self._get_prefix(p.name)
        self.suffix = self._get_suffix(p.name)
        self.extension = p.suffix
        self.zerofill = self._get_zero_fill(start)
        self.out_dir = out_dir
        self.max_retry = 3

    def _get_zero_fill(self, start: str) -> int:
        result = sum(c.isdigit() for c in str(start))
        return result

    def _get_start_num(self, start: str) -> int:
        result = int(start)
        return result

    def _get_end_num(self, filename: str) -> int:
        pattern = r'\d+'
        try:
            match = re.search(pattern, filename)
            result = int(match.group(0))
            return result
        except Exception:
            print('Not found numbered file in url')
            raise

    def _get_prefix(self, filename: str) -> str:
        pattern = r'([a-zA-Z]+)\d+'
        match = re.search(pattern, filename)
        if match is None:
            return ''
        else:
            result = str(match.group(1))
            return result

    def _get_suffix(self, filename: str) -> str:
        pattern = r'\d+([a-zA-Z]+).'
        match = re.search(pattern, filename)
        if match is None:
            return ''
        else:
            result = str(match.group(1))
            return result

    def _make_serial_num_list(self) -> List[str]:
        start = self.start_num
        end = self.end_num
        zerofill = self.zerofill
        result = [str(i).zfill(zerofill) for i in range(start, end + 1)]
        return result

    def _make_url(self, serial_num_list: List[str]) -> List[str]:
        target_dir = self.target_dir
        prefix = self.prefix
        suffix = self.suffix
        ext = self.extension
        result = []
        for n in serial_num_list:
            result.append(f'{target_dir}/{prefix}{n}{suffix}{ext}')
        return result

    def download(self, url_list: List[str]) -> None:
        out = self.out_dir
        ext = self.extension
        zerofill = self.zerofill
        os.makedirs(out, exist_ok=True)
        opener = urllib.request.build_opener()
        opener.addheaders = [(
            'User-Agent',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/36.0.1941.0 Safari/537.36'
        )]
        urllib.request.install_opener(opener)
        for i, url in enumerate(url_list):
            retry = 0
            while True:
                time.sleep(0.5)
                print(f'Progress ... {i + 1}/{len(url_list)}')
                dest = f'{out}/{str(i + 1).zfill(zerofill)}{ext}'
                try:
                    urllib.request.urlretrieve(url, dest)
                except urllib.error.HTTPError as e:
                    retry += 1
                    print(f'Download error: <{e}>')
                    print(f'Retry: {retry}/{self.max_retry}')
                    if retry > 2:
                        print('The number of retries has reached the maximum')
                        break
                else:
                    break

    def main(self):
        try:
            snl = self._make_serial_num_list()
            url_list = self._make_url(snl)
            self.download(url_list)
            print('Finish')

        except Exception as e:
            print(f'Something went wrong: <{e}>')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download the file saved with the serial number at once')
    parser.add_argument('-u', '--url', required=True, help='Enter the URL of the last file of the serial numbered file')
    parser.add_argument('-s', '--start_num', required=True, type=str, default=1,
                        help='First file number of serial number file / example: -s001 or -s01')
    parser.add_argument('-o', '--output', required=True, type=str, help='Output destination directory')

    args = parser.parse_args()
    # print(f'url = {args.url}')
    # print(f'start_num = {args.start_num}')
    # print(f'output = {args.output}')

    url = args.url
    st = args.start_num
    out = args.output
    sd = SerialDownloader(url=url, out_dir=out, start=st)
    sd.main()

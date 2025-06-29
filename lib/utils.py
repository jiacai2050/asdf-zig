#!/usr/bin/env python3
# coding: utf-8

import os
import platform
import sys
import urllib.request
import json
import hashlib

INDEX_URL = os.getenv('ASDF_ZIG_INDEX_URL', 'https://ziglang.org/download/index.json')
HTTP_TIMEOUT = int(os.getenv('ASDF_ZIG_HTTP_TIMEOUT', '30'))

OS_MAPPING = {
    'darwin': 'macos',
}
ARCH_MAPPING = {
            'i386': 'x86',
            'i686': 'x86',
            'amd64': 'x86_64',
            'arm64':'aarch64',
}

def fetch_index():
    with urllib.request.urlopen(INDEX_URL, timeout=HTTP_TIMEOUT) as response:
        if response.getcode() == 200:
            body = response.read().decode('utf-8')
            return json.loads(body)
        else:
            raise Exception(f"Fetch index.json error: {response.getcode()}")


def all_versions():
    index = fetch_index()
    versions = [k for k in index.keys() if k != 'master']
    versions.sort(key=lambda v: tuple(map(int, v.split('.'))))
    return versions


def download_tarball(url, out_file, expected_shasum):
    chunk_size = 8192  # 8KB chunks
    sha256_hash = hashlib.sha256()
    with urllib.request.urlopen(url, timeout=HTTP_TIMEOUT) as response:
        if response.getcode() != 200:
            raise Exception(f"Fetch index.json error: {response.getcode()}")

        with open(out_file, 'wb') as f:
           while True:
               chunk = response.read(chunk_size)
               if not chunk:
                   break # eof
               sha256_hash.update(chunk)
               f.write(chunk)

    actual = sha256_hash.hexdigest()
    if actual != expected_shasum:
        raise Exception(f"Shasum not match, expected:{expected_shasum}, actual:{actual}")

def download(version, out_file):
    index = fetch_index()
    if version in index is False:
        raise Exception(f'There is no such version: {version}')

    links = index[version]
    os_name = platform.system().lower()
    arch = platform.machine().lower()
    os_name = OS_MAPPING.get(os_name, os_name)
    arch = ARCH_MAPPING.get(arch, arch)
    link_key = f'{arch}_{os_name}'
    if link_key in links is False:
        raise Exception(f'No tarball link for {link_key}')

    tarball_url = link_key[link_key]['tarball']
    tarball_shasum = link_key[link_key]['shasum']
    download_tarball(url ,out_file, tarball_shasum)

def main(args):
    command = args[0] if args else 'default'
    if command == 'all-versions':
        versions = all_versions()
        print(" ".join(versions))
    elif command == 'latest-version':
        versions = all_versions()
        print(versions[-1])
    elif command == 'download':
        download(args[1], args[2])
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])

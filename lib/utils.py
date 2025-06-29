#!/usr/bin/env python3
# coding: utf-8

import os
import random
import platform
import sys
import urllib.request
from urllib.parse import urljoin
import json
import hashlib
import logging

INDEX_URL = os.getenv("ASDF_ZIG_INDEX_URL", "https://ziglang.org/download/index.json")
HTTP_TIMEOUT = int(os.getenv("ASDF_ZIG_HTTP_TIMEOUT", "30"))

# https://github.com/mlugg/setup-zig/blob/main/mirrors.json
# If any of these mirrors are down, please open an issue!
MIRRORS = [
    "https://pkg.machengine.org/zig",
    "https://zigmirror.hryx.net/zig",
    "https://zig.linus.dev/zig",
    "https://fs.liujiacai.net/zigbuilds",
]
OS_MAPPING = {
    "darwin": "macos",
}
ARCH_MAPPING = {
    "i386": "x86",
    "i686": "x86",
    "amd64": "x86_64",
    "arm64": "aarch64",
}


def fetch_index():
    with urllib.request.urlopen(INDEX_URL, timeout=HTTP_TIMEOUT) as response:
        if response.getcode() == 200:
            body = response.read().decode("utf-8")
            return json.loads(body)
        else:
            raise Exception(f"Fetch index.json error: {response.getcode()}")


def all_versions(index=fetch_index()):
    versions = [k for k in index.keys() if k != "master"]
    versions.sort(key=lambda v: tuple(map(int, v.split("."))))
    return versions


def download_and_check(url, out_file, expected_shasum, total_size):
    logging.info(f"Begin download tarball({total_size}) from {url} to {out_file}...")
    chunk_size = 1024 * 1024 # 1M chunks
    sha256_hash = hashlib.sha256()
    with urllib.request.urlopen(url, timeout=HTTP_TIMEOUT) as response:
        if response.getcode() != 200:
            raise Exception(f"Fetch index.json error: {response.getcode()}")

        read_size = 0
        with open(out_file, "wb") as f:
            while True:
                chunk = response.read(chunk_size)
                read_size += len(chunk)
                progress_percentage = (read_size / total_size) * 100 if total_size > 0 else 0
                logging.info(f'Downloaded: {read_size}/{total_size} bytes ({progress_percentage:.2f}%)')
                if not chunk:
                    break  # eof
                sha256_hash.update(chunk)
                f.write(chunk)

    actual = sha256_hash.hexdigest()
    if actual != expected_shasum:
        raise Exception(
            f"Shasum not match, expected:{expected_shasum}, actual:{actual}"
        )


def download_tarball(url, out_file, expected_shasum, total_size):
    filename = url.split("/")[-1]
    random.shuffle(MIRRORS)

    for mirror in MIRRORS:
        try:
            # Ensure base_url has a trailing slash
            mirror = mirror if mirror.endswith('/') else mirror + '/'
            download_and_check(urljoin(mirror, filename), out_file, expected_shasum, total_size)
            return
        except Exception as e:
            logging.error(f"Current mirror failed, try next. err:{e}")

    # All mirrors failed, fallback to original url
    download_and_check(url, out_file, expected_shasum, total_size)


def download(version, out_file):
    index = fetch_index()
    if version not in index:
        raise Exception(f"There is no such version: {version}")

    links = index[version]
    os_name = platform.system().lower()
    arch = platform.machine().lower()
    os_name = OS_MAPPING.get(os_name, os_name)
    arch = ARCH_MAPPING.get(arch, arch)
    link_key = f"{arch}-{os_name}"
    if link_key not in links:
        raise Exception(f"No tarball link for {link_key} in {version}")

    tarball_url = links[link_key]["tarball"]
    tarball_shasum = links[link_key]["shasum"]
    tarball_size = int(links[link_key]["size"])
    download_tarball(tarball_url, out_file, tarball_shasum, tarball_size)


def main(args):
    command = args[0] if args else "default"
    if command == "all-versions":
        versions = all_versions()
        print(" ".join(versions))
    elif command == "latest-version":
        versions = all_versions()
        print(versions[-1])
    elif command == "download":
        download(args[1], args[2])
    else:
        logging.error(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')
    main(sys.argv[1:])

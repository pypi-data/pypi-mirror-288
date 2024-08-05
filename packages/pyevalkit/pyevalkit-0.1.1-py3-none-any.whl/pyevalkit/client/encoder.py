#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2024/7/30 15:29
import mimetypes
import os


def encode_file(filepath):
    filename = os.path.basename(filepath)
    mimetype, _ = mimetypes.guess_type(filename)
    if mimetype is None:
        mimetype = "application/octet-stream"
    filedata = (filename, open(filepath, "rb"), mimetype)
    return filedata


def encode_files(files):
    if files is None:
        return None

    items = []
    for item in files:
        if isinstance(item, list):
            try:
                file_name = item[0]
                file_path = item[1]
                file_tuple = encode_file(file_path)
            except FileNotFoundError as e:
                raise e
            except Exception as e:
                raise e
            items.append((file_name, file_tuple))
    return items

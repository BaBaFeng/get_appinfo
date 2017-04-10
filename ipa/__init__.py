#!/usr/bin/env python
# -*- coding: utf8 -*-

# author: xiaofengfeng
# create: 2017-03-16 10:41:28

import os
import re

import hashlib
import zipfile
import plistlib


class iOSAppInfo():
    '''
    获取的ipa基本信息
    '''

    def __init__(self, ipa):
        self.ipa = ipa

        plist_root = self.analyze_ipa_with_plistlib()
        self.get_app_name = plist_root["CFBundleName"]
        # if self.get_app_name == "drawable":
        self.get_app_name = plist_root["CFBundleDisplayName"]
        self.get_app_pack = plist_root["CFBundleIdentifier"]
        self.get_app_version_name = plist_root["CFBundleShortVersionString"]
        self.get_app_md5 = self.ipa_md5()
        self.get_app_sha1 = self.ipa_sha1()
        self.get_app_size = self.ipa_size()

    def analyze_ipa_with_plistlib(self):
        ipa_file = zipfile.ZipFile(self.ipa)
        plist_path = self.find_plist_path(ipa_file)
        plist_data = ipa_file.read(plist_path)
        plist_root = plistlib.loads(plist_data)

        return plist_root

    def ipa_size(self):
        file_size = os.path.getsize(self.ipa)
        return file_size

    def ipa_md5(self):
        md5 = hashlib.md5()
        _File = open(self.ipa, "rb")
        md5.update(_File.read())
        _File.close()
        appmd5 = md5.hexdigest()
        if appmd5:
            return appmd5
        else:
            return "E: GET IPA MD5 ERROR..."

    def ipa_sha1(self):
        sha1 = hashlib.sha1()
        _File = open(self.ipa, "rb")
        sha1.update(_File.read())
        _File.close()
        AppSHA1 = sha1.hexdigest()
        if AppSHA1:
            return AppSHA1
        else:
            return "E: GET IPA AppSHA1 ERROR..."

    def find_plist_path(self, zip_file):
        name_list = zip_file.namelist()
        pattern = re.compile(r'Payload/[^/]*.app/Info.plist')
        for path in name_list:
            m = pattern.match(path)
            if m is not None:
                return m.group()


def get_app_name(ipa):
    i = iOSAppInfo(ipa)
    return i.get_app_name


def get_app_pack(ipa):
    i = iOSAppInfo(ipa)
    return i.get_app_pack


def get_app_version_name(ipa):
    i = iOSAppInfo(ipa)
    return i.get_app_version_name


def get_app_md5(ipa):
    i = iOSAppInfo(ipa)
    return i.get_app_md5


def get_app_sha1(ipa):
    i = iOSAppInfo(ipa)
    return i.get_app_sha1


def get_app_size(ipa):
    i = iOSAppInfo(ipa)
    return i.get_app_size

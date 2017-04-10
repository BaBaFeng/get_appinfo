# -*- coding: utf8 -*-

import sys

from apk.info import AppInfo
from ipa import get_app_name
from ipa import get_app_pack
from ipa import get_app_version_name
from ipa import get_app_md5
from ipa import get_app_sha1
from ipa import get_app_size


def main(arg):
    if arg[-3:] == "apk":
        a = AppInfo(arg)

        print("AppName:", a.AppName())
        print("AppVersionName:", a.AppVersionName())
        print("AppVersionCode:", a.AppVersionCode())
        print("SdkVersion:", a.SdkVersion())
        print("AppPackName:", a.AppPackName())
        print("AppHomeActivity:", a.AppHomeActivity())
        print("AppMD5:", a.AppMD5())
        print("AppSHA1:", a.AppSHA1())
        print("AppSHA256:", a.AppSHA256())
        print("AppCer:", a.AppCer())

    if arg[-3:] == "ipa":
        print("app_name:", get_app_name(arg))
        print("app_pack:", get_app_pack(arg))
        print("app_version_name:", get_app_version_name(arg))
        print("app_md5:", get_app_md5(arg))
        print("app_sha1:", get_app_sha1(arg))
        print("app_size:", get_app_size(arg))


if __name__ == '__main__':
    try:
        arg = sys.argv[1]
        main(arg)
    except Exception as e:
        print("E: Input a File path.")

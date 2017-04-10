# -*- coding: utf8 -*-

import re
import os
import shutil
import hashlib
import subprocess

from zipfile import ZipFile
from os.path import split
from os.path import abspath


class AppInfo():
    def __init__(self, apkpath):
        self.apkpath = apkpath
        infos = subprocess.Popen(["aapt", "dump", "badging", apkpath], stdout=subprocess.PIPE).stdout.read()
        self.infos = infos.decode("utf-8")
        # print(self.infos)

        self.apk_per = split(apkpath)[0]

    def AppName(self):
        app_name = ""
        appname = re.search("application: label='.*?'", self.infos)
        if appname:
            app_name = appname.group(0).split("=")[-1][1:-1]
        else:
            appname = re.search("application-label.*?'.*?'", self.infos)
            if appname:
                app_name = appname.group(1).split(":")[-1][1:-1]
            else:
                app_name = "E: GET APP NAME ERROR..."

        if app_name == "":
            rex = re.compile("label='.*?'")
            match = rex.findall(self.infos)
            for m in match:
                if m == "label=''":
                    continue
                app_name = m[7:-1]

        if app_name == "":
            rex = re.compile("label='.*?'")
            match = rex.findall(self.infos)
            for m in match:
                if m == "label=''":
                    continue
                app_name = m[7:-1]

        return app_name

    def AppPackName(self):
        apppackname = re.search("package: name='.*?'", self.infos)
        if apppackname:
            return apppackname.group(0)[15:-1]
        else:
            return "E: GET APP PACKAGE NAME ERROR..."

    def AppHomeActivity(self):
        apphomeactivity = re.search(
            "launchable-activity: name='.*?'", self.infos)
        if apphomeactivity:
            return apphomeactivity.group(0)[27:-1]
        else:
            return "E: GET APP HOME ACTIVITY ERROR..."

    def AppVersionName(self):
        appversion = re.search("versionName='.*?'", self.infos)
        if appversion:
            return appversion.group(0)[13:-1]
        else:
            return "E: GET APP VERSION NAME ERROR..."

    def AppVersionCode(self):
        appversioncode = re.search("versionCode='.*?'", self.infos)
        if appversioncode:
            return appversioncode.group(0)[13:-1]
        else:
            return "E: GET APP VERSION CODE ERROR..."

    def AppSHA1(self):
        sha1 = hashlib.sha1()
        _File = open(self.apkpath, "rb")
        sha1.update(_File.read())
        _File.close()
        AppSHA1 = sha1.hexdigest()
        if AppSHA1:
            return AppSHA1
        else:
            return "E: GET APK AppSHA1 ERROR..."

    def AppCer(self):
        try:
            zipx = abspath(self.apkpath)
            z = ZipFile(zipx, "r")
            for item in z.infolist():
                if ".RSA" == item.filename[-4:]:
                    z.extract(item.filename, self.apk_per)
            z.close()

            rsa_path = os.path.join(self.apk_per, "META-INF")

            keytools = "%s -printcert -file %s/*.RSA" % ("keytool", rsa_path)
            cer = os.popen(keytools).read()
            shutil.rmtree(rsa_path)

            if cer:
                return cer
            else:
                return "E: GET APK CERT ERROR..."
        except Exception as e:
            return "META-INF not exists."

    def AppMD5(self):
        md5 = hashlib.md5()
        _File = open(self.apkpath, "rb")
        md5.update(_File.read())
        _File.close()
        appmd5 = md5.hexdigest()
        if appmd5:
            return appmd5
        else:
            return "E: GET APK MD5 ERROR..."

    def AppSHA256(self):
        sha256 = hashlib.sha256()
        _File = open(self.apkpath, "rb")
        sha256.update(_File.read())
        _File.close()
        AppSHA256 = sha256.hexdigest()
        if AppSHA256:
            return AppSHA256
        else:
            return "E: GET APK AppSHA256 ERROR..."

    def SdkVersion(self):
        SdkVersion = re.search("sdkVersion:'.*?'", self.infos)
        if SdkVersion:
            return SdkVersion.group(0)[12:-1]
        else:
            return "E: GET APP SDKVERSION ERROR..."

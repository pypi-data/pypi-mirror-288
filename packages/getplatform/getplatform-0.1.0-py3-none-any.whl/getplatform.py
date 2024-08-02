import os
import platform


def get_platform():
    # Check if system is not 'Linux'
    if platform.system() != "Linux":
        return platform.system()

    # Check for android files
    android_files = [
        "/system/build.prop",
        "/system/app/Superuser.apk",
        "/system/bin/su",
    ]

    if any(os.path.exists(file) for file in android_files):
        return "Android"

    return platform.system()


print(get_platform())

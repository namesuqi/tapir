# coding=utf-8
# author: zengyuetian
# android test related constant

from lib.common.debug import *
from lib.mobile.const import *
from lib.common.path import *

# ----------------------------------------
# device related const
# ----------------------------------------
# Huawei G9
ANDROID_DEVICE = "3DN7N16C06002932"
ANDROID_PLATFORM = "Android"
ANDROID_VERSION = "6.0"

# ----------------------------------------
# Application related const
# ----------------------------------------
APK_PATH = MISC_PATH + "/sdk/apk"
DEMO_APK = APK_PATH + "/aplayer-3.11.10Release.apk"
DEMO_PACKAGE_NAME = "com.cloutropy.bplayer"
DEMO_ACTIVITY_NAME = "MainActivity"


# ----------------------------------------
# SDK related const
# ----------------------------------------
YUNSHANG_CONF = "/sdcard/yunshang/yunshang.conf"
SDK_PORT = 32717
SDK_VERION = "3.11.10"
PEER_ID_LENGTH = 32

# ----------------------------------------
# Test PC related const
# ----------------------------------------
ANDROID_HOST = "192.168.124.36"



# ----------------------------------------
# Live Channel for Testing
# ----------------------------------------
CHANNEL1 = "live_flv/user/yunduan?url=http://rtmpp2p.meixiu98.com/live/livestream.flv"


"""
# coding=utf-8
# author: zengyuetian

from lib.utility.path import *
root_path = PathController.get_root_path()

REMOTE_URL4723 = "http://localhost:4723/wd/hub"
REMOTE_URL4725 = "http://localhost:4725/wd/hub"

ANDROID_PLATFORM = "Android"
ANDROID_VERSION = "4.4"



NO_RESET = "--no-reset"

## follow display different android devices
#ANDROID_DEVICE = "Android Emulator"
#ANDROID_DEVICE = "Coolpad5951-2b889fe7"  # Coolpad YS-B-SJ-0003
# ANDROID_DEVICE = "68a0f62cd2a7"          # Honor YS-B-SJ-0002
# ANDROID_DEVICE = "79c9ce5d"              # Samsung
ANDROID_DEVICE = "3DN7N16C06002932"      # zyt's huawei g9
#ANDROID_DEVICE = "6NJUMLZL0J"            # Kaiboer H19
# ANDROID_DEVICE = "K7D6Y5LBT8DUS4EE"       # Lenovo YS-B-SJ-0004
# ANDROID_DEVICE = "81MEBMP2DRFE"          # melan note2

## follow display app name and package name
CHROME_APP = root_path + "/misc/bin/apk/com.android.chrome.apk"       # android chrome browser apk
CHROME_PACKAGE_NAME = "com.android.chrome"                    # android chrome browser apk package name
CHROME_ACTIVITY_NAME = "com.google.android.apps.chrome.Main"  # android chrome browser apk activity name
DEMO_APP = root_path + "/misc/bin/apk/aplayer-3.11.10Release.apk"                # android sdk demo apk
DEMO_PACKAGE_NAME = "com.cloutropy.bplayer"                   # android sdk demo apk package name
DEMO_ACTIVITY_NAME = "MainActivity"                         # android sdk demo apk activity name

EXPECTED_PEER_ID_LENGTH = "32" # sdk peer id length

## follow display different apk peer id prefix
PEER_ID_PREFIX_ICNTV = "00010023" # peer id prefix of user icntv

## follow display different time about playing video
PLAY_TIME = "300" # unit is seconds

CORE_VERSION = "2.4.8"
URL_FILE_NAME = "url-file.txt"

YUNSHANG_CONF = "/sdcard/yunshang/yunshang.conf"
"""






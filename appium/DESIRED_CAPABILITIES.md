Appium desired capabilities for mvvm_note_app_kotlin_android_studio

Detected package and launcher activity (from app/src/main/AndroidManifest.xml):
- package: com.bersyte.noteapp
- launcher activity: .MainActivity (fully-qualified: com.bersyte.noteapp.MainActivity)

Notes:
- You can either launch the already-installed app using appPackage/appActivity, or launch an APK built locally.
- To build the debug APK locally: ./gradlew assembleDebug (run from the project root). The debug APK will be at app/build/outputs/apk/debug/app-debug.apk

Example capability sets

1) If you want Appium to start the installed app (preferred when app already installed on emulator):

JSON (used by many clients):
{
  "platformName": "Android",
  "automationName": "UiAutomator2",
  "deviceName": "emulator-5554",
  "appPackage": "com.bersyte.noteapp",
  "appActivity": ".MainActivity",
  "appWaitActivity": "com.bersyte.noteapp.MainActivity",
  "noReset": true,
  "newCommandTimeout": 300
}

Python (Appium-Python-Client):
desired_caps = {
    "platformName": "Android",
    "automationName": "UiAutomator2",
    "deviceName": "emulator-5554",
    "appPackage": "com.bersyte.noteapp",
    "appActivity": ".MainActivity",
    "appWaitActivity": "com.bersyte.noteapp.MainActivity",
    "noReset": True,
    "newCommandTimeout": 300,
}

2) If you want Appium to install and launch a locally built APK:

JSON:
{
  "platformName": "Android",
  "automationName": "UiAutomator2",
  "deviceName": "emulator-5554",
  "app": "/absolute/path/to/mvvm_note_app_kotlin_android_studio/app/build/outputs/apk/debug/app-debug.apk",
  "noReset": false,
  "fullReset": false,
  "newCommandTimeout": 300
}

Python:
desired_caps = {
    "platformName": "Android",
    "automationName": "UiAutomator2",
    "deviceName": "emulator-5554",
    "app": "/absolute/path/to/mvvm_note_app_kotlin_android_studio/app/build/outputs/apk/debug/app-debug.apk",
    "noReset": False,
    "fullReset": False,
    "newCommandTimeout": 300,
}

Recommended steps to use these capabilities
1. Build the app (if using an APK):
   - cd /Users/olena.imfeld/Desktop/mvvm_note_app_kotlin_android_studio
   - ./gradlew assembleDebug
2. Start an Android emulator (the default device name for the first emulator instance is usually "emulator-5554"). To list AVDs: avdmanager list avd or emulator -list-avds
3. Install the APK manually (if you prefer): adb install -r app/build/outputs/apk/debug/app-debug.apk
4. Start Appium server (e.g., appium)
5. Connect using your client with the capabilities above

Troubleshooting
- If appActivity doesn't start, try the fully-qualified activity: "com.bersyte.noteapp.MainActivity"
- If the device name differs, replace "emulator-5554" with your emulator's device name or set "avd": "Your_AVD_Name" to tell Appium which AVD to launch.

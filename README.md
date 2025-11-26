mvvm_note_app_kotlin_android_studio

Quick start — build, run, and push

Prerequisites
- Android SDK & command-line tools (adb, emulator, avdmanager)
- Java JDK (Java 11 recommended for building this project)
- Gradle (the project includes a wrapper: ./gradlew)
- Git
- (Optional) Appium server and client if you want to run UI automation

Build the debug APK locally
1. From the project root:
   ./gradlew assembleDebug
   - Output APK: app/build/outputs/apk/debug/app-debug.apk
   - If you run into Kotlin/Room native errors on Apple Silicon (aarch64), use Java 11 when running Gradle:
     export JAVA_HOME=$(/usr/libexec/java_home -v 11)
     ./gradlew assembleDebug
   - If annotation-processing fails due to native sqlite for aarch64, either build on an x86_64 environment or add a sqlite native/JDBC dependency as needed.

Run on an emulator or device
1. Start an Android emulator (or connect a device):
   - List AVDs: emulator -list-avds
   - Start AVD: emulator -avd <AVD_NAME>
2. Install the APK (if you built it locally):
   adb install -r app/build/outputs/apk/debug/app-debug.apk
3. Launch the app activity:
   adb shell am start -n com.bersyte.noteapp/.MainActivity

Appium / automation hints
- I added Appium capability examples and notes at appium/DESIRED_CAPABILITIES.md
- Quick run file: RUN_APP_WITH_APPIUM.md
- Typical desired capabilities: use appPackage=com.bersyte.noteapp and appActivity=.MainActivity (or provide the built APK path to install automatically).

Push changes to your GitHub
1. Add remote (if you haven't already) and push:
   git remote add user https://github.com/olenabughunter/mvvm_note_app_kotlin_android_studio.git
   git push user master

Notes & troubleshooting
- If Gradle/Kotlin fails on recent JDKs due to reflective access, try adding the following to gradle.properties (already added in this repo):
  org.gradle.jvmargs=--add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED -Xmx1536m
  android.useAndroidX=true
  android.enableJetifier=true
- If Room's annotation processor throws errors about missing native sqlite on macOS aarch64, either switch to Java 11, run under x86_64 (Rosetta) or add an appropriate sqlite-jdbc native library so the processor can load the native implementation during kapt.

If you'd like, I can:
- Continue fixing the build so the APK can be produced on this machine (I can try adding a sqlite native dependency or other fixes)
- Or, if you build the APK locally and provide the path, I will install and launch it on the emulator or run Appium tests against it.

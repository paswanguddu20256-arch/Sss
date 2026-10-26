Apkname: Build Super Coin Adventure APK

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  workflow_dispatch: # Allows manual trigger from GitHub Actions tab on mobile or PC

jobs:
  build-android:
    name: Build Android APK
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'

      - name: Setup Android SDK
        uses: android-actions/setup-android@v3

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - name: Install Dependencies
        run: npm install

      - name: Build Web Application
        run: npm run build

      - name: Sync Capacitor Android Project
        run: npx cap sync android

      - name: Make Gradlew Executable
        run: chmod +x android/gradlew

      - name: Build Debug APK
        run: |
          cd android
          ./gradlew assembleDebug --stacktrace

      - name: Build Unsigned Release APK
        continue-on-error: true
        run: |
          cd android
          ./gradlew assembleRelease --stacktrace

      - name: Upload Debug APK Artifact
        uses: actions/upload-artifact@v4
        with:
          name: SuperCoinAdventure-Debug-APK
          path: android/app/build/outputs/apk/debug/app-debug.apk
          retention-days: 14

      - name: Upload Release APK (Unsigned) Artifact
        continue-on-error: true
        uses: actions/upload-artifact@v4
        with:
          name: SuperCoinAdventure-Release-Unsigned-APK
          path: android/app/build/outputs/apk/release/*.apk
          retention-days: 14

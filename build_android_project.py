import os
import shutil
import zipfile

BASE_DIR = "SuperCoinAdventure"
shutil.rmtree(BASE_DIR, ignore_errors=True)
os.makedirs(BASE_DIR, exist_ok=True)

# Copy the entire native-android directory structure to SuperCoinAdventure
src_native = "native-android"

for root, dirs, files in os.walk(src_native):
    for f in files:
        src_file = os.path.join(root, f)
        rel_path = os.path.relpath(src_file, src_native)
        dest_file = os.path.join(BASE_DIR, rel_path)
        os.makedirs(os.path.dirname(dest_file), exist_ok=True)
        shutil.copy2(src_file, dest_file)

# Add Groovy standard build files for maximum GitHub Actions compatibility
with open(os.path.join(BASE_DIR, "settings.gradle"), "w", encoding="utf-8") as f:
    f.write("""pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "Super Coin Adventure"
include ':app'
""")

with open(os.path.join(BASE_DIR, "build.gradle"), "w", encoding="utf-8") as f:
    f.write("""buildscript {
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:8.2.2'
        classpath 'org.jetbrains.kotlin:kotlin-gradle-plugin:1.9.22'
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}

task clean(type: Delete) {
    delete rootProject.buildDir
}
""")

with open(os.path.join(BASE_DIR, "gradle.properties"), "w", encoding="utf-8") as f:
    f.write("""org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
android.nonTransitiveRClass=true
kotlin.code.style=official
""")

with open(os.path.join(BASE_DIR, "app/build.gradle"), "w", encoding="utf-8") as f:
    f.write("""plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}

android {
    namespace 'com.supercoinadventure.game'
    compileSdk 34

    defaultConfig {
        applicationId "com.supercoinadventure.game"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0.0"

        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
        vectorDrawables {
            useSupportLibrary true
        }
    }

    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = '17'
    }
    buildFeatures {
        compose true
    }
    composeOptions {
        kotlinCompilerExtensionVersion '1.5.8'
    }
    packaging {
        resources {
            excludes += '/META-INF/{AL2.0,LGPL2.1}'
        }
    }
}

dependencies {
    implementation 'androidx.core:core-ktx:1.12.0'
    implementation 'androidx.lifecycle:lifecycle-runtime-ktx:2.7.0'
    implementation 'androidx.activity:activity-compose:1.8.2'
    implementation platform('androidx.compose:compose-bom:2024.02.00')
    implementation 'androidx.compose.ui:ui'
    implementation 'androidx.compose.ui:ui-graphics'
    implementation 'androidx.compose.ui:ui-tooling-preview'
    implementation 'androidx.compose.material3:material3'
    implementation 'androidx.compose.material:material-icons-extended'
}
""")

# .gitignore
with open(os.path.join(BASE_DIR, ".gitignore"), "w", encoding="utf-8") as f:
    f.write("""*.iml
.gradle
/local.properties
/.idea/
.DS_Store
/build
/captures
.externalNativeBuild
.cxx
local.properties
app/build/
""")

# README.md
with open(os.path.join(BASE_DIR, "README.md"), "w", encoding="utf-8") as f:
    f.write("""# Super Coin Adventure 🪙 - Native Android Game (Kotlin + Jetpack Compose)

This is the complete, compilable Native Android game project for "Super Coin Adventure".

## How to Build the APK on GitHub using Android Phone:
1. Create a new repository on GitHub (e.g. `super-coin-adventure`).
2. Upload all the files from this ZIP to the repository.
3. Open the **Actions** tab on GitHub.
4. Select the **Build Super Coin Adventure APK** workflow and tap **Run workflow**.
5. Wait 2-3 minutes for the build to complete.
6. Under **Artifacts**, tap **SuperCoinAdventure-Debug-APK** to download your APK file!
7. Install the APK on your Android phone and enjoy!
""")

# .github/workflows/android-apk.yml
os.makedirs(os.path.join(BASE_DIR, ".github/workflows"), exist_ok=True)
with open(os.path.join(BASE_DIR, ".github/workflows/android-apk.yml"), "w", encoding="utf-8") as f:
    f.write("""name: Build Super Coin Adventure APK

on:
  push:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  build:
    name: Build Debug APK
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

      - name: Setup Gradle
        uses: gradle/actions/setup-gradle@v3
        with:
          gradle-version: '8.2'

      - name: Build Debug APK
        run: gradle :app:assembleDebug --stacktrace --no-daemon

      - name: Upload Debug APK Artifact
        uses: actions/upload-artifact@v4
        with:
          name: SuperCoinAdventure-Debug-APK
          path: app/build/outputs/apk/debug/*.apk
          retention-days: 14
""")

# Create the real ZIP in public/ and root
os.makedirs("public", exist_ok=True)
zip_public = "public/SuperCoinAdventure_Android_Project.zip"
zip_root = "SuperCoinAdventure_Android_Project.zip"

all_files = []
with zipfile.ZipFile(zip_public, "w", zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(BASE_DIR):
        for f in files:
            full_path = os.path.join(root, f)
            arc_name = os.path.relpath(full_path, BASE_DIR)
            zf.write(full_path, arc_name)
            all_files.append(arc_name)

shutil.copy2(zip_public, zip_root)

zip_size = os.path.getsize(zip_public)
print(f"PACKED {len(all_files)} FILES INTO {zip_public} ({zip_size} bytes)")
for af in sorted(all_files):
    print("  +", af)

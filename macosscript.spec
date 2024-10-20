name: Auto Compile on Commit (macOS)

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: macos-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Build the application with PyInstaller
      run: |
        pyinstaller script.spec

    - name: List contents of the output directory
      run: |
        ls -R dist

    - name: Prepare files for zipping
      run: |
        mkdir -p zip_temp
        mv dist/Vector24.app zip_temp/  # Moving the .app bundle
        [ -f app.log ] && mv app.log zip_temp/ || echo "app.log not found"
        [ -f config.json ] && mv config.json zip_temp/ || echo "config.json not found"
        [ -f positions.json ] && mv positions.json zip_temp/ || echo "positions.json not found"
        [ -f startup.mp3 ] && mv startup.mp3 zip_temp/ || echo "startup.mp3 not found"
        [ -f version.json ] && mv version.json zip_temp/ || echo "version.json not found"

    - name: Create ZIP archive
      run: |
        cd zip_temp
        zip -r ../Vector24-${{ github.sha }}-amd64-macos.zip ./*

    - name: Upload ZIP as an artifact
      uses: actions/upload-artifact@v3
      with:
        name: final-zip-package
        path: Vector24-${{ github.sha }}-amd64-macos.zip

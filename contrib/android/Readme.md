# Kivy GUI

The Kivy GUI is used with Electrum on Android devices.
To generate an APK file, follow these instructions.

## Android binary with Docker

✓ _These binaries should be reproducible, meaning you should be able to generate
   binaries that match the official releases._

This assumes an Ubuntu (x86_64) host, but it should not be too hard to adapt to another
similar system.

1. Install Docker

    See `contrib/docker_notes.md`.

2. Build binaries

    The build script takes a few arguments. To see syntax, run it without providing any:
    ```
    $ ./build.sh
    ```
    For development, consider e.g. `$ ./build.sh kivy arm64-v8a debug`

    If you want reproducibility, try instead e.g.:
    ```
    $ ELECBUILD_COMMIT=HEAD ELECBUILD_NOCACHE=1 ./build.sh kivy all release-unsigned
    ```

3. The generated binary is in `./dist`.


## Verifying reproducibility and comparing against official binary

Every user can verify that the official binary was created from the source code in this
repository.

1. Build your own binary as described above.
   Make sure you don't build in `debug` mode,
   instead use either of `release` or `release-unsigned`.
   If you build in `release` mode, the apk will be signed, which requires a keystore
   that you need to create manually (see source of `make_apk.sh` for an example).
2. Note that the binaries are not going to be byte-for-byte identical, as the official
   release is signed by a keystore that only the project maintainers have.
   You can use the `apkdiff.py` python script (written by the Signal developers) to compare
   the two binaries.
    ```
    $ python3 contrib/android/apkdiff.py Electrum_apk_that_you_built.apk Electrum_apk_official_release.apk
    ```
   This should output `APKs match!`.


## FAQ

### I changed something but I don't see any differences on the phone. What did I do wrong?
You probably need to clear the cache: `rm -rf .buildozer/android/platform/build-*/{build,dists}`


### How do I deploy on connected phone for quick testing?
Assuming `adb` is installed:
```
$ adb -d install -r dist/Electrum-*-arm64-v8a-debug.apk
$ adb shell monkey -p org.electrum_bte.electrum_bte 1
```


### How do I get an interactive shell inside docker?
```
$ docker run -it --rm \
    -v $PWD:/home/user/wspace/electrum \
    -v $PWD/.buildozer/.gradle:/home/user/.gradle \
    --workdir /home/user/wspace/electrum \
    electrum-android-builder-img
```


### How do I get more verbose logs for the build?
See `log_level` in `buildozer.spec`


### How can I see logs at runtime?
This should work OK for most scenarios:
```
adb logcat | grep python
```
Better `grep` but fragile because of `cut`:
```
adb logcat | grep -F "`adb shell ps | grep org.electrum_bte.electrum_bte | cut -c14-19`"
```


### Kivy can be run directly on Linux Desktop. How?
Install Kivy.

Build atlas: `(cd contrib/android/; make theming)`

Run electrum with the `-g` switch: `electrum -g kivy`

### debug vs release build
If you just follow the instructions above, you will build the apk
in debug mode. The most notable difference is that the apk will be
signed using a debug keystore. If you are planning to upload
what you build to e.g. the Play Store, you should create your own
keystore, back it up safely, and run `./contrib/make_apk.sh release`.

See e.g. [kivy wiki](https://github.com/kivy/kivy/wiki/Creating-a-Release-APK)
and [android dev docs](https://developer.android.com/studio/build/building-cmdline#sign_cmdline).

### Access datadir on Android from desktop (e.g. to copy wallet file)
Note that this only works for debug builds! Otherwise the security model
of Android does not let you access the internal storage of an app without root.
(See [this](https://stackoverflow.com/q/9017073))
```
$ adb shell
$ run-as org.electrum_bte.electrum_bte ls /data/data/org.electrum_bte.electrum_bte/files/data
$ run-as org.electrum_bte.electrum_bte cp /data/data/org.electrum_bte.electrum_bte/files/data/wallets/my_wallet /sdcard/some_path/my_wallet
```

### Update - How Fast build release

Host ubuntu 18.04-LTS

Git clone https://github.com/bitweb-project/electrum-bte.git

Generate your keystore files

See e.g. [kivy wiki](https://github.com/kivy/kivy/wiki/Creating-a-Release-APK)

as example rename it to android_release.keystore

got to contrib\android\make_apk and edit it

from 

if [[ -n "$1"  && "$1" == "release" ]] ; then
    echo -n Keystore Password:
    read -s password
    export P4A_RELEASE_KEYSTORE=~/.keystore
    export P4A_RELEASE_KEYSTORE_PASSWD=$password
    export P4A_RELEASE_KEYALIAS_PASSWD=$password
    export P4A_RELEASE_KEYALIAS=electrum
    # build two apks
    export APP_ANDROID_ARCH=armeabi-v7a
    make release
    export APP_ANDROID_ARCH=arm64-v8a
    make release
    
to

if [[ -n "$1"  && "$1" == "release" ]] ; then
    echo -n Keystore Password:
    read -s password
    export P4A_RELEASE_KEYSTORE="$CONTRIB_ANDROID"/android_release.keystore
    export P4A_RELEASE_KEYSTORE_PASSWD=Your_Pass-for-key-store-file
    export P4A_RELEASE_KEYALIAS_PASSWD=Your_Pass-for-key-store-file
    export P4A_RELEASE_KEYALIAS=Your alis for key store file.
    # build two apks
    export APP_ANDROID_ARCH=armeabi-v7a
    make release
    export APP_ANDROID_ARCH=arm64-v8a
    make release
    
Now copy keystore files and put it to contrib/android

and run at android folder

```
    ./build.sh kivy all release
```


Then

This assumes an Ubuntu (x86_64) host, but it should not be too hard to adapt to another
similar system. The docker commands should be executed in the project's root
folder.

1. Install Docker

    ```
    $ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    $ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    $ sudo apt-get update
    $ sudo apt-get install -y docker-ce
    ```

2. Build image

    ```
    $ sudo docker build -t electrum-android-builder-img contrib/android
    ```

3. Build locale files

    ```
    $ ./contrib/pull_locale
    ```

4. Prepare pure python dependencies

    ```
    $ ./contrib/make_packages
    ```

5. Build binaries

    ```
    $ mkdir --parents $PWD/.buildozer/.gradle
    $ sudo docker run -it --rm \
        --name electrum-android-builder-cont \
        -v $PWD:/home/user/wspace/electrum \
        -v $PWD/.buildozer/.gradle:/home/user/.gradle \
        -v ~/.keystore:/home/user/.keystore \
        --workdir /home/user/wspace/electrum \
        electrum-android-builder-img \
        ./contrib/android/make_apk release
    ```
    This mounts the project dir inside the container,
    and so the modifications will affect it, e.g. `.buildozer` folder
    will be created.

5. The generated binary is in `./bin`.
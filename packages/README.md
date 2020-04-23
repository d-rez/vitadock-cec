# Information about these packages

VitaDock MPV edition comes by default with pre-compiled and pre-installed multiple packages executed by a script called Vidware shared by a raspberry pi community user at https://www.raspberrypi.org/forums/viewtopic.php?t=199775

Now this is great, but python-mpv module needs a shared libmpv.so library, which wasn't built by default. To build MPV with libmpv shared library though... You have to re-build ffmpeg with -fPIC parameter

To save time and effort you can simply install these two packages over the ones already present and it will take care of all dependencies for MPV playback inside my script

Just follow main instructions of the script or run these two commands from inside of this folder:

```
sudo dpkg -i ffmpeg_4.0.2-1_armhf.deb
sudo dpkg -i mpv_0.29.0-1_armhf.deb
```

# License Information
Note: My project's license obviously doesn't apply to packages in this folder, each package has its own license and was compiled without any code changes other than listed in the project linked above

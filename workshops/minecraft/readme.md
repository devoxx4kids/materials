# Minecraft Modding using Forge

## Quick Start Instructions

You need to download/install only the following two components:

* [JDK 7](http://www.oracle.com/technetwork/java/javase/downloads/jdk7-downloads-1880260.html)
* Modding Kit (one of the following based upon your platform)
    * [Modkit for Mac](https://delucaconsulting.app.box.com/d4kminecraft/1/1415067806/12742874198/1)
    * [Modkit for Windows - 32 bit](https://delucaconsulting.app.box.com/d4kminecraft/1/1415067806/14622594726/1)
    * [Modkit for Windows - 64 bit](https://delucaconsulting.app.box.com/d4kminecraft/1/1415067806/14622936096/1)

That's it, now follow the <a href="http://www.youtube.com/embed/QkPq6KUvY7g?list=PLX8CzqL3ArzVET0IIHcCf3-JfzY8RL4xG">tutorials</a>.

## Detailed Instructions

You only need to follow these instructions if you are planning to build your own modding kit. Generally the pre-built mod kits (as explained in Quick Start above) would work. Building mod kits could be a significant work and may require significant understanding of the build scripts.

If you are ready to dare, then follow the instructions:

Download Src bundle from (files.minecraftforge.net). As of Jan 1, 2014 [1.6.4-Recommended](http://files.minecraftforge.net/maven/net/minecraftforge/forge/1.6.4-9.11.1.965/forge-1.6.4-9.11.1.965-src.zip) and [1.7.2-Latest](http://files.minecraftforge.net/maven/net/minecraftforge/forge/1.7.2-10.12.0.982/forge-1.7.2-10.12.0.982-src.zip) bundles are available. 1.7.x are not recommended as [explained here](https://github.com/MinecraftForge/ForgeGradle/issues/27#issuecomment-31436639).

* For 1.6.4 (recommended)
    * Unzip the downloaded bundle
    * Change directory to "forge"
    * Give the command `install.sh` (on Mac) or `install.cmd` (on Windows) to configure Forge for modding.
* For 1.7.2 (not recommended)
    * Give the command `./gradlew setupDevWorkspace --refresh-dependencies`

      On Mac, you may encounter [ForgeGradle#34](https://github.com/MinecraftForge/ForgeGradle/issues/34) and will have to manually edit `build/unpacked/dev.json` as [explained here](https://github.com/MinecraftForge/ForgeGradle/issues/34#issuecomment-31344841). And then give `./gradlew setupDecomWorkspace`
    * `./gradlew eclipse` to generate Eclipse specific project. You will have to manually edit `dev.json` once again.


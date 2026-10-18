# kpython wheels

A package index of wheels for [kpython](https://github.com/warpforgedotco/kpython), the statically linked CPython: build tools, static dependencies and packages, built with the recipes in [warpforgedotco/MonolithPy-packages](https://github.com/warpforgedotco/MonolithPy-packages).

kpython's pip searches it as an extra index:

```
https://warpforgedotco.github.io/kpython-wheels/simple/
```

Only kpython can install these wheels. Their tags, such as `monolithpy315-mp3_15-macosx_11_0_arm64`, match no other interpreter.

## Contents

For Python 3.15, built from source with the recipes and tested with them:

- **macOS arm64** (`mp3_15-macos-arm64`): numpy, scipy, pandas, scikit-learn, statsmodels, matplotlib, contourpy, pillow, kiwisolver, cffi, pyyaml, multidict, frozenlist, propcache, yarl and aiohttp; the dependencies OpenBLAS, gcc-rt, raqm, jpeg and libyaml; and the build tools clang, gcc, cmake and ninja.
- **Linux x86_64** (`mp3_15-linux-x86_64`): numpy, scipy, pandas, scikit-learn, statsmodels, matplotlib, contourpy, pillow, kiwisolver, cffi, pyyaml, multidict, frozenlist, propcache, yarl and aiohttp; the dependencies OpenBLAS, gcc-rt, raqm, jpeg and libyaml; and the build tools cmake, ninja and meson.

For Python 3.14, MonolithPy's mirror has macOS wheels, but its numpy 2.5.3 doesn't link BLAS into matmul (60 times slower):

- **macOS arm64** (`mp3_14-macos-arm64`): numpy 2.5.4 with OpenBLAS 0.3.34 and gcc-rt, built with the fork's recipes. As a newer version, pip prefers it to the mirror's.
- **Linux x86_64** (`mp3_14-linux-x86_64`): the same set as for 3.15 on Linux. MonolithPy's mirror has no Linux wheels.

The macOS wheels target macOS 11.0, like the interpreter, and are tagged `macosx_11_0_arm64`.

The Linux wheels are built in the `manylinux_2_28` image and tagged `manylinux_2_28_x86_64`: they need glibc 2.28 or newer, so they run on RHEL/Rocky/Alma 8 and later, Debian 10 and later and Ubuntu 18.10 and later. Installing a package relinks kpython with the system's C compiler, which has to read the GCC 14 LTO objects that kpython and these wheels hold: GCC 14 or newer. On RHEL 8 and 9 that is `gcc-toolset-14`.

## Layout

- **Releases** hold the wheels, one release per Python series and platform, such as `mp3_15-macos-arm64`.
- **The index** on GitHub Pages lists every wheel of every release under its project and links to the release asset with its SHA-256. `scripts/build_index.py` builds it, and the `Index` workflow republishes it.

## Publishing

Build the wheels with kpython, for example by installing a package with its recipe, then:

```console
python3 scripts/publish.py mp3_15-macos-arm64 path/to/*.whl
```

This creates the release if needed, uploads the wheels (replacing any of the same name), and starts the `Index` workflow. Release assets are limited to 2 GB each.

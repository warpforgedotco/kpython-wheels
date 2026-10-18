# kpython wheels

A package index of wheels for [kpython](https://github.com/warpforgedotco/kpython), the statically linked CPython: build tools, static dependencies and packages, built with the recipes in [warpforgedotco/MonolithPy-packages](https://github.com/warpforgedotco/MonolithPy-packages).

kpython's pip searches it as an extra index:

```
https://warpforgedotco.github.io/kpython-wheels/simple/
```

Only kpython can install these wheels. Their tags, such as `monolithpy315-mp3_15-macosx_26_0_arm64`, match no other interpreter.

## Contents

For Python 3.15, built from source with the recipes and tested with them:

- **macOS arm64** (`mp3_15-macos-arm64`): numpy, scipy, pandas, scikit-learn, statsmodels, matplotlib, contourpy, pillow, kiwisolver, cffi, pyyaml, multidict, frozenlist, propcache, yarl and aiohttp; the dependencies OpenBLAS, gcc-rt, raqm, jpeg and libyaml; and the build tools clang, gcc, cmake and ninja.
- **Linux x86_64** (`mp3_15-linux-x86_64`): numpy, scipy, pandas, scikit-learn, statsmodels, matplotlib, contourpy, pillow, kiwisolver and cffi; the dependencies OpenBLAS, gcc-rt, raqm and jpeg; and the build tools cmake, ninja and meson.

The macOS wheels were built on macOS 26, and most are tagged `macosx_26_0`, so pip installs them only on macOS 26 or newer. The Linux wheels were built on Ubuntu 26.04 and are tagged `manylinux_2_43`, for glibc 2.43 or newer.

## Layout

- **Releases** hold the wheels, one release per Python series and platform, such as `mp3_15-macos-arm64`.
- **The index** on GitHub Pages lists every wheel of every release under its project and links to the release asset with its SHA-256. `scripts/build_index.py` builds it, and the `Index` workflow republishes it.

## Publishing

Build the wheels with kpython, for example by installing a package with its recipe, then:

```console
python3 scripts/publish.py mp3_15-macos-arm64 path/to/*.whl
```

This creates the release if needed, uploads the wheels (replacing any of the same name), and starts the `Index` workflow. Release assets are limited to 2 GB each.

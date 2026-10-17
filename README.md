# kpython wheels

A package index of wheels for [kpython](https://github.com/warpforgedotco/kpython), the statically linked CPython: build tools, static dependencies and packages, built with the recipes in [warpforgedotco/MonolithPy-packages](https://github.com/warpforgedotco/MonolithPy-packages).

kpython's pip searches it as an extra index:

```
https://warpforgedotco.github.io/kpython-wheels/simple/
```

Only kpython can install these wheels. Their tags, such as `monolithpy315-mp3_15-macosx_26_0_arm64`, match no other interpreter.

## Layout

- **Releases** hold the wheels, one release per Python series and platform, such as `mp3_15-macos-arm64`.
- **The index** on GitHub Pages lists every wheel of every release under its project and links to the release asset with its SHA-256. `scripts/build_index.py` builds it, and the `Index` workflow republishes it.

## Publishing

Build the wheels with kpython, for example by installing a package with its recipe, then:

```console
python3 scripts/publish.py mp3_15-macos-arm64 path/to/*.whl
```

This creates the release if needed, uploads the wheels (replacing any of the same name), and starts the `Index` workflow. Release assets are limited to 2 GB each.

# adze

**adze** is a Python package for accurate polyhedron clipping
 and anti-aliased voxelization.

**Homepage:** https://mpxd.net/code/jan/adze

**Capabilities:**
    - Clipping or splitting arbitrary polyhedra
        - by a plane or a collection of planes (i.e. a convex polyhedron)
    - Voxelizing arbitrary polyhedra
        -


## Installation

**Dependencies:**
* python 3.6 or newer
* numpy
* pytest (optional, testing)
* pytest-benchmark (optional, benchmarking)

Install with pip from PyPi (preferred):
```bash
pip3 install adze
```

Install directly from git repository:
```bash
pip3 install git+https://mpxd.net/code/jan/adze.git@release
```

## Documentation
Most functions and classes are documented inline.

To read the inline help,
```python3
import adze
help(adze)
help(adze.split)
```

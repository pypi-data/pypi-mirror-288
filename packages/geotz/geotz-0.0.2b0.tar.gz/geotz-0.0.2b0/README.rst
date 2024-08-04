.. image:: https://github.com/dmayo3/geotz/actions/workflows/ci.yaml/badge.svg
    :target: https://github.com/dmayo3/mocksafe/actions/workflows/ci.yaml?query=branch%3Amain
    :alt: Github Actions Status
.. image:: https://codecov.io/github/dmayo3/geotz/graph/badge.svg?token=A0WO17S0KD 
 :target: https://codecov.io/github/dmayo3/geotz
.. image:: https://readthedocs.org/projects/geotz/badge/?version=latest
    :target: https://geotz.readthedocs.io/en/stable/?badge=latest
    :alt: Documentation Status
.. image:: https://badge.fury.io/py/geotz.svg
    :target: https://badge.fury.io/py/geotz
    :alt: PyPI Package
.. image:: https://img.shields.io/pypi/pyversions/geotz.svg
    :target: https://pypi.org/project/geotz
    :alt: Supported versions
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code style: black
.. image:: http://www.mypy-lang.org/static/mypy_badge.svg
    :target: http://mypy-lang.org/
    :alt: Type checked by mypy
.. image:: https://img.shields.io/badge/License-CC%20BY%204.0%20%2B%20MIT-yellow
   :target: https://github.com/dmayo3/geotz/blob/main/LICENSE
   :alt: License


GeoTZ v0.0.2b0
--------------

Docs: https://geotz.readthedocs.io/

This is a small library for looking up the timezone for a given country code
and postal code / postal code prefix. The main logic under `geotz` is very
small indeed, so you can easily read it for yourself.

It's well tested - see the coverage badge above and take a look at the tests
for all the cases that are covered.

Compared to alternatives like `geopy` or `pgeocode`, it's intended to be
easier to use, less feature rich, and more lightweight.

It uses offline data from www.geonames.org to find the approximate location
and then uses another library to convert that into a timezone.

Please read the LICENSE file for important information about using this
library and the data contained within.

Motivation
----------

1. Easy to use. No API key or external API service required.

2. Fast offline lookup.

3. No downloads required; the necessary data comes bundled with the package.

4. No network requests.

5. I tried to keep the extra dependencies to a minimum.

6. Data is loaded from disk on demand, so as to not use unnecessary memory.

Development
-----------

To run the build, there's the GitHub actions workflows as well as the option to run locally.

For running the build locally, use `pip install tox` and the run `tox` in the repository base
directory (or `tox -p` to run the build in parallel).

1. Ensure you have `tox` installed e.g. by running `pip install tox`

2. Extract data `tox -e extract_data`

3. Run the build: `tox`

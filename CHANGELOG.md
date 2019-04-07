# Changelog

This changelog is losely based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/).
Cenv adheres to [Semi-Semantic Versioning](http://semver.org/spec/v2.0.0.html). That means it adheres to Semantic Versioning, except when I screw something up. That said, [Semantic Versioning is mostly a pit of lies anyway](https://www.youtube.com/watch?v=tISy7EJQPzI) so hopefully you won't judge me too much.

## [1.1.1] - 2019-03-23

- Variables set in bash scripts were not being properly quoted leading to issues in some cases. They may still not be in Python 2, but are in Python 3. Python 2 uses a hack which may not be worth keeping.

## [1.1.0] - 2018-01-02

- The PATH environment variable is now set to include the `bin` directory of the activated env. This allows users to run executables installed to the `env`.

## [1.0.0] - 2017-12-31

- Added a changelog.

**worldview-config** is an open source project and Python package that makes maintaining
your own instance of [NASA Worldview](https://github.com/nasa-gibs/worldview) easier.

# Installation
```
pip install worldview-config
```

# Usage
This package adds the `worldview_config` CLI to your path which provides some commands:
- Keep all your layer configuration in one place and dynamically render
the full set of configuration files with `worldview_config render`.
- Only maintain your custom content - at build time, merge it into the default config
using `worldview_config merge`.  Avoid making a static copy of the default config and
becoming quickly out of date.

For an example of how to use this tool to deploy your own custom Worldview instance,
see the [ASIPS Worldview](https://github.com/asips/asips-worldview) project.

# Contributing
This project is in development and compatibility with the full feature set of NASA Worldview
is not guaranteed.  Contributions are welcome.

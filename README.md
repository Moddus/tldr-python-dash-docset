# tldr-pages Python Dash Docset Generator
This project builds a [Dash][1] docset for the [tldr-pages][3]
user manual.

Thanks to [tldr.jsx][4] for your great CSS!

### This is a fork

The original author of this project, [Moddus](https://github.com/Moddus/tldr-python-dash-docset), appears to have abandoned it. This fork contains some [bug fixes and small improvements](https://github.com/Moddus/tldr-python-dash-docset/pull/5) to the original.

### Build

If you have python 3 and the [required packages](requirements.txt):

    python generator.py

Or use Docker to create an environment and build:

    docker-compose up


[1]: http://kapeli.com/dash
[2]: http://zealdocs.org/
[3]: https://github.com/tldr-pages/tldr
[4]: https://github.com/ostera/tldr.jsx

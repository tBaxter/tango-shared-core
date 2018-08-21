Tango Shared Core
=====

Provides shared and core functionality used by multiple Tango apps,
and will be installed by them as needed.

[![Build Status](https://travis-ci.org/tBaxter/tango-shared-core.svg?branch=master)](https://travis-ci.org/tBaxter/tango-shared-core)

## So what's in here, anyway?

### Base models
Abstract base models are included for common content objects, including images, so you can handle common fields and needs quickly, easily and consistently.

### Useful settings
A lot of them. Seriously, take a look at the settings file.

### Template tags and filters
* Formatting helpers
* Simple (and non-tracking) social media links.
* Additional time output helpers

### A robust base template
Based on HTML5 Boilerplate, but for Django, and battle-tested.

### A administrator how-to section in the admin
You already have developer documentation in the admin. This gives you hooks to include documentation aimed at administrators as well, just by including a `how_to.md` file in your app. See the other Tango apps for examples.

### Middleware and Context Processors
* StripEmptyLines: Strips HTML output of excessive newlines
* CompactHTMLMiddleware: Pseudo-minification for HTML output, good for a 30-40% reduction in file size. Not entirely safe with `pre` tags. Use with caution.
* The site_processor context processor adds a bunch of useful things in context.

### Utils
* Robust user submission sanitization
* Map tools to ease Google Map integration (Note: You'll need to set `GMAP_KEY` in your settings)

### JS
* A solid implementation of Markitup

## Installation
Installation should be automatic, from the application needing it.

You can also install from pip or github.

If you run into appRegistry issues, be sure  `INSTALLED_APPS` contains
`easy_thumbnails` and  `django.contrib.contenttypes`.

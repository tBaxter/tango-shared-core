# Tango Shared Core Change Log

### 0.14.2
* Addressing more issues in humanized_join.

### 0.14.1
* Addressing some issues in humanized_join.

### 0.14.0
* Removed humanized_simple_join tag, improved humanized_join, and polished tests.

### 0.13.0
* Removed internal xmltramp copy in favor of xmltramp2.

### 0.12.5
* Passing tests for Python3 support

### 0.12.4
* Added shared user fixture to help dependent apps with Travis.

### 0.12.3
* Better classification in setup.py

### 0.12.2
* Pulling tango-voting from PyPi instead of Github.
* skeleton of Travis support.

### 0.12.1 -- 10.30.14
* Fixed setup.py bug that kept dependencies from being loaded reliably.

### 0.12.0 -- 10.1.14
* Added some template tag tests
* renamed humanize_join to humanized_simple_join
* Included more robust humanized_simple_join that uses get_absolute_url to create a link to the object.

### 0.11.0 -- 10.1.14
* Moved modernizer to bottom of file. Note that you may want to use a custom modernizr build and put an html5 shim high in the document. {% block htmlshiv %} has been added for that purpose in the base_all template. See http://stackoverflow.com/a/16085479 for details.
* Added humanize_join template filter in formatting tags, to provide nice "apples, oranges, and pears" output.

### 0.10.0 -- 8.27.14
Added three col thumbnail defaults

### 0.9.0
Spun admin functionality out to tango-admin

### 0.8.2
Don't create top assets slideshow unless top assets > 1

### 0.8.1
Restored some photo sizes that went missing

### 0.8.0
New column-based sizes for images

### 0.7.7
.format() doesn't always play nice with 2.7. Removed some instances for reliability.

### 0.7.6
Small fix for emoticon replacements

### 0.7.5
Attempted to resolve some intermittent unicode errors in sanetization.

### 0.7.4
Removed old comment templates. They don't belong here.

### 0.7.3
Fixed attribute in comment list

### 0.7.2
Template tag improvements

### 0.7.1
BaseUserContentModel using 'user' as FK instead of 'author'

### 0.7
Added BaseUserContentModel, an abstract base model to simplify standardizing and sanitizing user-submitted content.

## 0.6.1
* Removed duplicated field in models
* Moved header out of wrapper
* Added ability to pass arbitrary classnames to formatted_time helper for better microformat compliance

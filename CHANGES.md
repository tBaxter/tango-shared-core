# Tango Shared Core Change Log

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

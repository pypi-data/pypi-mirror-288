
# Changelog
All notable changes to wuttaweb will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## v0.4.0 (2024-08-05)

### Feat

- add basic App Info view (index only)
- add initial `MasterView` support

### Fix

- add `notfound()` View method; auto-append trailing slash
- bump min version for wuttjamaican

## v0.3.0 (2024-08-05)

### Feat

- add support for admin user to become / stop being root
- add view to change current user password
- add basic logo, favicon images
- add auth views, for login/logout
- add custom security policy, login/logout for pyramid
- add `wuttaweb.views.essential` module
- add initial/basic forms support
- add `wuttaweb.db` module, with `Session`
- add `util.get_form_data()` convenience function

### Fix

- allow custom user getter for `new_request_set_user()` hook

## v0.2.0 (2024-07-14)

### Feat

- add basic support for menu handler

- add "web handler" feature; it must get the menu handler

## v0.1.0 (2024-07-12)

### Feat

- basic support for WSGI app, views, templates

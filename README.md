[![Tests](https://github.com//ckanext-resource-visibility/workflows/Tests/badge.svg?branch=main)](https://github.com//ckanext-resource-visibility/actions)

# ckanext-resource-visibility

## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.8 and earlier | no            |
| 2.9             | no (2.1.2)    |
| 2.10            | no (2.1.2)    |
| 2.11            | yes (2.2.x+ ) |
| 2.12            | yes           |


## Installation

To install ckanext-resource-visibility:

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv

       pip install ckanext-resource-visibility

   or 

       git clone https://github.com//ckanext-resource-visibility.git
       cd ckanext-resource-visibility
       pip install -e .

3. Add `resource-visibility` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

     sudo service apache2 reload


## Config settings

    # The minimum number of hours to wait before re-checking a resource
    # (optional, default: 24).
    ckanext.resource_visibility.some_setting = some_default_value


## Developer installation

To install ckanext-resource-visibility for development, activate your CKAN virtualenv and
do:

    git clone https://github.com//ckanext-resource-visibility.git
    cd ckanext-resource-visibility
    pip install -e '.[dev]'
    pip install -r dev-requirements.txt


## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini


## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)

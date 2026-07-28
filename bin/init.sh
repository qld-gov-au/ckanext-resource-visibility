#!/usr/bin/env sh
##
# Initialise CKAN data for testing.
#
set -e

. `dirname $0`/activate
ckan -c $CKAN_INI db clean --yes
ckan -c $CKAN_INI db init
# apply any plugin migrations
ckan -c $CKAN_INI db upgrade

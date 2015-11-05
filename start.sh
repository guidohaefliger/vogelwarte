pushd ../geonode
paver start_geoserver
popd
python manage.py runserver
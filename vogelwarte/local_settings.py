DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'vogelwarte',
        'USER' : 'Simone',
    },
    # vector datastore for uploads
    'datastore' : {
       'ENGINE': 'django.contrib.gis.db.backends.postgis',
       'NAME': 'vogelwarte',
       'USER' : 'Simone',
       'HOST': 'localhost',
       'PORT': '5432'
    }
}
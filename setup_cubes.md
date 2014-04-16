### Установка
Скачиваем и устанавливаем [Cubes](https://github.com/Stiivi/cubes). 
Сначала установим необходимые библиотеки

	pip install pytz python-dateutil jsonschema
	pip install sqlalchemy flask

Далее устанавливаем **cubes**:

	pip install cubes

### Настройка

Для Windows необходимо в файле *$PYTHON_DIR$\Lib\site-packages\dateutil\tz.py* заменить 40 строку:

	return myfunc(*args, **kwargs).encode()

на 

	return myfunc(*args, **kwargs)

Кроме этого необходимо *$PYTHON_DIR$\Lib\site-packages\cubes-1.0alpha-py2.7.egg\cubes* добавить следующий [код](https://github.com/rgruebel/cubes/commit/4fb6b8e1d85a99bc7bdd4f88697ca6731503eee6) начиная с 90 строки:

	elif len(parts.scheme) == 1 and os.path.isdir(source):
		# TODO: same hack as in _json_from_url
        return read_model_metadata_bundle(source)	

### Разворачиваем тестовый пример

Клонируем ветку с GitHub'а:

	git clone git://github.com/Stiivi/cubes.git

переходим в папку с примерами:

	cd cubes
	cd examples/hello_world

Далее разворачиваем тестовые данные с помощью скрипта *prepare_data.py*:

	python prepare_data.py

Запускаем *slicer*:

- для Unix
	
	```slicer serve slicer.ini```

- для Winodows

	```python c:\Python27\Scripts\slicer serve slicer.ini```

Подробнее об [разворачивании](http://pythonhosted.org/cubes/deployment.html) сервере и [конфигурировании](http://pythonhosted.org/cubes/configuration.html) на базе apache в документации.
	
### Установка cubesviewer

Копируем [репозиторий](https://github.com/nonsleepr/cubesviewer):

	git clone https://github.com/nonsleepr/cubesviewer.git


Копируем содержимое папки */src* в нужный каталог

Конфигурируем Django оболочку в *web/cvapp/settings.py*

Внести изменения от [коммита](https://bitbucket.org/spookylukey/django-piston/commits/40645e760ea2cb9a37d87c9352607b3fa7fac346#chg-piston/emitters.py) в dajno-piston

Синхронизируем приложение из *$INSTALLATION_PATH$/web/cvapp* с БД

	python manage.py syncdb

Запускаем тестовый сервер Django:

	python manage.py runserver

Подробнее в [документации](https://github.com/nonsleepr/cubesviewer/blob/master/doc/guide/cubesviewer-gui-installation.md)
# UNEG Fleet
#### _Proyecto de trabajo de grado para optar al título de Ingeniería Informática de la Universidad Nacional Experimental de Guayana_
_Desarrollado por:_ <br>
José Arenas <br>
Jennifer Rondón <br>

## Features

- Operaciones CRUD para vehículos
- Operaciones CRUD para conductores
- Operaciones CRUD para trackers
- Consulta de status de los trackers, envío de comandos al dispositivo
- Manejo de roles de usuarios para separar la lógica de negocios
- Visualización de reportes


> El desarrollo de este proyecto surge de la necesidad de crear una plataforma 
> que permita unificar el manejo de flotas vehiculares, así como también los
> aspectos asociados al mantenimiento de los vehículos, los datos de los conductores
> y el rastreo de los vehículos a través de dispositivos GPS <br>
> Todo esto junto con un dashboard que permita revisar las métricas en tiempo real
> de los aspectos más resaltantes de la gestión de la flota vehicular.


## Stack de tecnologías

Entre las tecnologías utilizadas como apoyo para desarrollar este proyecto, están:

- [Python](https://www.python.org/) - Lenguaje de programación interpretado para el backend
- [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Un micro-framework para Python
- [Jinja](https://jinja.palletsprojects.com/en/2.11.x/) - Motor de renderizado de plantillas de Python
- [MySQL](https://www.mysql.com/) - Motor de base de datos 
- [Twitter Bootstrap](https://getbootstrap.com/) - Framework UI para maquetado de interfaces modernas
- [NodeJS](https://nodejs.org/es/) - Entorno en tiempo de ejecución para JavaScript del lado del servidor
- [JavaScript](https://www.javascript.com/) Lenguaje interpretado por los navegadores para darle funcionalidad al frontend


## Instalación

UNEG Fleet requiere: <br>
[Python 3.8](https://www.python.org/) para su ejecución <br>
[venv](https://packaging.python.org/key_projects/#venv) para la creación de un entorno virtual aislado <br>
[Pip](https://pypi.org/project/pip/) para instalar las dependencias <br>

Instalación de dependencias e inicialización del servidor en modo desarrollo:

Nos movemos a la carpeta del proyecto
```sh
cd tesis_fleet
```
Creamos un entorno virtual con venv
```sh
python3 -m venv venv 
```
Activamos el entorno virtual
```sh
source /venv/bin/activate
```

Instalamos las dependencias del proyecto con Pip
```sh
pip install -r requirements.txt
```
Definimos las variables de entorno temporales
```sh
export FLASK_APP=wsgi.py
export FLASK_ENV=development
```
Lanzamos el servidor de desarrollo
```sh
flask run
```

El proyecto sera accesible a través del navegador en la url:
```sh
127.0.0.1:8000
```
## License

MIT



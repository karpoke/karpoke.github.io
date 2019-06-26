Title: Kippo, probando un honeypot en Ubuntu
Date: 2012-05-13 16:19
Author: Nacho Cano
Tags: honeypot, kippo, mysql, netstat, nmap, ubuntu
Slug: kippo-probando-un-honeypot-en-ubuntu

Un _honeypot_ emula un servicio vulnerable, en caso de [Kippo][] el de
SSH pero los hay también para otros servicios como FTP o web, con el fin
de registrar la interacción del atacante. De esta manera, se puede tener
constancia de la técnica y el tipo de ataques que se llevan a cabo. El
_honeypot_ puede ser de baja interacción, si emula un servicio no
existente, o de alta interacción, si trabaja sobre un servicio real.
Kippo es de los primeros.


Instalación y configuración
---------------------------

Antes de instalarlo en Ubuntu, instalaremos las dependencias:

```bash
$ sudo aptitude install python-twisted
```

Creamos un usuario y una base de datos en MySQL para guardar los
ataques:

```bash
$ mysql -uroot -p
mysql> CREATE DATABASE kippo;
mysql> CREATE USER 'kippo'@'localhost' IDENTIFIED BY 'password';
mysql> GRANT ALL PRIVILEGES ON kippo.* TO 'kippo'@'localhost';
mysql> FLUSH PRIVILEGES;
```

Crearemos un usuario sin privilegios en el sistema para ejecutar el
_honeypot_:

```bash
$ sudo adduser kippo
```

Cambiamos de usuario:

```bash
$ su kippo
```

Descargamos el código y lo descomprimimos:

```bash
kippo$ cd
kippo$ wget http://kippo.googlecode.com/files/kippo-0.5.tar.gz
kippo$ tar -xvzf kippo-0.5.tar.gz
kippo$ cd kippo-0.5
```

En este directorio podemos encontrar:

-   `dl/`: donde se guarda los ficheros descargados mediante `wget`
-   `log/kippo.log`: donde se guarda información de uso y depuración
-   `log/tty/`: _logs_ de las sesiones
-   `utils/playlog.py`: herramienta para reproducir los _logs_ de sesión
-   utils/createfs.py: utilizado para crear `fs.pickle`
-   fs.pickle: falso sistema de ficheros
-   honeyfs/: contenido del falso sistema de ficheros. Aquí podemos
    poner una copia de un sistema real.
-

Creamos la estructura de la base de datos mediante el _script_
proporcionado:

```bash
kippo$ mysql -ukippo -p -D kippo < ./doc/sql/mysql.sql
```

Añadimos la configuración de MySQL al final del archivo de configuración
de Kippo, `kippo.cfg`:

```bash
[database_mysql]
host = localhost
database = kippo
username = kippo
password = password
```

Para arrancar el _honeypot_:

```bash
kippo$ ./start.sh
Starting kippo in background...Loading dblog engine: mysql
Generating RSA keypair...
done.
```

Controlando la actividad
------------------------

Podemos comprobar que el _honeypot_ está a la escucha ejecutando:

```bash
$ sudo netstat -atnp | grep 2222
tcp        0      0 0.0.0.0:2222            0.0.0.0:*               ESCUCHAR    6800/python
```

Podemos hacer las primeras pruebas desde la máquina local. El usuario es
`root` y la contraseña `123456`:

```bash
$ ssh -l root -p 2222 localhost
```

Para ver las últimas 10 contraseñas utilizadas:

```bash
$ mysql -u kippo -p -D kippo -e "select * from auth order by timestamp desc limit 10;"
+-----+----------------------------------+---------+----------+------------------------------+---------------------+
| id  | session                          | success | username | password                     | timestamp           |
+-----+----------------------------------+---------+----------+------------------------------+---------------------+
| 153 | 7258df989e6d11e1be4f00030d3cf419 |       0 | root     | rk08xvx12!                   | 2012-05-15 09:07:51 |
| 152 | 70c8b7e89e6d11e1be4f00030d3cf419 |       0 | root     | bufusimata                   | 2012-05-15 09:07:49 |
| 151 | 6f30e1949e6d11e1be4f00030d3cf419 |       0 | root     | murgu123                     | 2012-05-15 09:07:46 |
| 150 | 6d9fe3529e6d11e1be4f00030d3cf419 |       0 | root     | iamana                       | 2012-05-15 09:07:43 |
| 149 | 6c10533c9e6d11e1be4f00030d3cf419 |       0 | root     | pulamea1985                  | 2012-05-15 09:07:41 |
| 148 | 6a8135a49e6d11e1be4f00030d3cf419 |       0 | root     | Zpfljk,fkczddjlbnm'njnGFHJKM | 2012-05-15 09:07:38 |
| 147 | 68e833509e6d11e1be4f00030d3cf419 |       0 | root     | yachTicDokdipow              | 2012-05-15 09:07:35 |
| 146 | 675810649e6d11e1be4f00030d3cf419 |       0 | root     | Y88..88P                     | 2012-05-15 09:07:33 |
| 145 | 65c925449e6d11e1be4f00030d3cf419 |       0 | root     | ~X4CK3R                      | 2012-05-15 09:07:30 |
| 144 | 6439d5849e6d11e1be4f00030d3cf419 |       0 | root     | vK94                         | 2012-05-15 09:07:28 |
+-----+----------------------------------+---------+----------+------------------------------+---------------------+
10 rows in set (0.01 sec)
```

Una opción interesante es reproducir la sesión de un usuario mediante el
_script_ `playlog.py`. Por ejemplo:

```bash
$ python utils/playlog.py -b -m 2 log/tty/20120513-141543-2892.log 0
```

Acceso desde el exterior
------------------------

El _honeypot_ se ejecuta en el puerto 2222, por defecto, por lo que
deberemos crear una redirección desde el puerto 22 (para que se
ejecutase en el puerto 22 debería tener privilegios de administrador, y
esto es algo que no queremos). Para redirigir el puerto podemos utilizar
la NAT del _router_, o utilizar `iptables` si queremos que a redirección
se lleve a cabo en el propio equipo:

```bash
$ iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 22 -j REDIRECT--to-port 2222
```

Si estamos utilizando algún tipo de cortafuegos, por ejemplo `ufw`,
deberemos crear una regla para permitir el acceso:

```bash
$ sudo ufw allow 2222
```

Para comprobar que se puede establecer la conexión podemos utilizar
`nmap`:

```bash
$ nmap -PN -sV -p 2222 192.168.50.75
Starting Nmap 5.21 ( http://nmap.org ) at 2012-05-13 14:12 CEST
Nmap scan report for terminus (192.168.50.75)
Host is up (0.0018s latency).
PORT     STATE SERVICE VERSION
2222/tcp open  ssh     OpenSSH 5.1p1 Debian 5 (protocol 2.0)
Service Info: OS: Linux
```

Referencias
-----------

- [Kippo][]
- [Installing kippo on a ubuntu system][]
- [Instalando kippo, un honeypot SSH][]
- [kippo honeypot on ubuntu 10.04][]

  [Kippo]: http://code.google.com/p/kippo/
    "Kippo"
  [Installing kippo on a ubuntu system]: http://www.syderoxylon.com/?p=159
    "Installing kippo on a ubuntu system"
  [Instalando kippo, un honeypot SSH]: http://dysloke.com/blog/?p=836
    "Instalando kippo, un honeypot SSH"
  [kippo honeypot on ubuntu 10.04]: http://hackertarget.com/kippo-honeypot-on-ubuntu-10-04/%20
    "kippo honeypot on ubuntu 10.04"

Title: Conexión inalámbrica en Raspbmc
Date: 2012-07-03 03:33
Author: Nacho Cano
Tags: concentrador, hub usb, ip dinámica, ip fija, iwconfig, iwlist, network-manager, nmcli, opendns, powered hub, raspberry pi, raspbmc, wifi, wireless, wpa_supplicant, wpa2, xbmc, zydas
Slug: conexion-inalambrica-en-raspbmc
Related: raspbmc,raspberry-pi,arch-en-raspberry-pi

[El otro día][] me quedé sin poder probar la conexión inalámbrica en
Raspbmc porque los puertos USB de la Raspberry Pi no dan suficiente
potencia para la antena WiFi USB que tengo. Cada puerto USB proporciona
hasta 100mA, y parece que [el consumo de la antena][] oscila entre 150mA
y 200mA, por lo que no es suficiente. Quizá conectando un cable USB en Y
desde los dos USB podría llegar a funcionar, pero nos quedaríamos sin
puertos USB libres.

Una solución que funciona es utilizar un concentrador (o _hub_) USB con
alimentación externa. Además, podemos conectar la alimentación de la
Raspberry Pi al concentrador, por lo que no necesitaremos dos enchufes.

Configurar una conexión inalámbrica en Raspbmc con una antena WiFi USB
es parecido a lo que hay que hacer para [configurarla en debian][], pero
como Raspbmc utiliza Network Manager, la configuraremos a través de
éste.

La antena que tengo es una Conceptronic CT-WN4320Z con chip ZD1211 y que
funciona con el controlador ZyDAS. Dado que el _firmware_ para este chip no
es libre, deberemos habilitar los repositorios `non-free` editando el
fichero `/etc/apt/sources.list`:


```bash
deb http://ftp.debian.org/debian stable main non-free
deb http://ftp.debian.org/debian/ squeeze-updates main non-free
deb http://security.debian.org/ squeeze/updates main non-free
```

Actualizamos los repositorios:

```bash
$ sudo aptitude update
```

Instalamos el controlador `zd1211-firmware`:

```bash
$ sudo aptitude install zd1211-firmware
```

Los siguientes paquetes puede que no sean estrictamente necesarios, pero
si queremos ejecutar comandos como `lsusb`, `iwconfig`, `iwlist`,
`wpa_supplicant`, etc. los vamos a necesitar. El paquete `wpasupplicant`
lo he instalado porque he estado probando la conexión antes de hacerlo a
través de Network Manager. Para instalarlos:

```bash
$ sudo aptitude install usbutils wireless-tools wpasupplicant
```

Vamos al directorio `/etc/NetworkManager/system-connections`, o lo
creamos si no existía, y creamos el fichero `wlan0`:

```bash
[connection]
id=wlan0
uuid=11111111-1111-1111-1111-111111111111
type=802-11-wireless
autoconnect=true
timestamp=0

[802-11-wireless]
ssid=77;89;83;83;73;68;
mode=infrastructure
security=802-11-wireless-security

[802-11-wireless-security]
key-mgmt=wpa-psk
psk=very long long password

[ipv4]
method=manual
dns=208.67.222.222;208.67.220.220;
addresses1=192.168.50.2;24;192.168.50.1;

[ipv6]
method=ignore
```

El fichero es bastante explicativo. De esta manera se configura una
conexión con cifrado WPA2 e IP fija. A destacar:

-   El identificador de la conexión `id` no tiene por qué ser el nombre
    de la interfaz, pero así es fácil identificarla.
-   El `uuid` debe ser único para todas las conexiones.
-   El SSID debe convertirse al valor decimal de los caracteres en ASCII
    separados por punto y coma. Por ejemplo, si el SSID es MYSSID,
    podemos ejecutar
    `python -c "print ';'.join(str(ord(c)) for c in 'MYSSID')+';'"` lo
    que nos devuelve `77;89;83;83;73;68;`. El punto y coma del final es
    importante.
-   La frase de paso, que se especifica en `psk`, no es necesario
    ponerla entre comillas aunque contenga espacios.
-   Los DNS son los de OpenDNS.
-   La dirección IP asignada es `192.168.50.2`, la máscara de red `24`,
    es decir, `255.255.255.0` y la puerta de enlace `192.168.50.1`.

Si en lugar de IP fija queremos usar DHCP, sustituimos la sección
`[ipv4]` por:

```bash
[ipv4]
method=auto
dhcp-client-id=xbmc
dhcp-hostname=xbmc
```

Una vez que hemos terminado de editar el fichero, le cambiamos los
permisos:

```bash
$ sudo chmod 600 /etc/NetworkManager/system-connections/wlan0
```

Esto es importante, porque si el fichero no tiene las restricciones de
usuario y permisos, Network Manager lo ignorará.

Mediante el siguiente comando levantamos la conexión:

```bash
$ nmcli con up id wlan0
```

Eso, o reiniciamos la Raspberry Pi.

Como curiosidad, podemos [consultar el UUID][] de las conexiones activas
ejecutando:

```bash
$ nmcli con status
NAME                      UUID                                   DEVICES    SCOPE    DEFAULT  VPN
wlan0                     11111111-1111-1111-1111-111111111111   wlan0      system   yes      no
```

O listar todas las conexiones con:

```bash
$ nmcli con list
NAME                      UUID                                   TYPE              SCOPE    TIMESTAMP-REAL
wlan0                     11111111-1111-1111-1111-111111111111   802-11-wireless   system   Tue Jul  2 21:08:07 2012
Auto eth0                 9ab5123b-s912-5215-cad2-b98fe521592d   802-3-ethernet    system   Mon Jul  2 20:48:03 2012
NAME                      UUID                                   TYPE              SCOPE    TIMESTAMP-REAL
```

Referencias
-----------

» [Configuring a NetworkManager Wireless Connection without Graphics][]

  [El otro día]: {filename}/admin/raspbmc.md
    "El otro día"
  [el consumo de la antena]: https://help.ubuntu.com/community/WifiDocs/Driver/zydas_zd1211
    "el consumo de la antena"
  [configurarla en debian]: http://terminus.ignaciocano.com/k/2012/06/21/raspberry-pi#conexion-inalambrica-con-una-antena-wifi-usb
    "configurarla en debian"
  [consultar el UUID]: http://askubuntu.com/questions/14195/get-uuid-of-specific-connection
    "consultar el UUID"
  [Configuring a NetworkManager Wireless Connection without Graphics]: http://newton.cx/~peter/work/?p=409
    "Configuring a NetworkManager Wireless Connection without Graphics"

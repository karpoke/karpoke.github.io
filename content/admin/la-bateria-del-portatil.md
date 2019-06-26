Title: La batería del portátil
Date: 2010-09-26 00:10
Author: Nacho Cano
Tags: acpi, acpitool, awk, capacidad de la bateria, cron, notify-send, script, temperatura, vida de la batería
Slug: la-bateria-del-portatil

Algunos [falsos mitos de las baterías del portátil][]:

-   Es necesario que se agote la batería para ponerla a cargar,
-   no se debe dejar el portátil siempre enchufado a la corriente,
-   ni se debe suspender conectado a la corriente.

También existen técnicas para [alargar la vida de la batería][]:

1.  enchufa el portátil (y enciéndelo, si quieres) hasta que la batería
    este cargada y déjalo cargando 2 horas más,
2.  desenchufa el portátil y espera a que se gaste la batería e hiberne
3.  enchufa el portátil sin encenderlo hasta que se cargue la batería
4.  realizar estas operaciones cada 2 ó 3 meses

En principio, las baterías de los portátiles _ya_ incorporan un
mecanismo que corta la corriente cuando éstas están totalmente cargadas,
evitando así la fatiga por la carga continua.

De todas formas, he pensado que sería buena idea obtener un aviso cuando
la batería ha terminado de cargarse, por si aún así queremos desenchufar
el portátil de la corriente.

Dentro del directorio `/proc/acpi/battery/BAT0` hay unos ficheros que
contienen información del estado de la batería:

```bash
$ cat /proc/acpi/battery/BAT0/state
present:                 yes
capacity state:          ok
charging state:          charged
present rate:            unknown
remaining capacity:      1065 mAh
present voltage:         12462 mV
```

```bash
$ cat /proc/acpi/battery/BAT0/info
present:                 yes
design capacity:         4400 mAh
last full capacity:      1130 mAh
battery technology:      rechargeable
design voltage:          12414 mV
design capacity warning: 113 mAh
design capacity low:     56 mAh
capacity granularity 1:  35 mAh
capacity granularity 2:  8 mAh
model number:            M50EA0
serial number:           00001
battery type:            LiOn
OEM info:                OEM
```

Podemos utilizar esta información para escribir un pequeño _script_ que
compruebe si la batería está cargando o si ya ha terminado:

```bash
$ if [[ -n "$(awk /charged/'{print $3}' /proc/acpi/battery/BAT0/state)" ]]; then
>    export DISPLAY=:0.0
>    notify-send -u critical --icon=gtk-dialog-error "Unplug the AC power"
> fi
```

Luego podemos meter esto en el _script_ [check-battery-status.sh][] y
añadirlo al `cron` para que lo ejecute regularmente, por ejemplo, cada 5
minutos:

```bash
$ */5 * * * * /home/user/check-battery-status.sh
```

En lugar de examinar el fichero `/proc/acpi/battery/BAT0/state`
directamente, podemos utilizar algunos comandos que nos muestran esta
información de diferentes formas, ya sea mostrando información relativa
a un aspecto concreto, o ampliando dicha información. Por ejemplo, el
comando `acpitool`:

```bash
$ acpitool  -h
 Usage: acpitool [option] . . .
 Shows ACPI information from the /proc/acpi filesystem, like battery status,
 temperature, or ac power. Can also suspend your machine (if supported).

   -a, --ac_adapter   AC adapter information
   -A, --Asus         show supported Asus ACPI extensions (LCD brightness level, video out routing DSTD/acpi4asus info)
   -b                 battery status, available batteries only
   -B, --battery      battery status, all info on all battery entries
   -c, --cpu          CPU information (type, speed, cache size, frequency scaling, c-states, . . .)
   -e                 show just about everything
   -f, --fan          show fan status
   -F x               force fan on (x=1) or switch back to auto mode (x=0). (Toshiba only)
   -h, --help         show this help screen
   -j                 eject ultrabay device (Thinkpad only)
   -l x               set LCD brightness level to x, where x is 0..7 (Toshiba and Thinkpad only)
   -m x               switch the mail led on (x=1) or off (x=0) (Asus only)
   -n x               switch the wireless led on (x=1) or off (x=0). (Asus only)
   -o x               set LCD on (x=1) or off (x=0). (Asus only)
   -s, --suspend      suspend to memory (sleep state S3), if supported
   -S                 suspend to disk (sleep state S4), if supported
   -t, --thermal      thermal information, including trip_points
   -T, --Toshiba      show supported Toshiba ACPI extensions (LCD brightness level, video out routing, fan status)
   -v                 be more verbose (more detailed error messages, only usefull combined with other options)
   -V, --version      show application version number and release date
   -w, --wakeup       show wakeup capable devices
   -W x               enable/disable wakeup capable device x. The x can be seen when invoking -w first.
   -z x               set Asus LCD brightness level to x, where x is 0..15 (Asus only).

 If invoked without options, acpitool displays information about available batteries,
 AC adapter and thermal information.

 For more info, type man acpitool at the prompt.

 AcpiTool v0.5.1, released 13-Aug-2009
 Homepage: http://freeunix.dyndns.org:8000/site2/acpitool.shtml
```

Con el argumento `-B` nos muestra el porcentaje de capacidad perdida de la
batería. La mía ya está agonizando:

```bash
$ acpitool  -B
  Battery #1     : present
    Remaining capacity : 887 mWh, 100.0%, 00:00:00
    Design capacity    : 5200 mWh
    Last full capacity : 887 mWh, 17.06% of design capacity
    Capacity loss      : 82.94%
    Present rate       : 1 mW
    Charging state     : charged
    Battery type       : non-recharge
    Model number       : 0 mWh
    Serial number      : Dell
```

Otro comando es `acpi`, que hace más o menos lo mismo:

```bash
$ acpi -h
Usage: acpi [OPTION]...
Shows information from the /proc filesystem, such as battery status or
thermal information.

  -b, --battery     battery information
  -i, --details     show additional details if available:
                - battery capacity information
                - temperature trip points
  -a, --ac-adapter      ac adapter information
  -t, --thermal     thermal information
  -c, --cooling     cooling information
  -V, --everything      show every device, overrides above options
  -s, --show-empty      show non-operational devices
  -f, --fahrenheit      use fahrenheit as the temperature unit
  -k, --kelvin          use kelvin as the temperature unit
  -d, --directory  path to ACPI info (/sys/class resp. /proc/acpi)
  -p, --proc            use old proc interface instead of new sys interface
  -h, --help            display this help and exit
  -v, --version     output version information and exit

By default, acpi displays information on installed system batteries.
Non-operational devices, for example empty battery slots are hidden.
The default unit of temperature is degrees celsius.

Report bugs to Michael Meskes .
```

```bash
$ acpi
Battery 0: Charging, 38%, 00:28:05 until charged
```

```bash
$ acpi -a
Adapter 0: on-line
```

Con `acpi` también podemos controlar la temperatura.

```bash
$ acpi -t
Thermal 0: ok, 58.0 degrees C
Thermal 1: ok, 60.0 degrees C
Thermal 2: ok, 72.0 degrees C
```

  [falsos mitos de las baterías del portátil]: http://www.macoteca.com/falsos-mitos-de-las-baterias/90/
    "falsos mitos de las baterías del portátil"
  [alargar la vida de la batería]: http://www.macoteca.com/rejuvenece-la-bateria-de-tu-portatil/94/
    "alargar la vida de la batería"
  [check-battery-status.sh]: http://terminus.ignaciocano.com/wp-uploads/linked/check-battery-status.sh
    "check-battery-status.sh"

Title: El consumo de la batería
Date: 2011-10-01 19:55
Author: Nacho Cano
Tags: ahorro energético, ASPM, grub, kernel, powertop, vida de la batería
Slug: el-consumo-de-la-bateria

Con las últimas versiones del _kernel_ el [consumo de la batería se
había disparado][], reduciendo el tiempo de vida útil de la batería. Las
baterías son un bien preciado, por lo que existen multitud de trucos
para intentar [alargar su tiempo de vida][].

Aunque no se conoce con certeza si [este elevado consumo podría deberse
a un fallo][], en los casos en que la BIOS indicaba que ASPM no estaba
soportado estando éste habilitado, o a la configuración en algunos
[parámetros del _kernel_][parámetros del kernel].


Configuración del _kernel_
--------------------------

Entre estos parámetros se encuentran:

-   `dirty_writeback_centisecs`, que indica las centésimas entre
    despertares de `pdflush` para escribir datos en disco y tiene un
    valor por defecto de 500, lo cual es óptimo para el rendimiento pero
    no para la vida de la batería. El parámetro no cambia
    automáticamente cuando desconectamos el portátil de la corriente.
-   `nmi_watchdog`, sirve para generar [interrupciones no
    enmascarables][] (NMI). Se puede utilizar para depurar el _kernel_.
    Ejecutando NMI periódicas, el _kernel_ puede monitorizar _locks_ en
    cualquier CPU.
-   `sched_smt_power_savings`, se utiliza para [controlar la potencia de
    la CPU][]. Bajo condiciones de poca carga, y si la política de
    ahorro energético está habilitada, el planificador minimiza el
    número de núcleos que ejecutan dicha carga, ahorrando energía a
    costa del rendimiento.
-   `snd_hda_intel/parameters/power_save`, especifica el número de
    segundos tras los cuales el [módulo de sonido][] se deshabilita.

        $ cat /sys/module/snd_hda_intel/parameters/power_save
    0

  [consumo de la batería se había disparado]: http://www.phoronix.com/scan.php?page=article&item=linux_mobile_uffda#=1
    "consumo de la batería se había disparado"
  [alargar su tiempo de vida]: {filename}/admin/la-bateria-del-portatil.md
    "la batería del portátil"
  [este elevado consumo podría deberse a un fallo]: http://elsoftwarelibre.wordpress.com/2011/09/29/el-elevado-consumo-de-energia-de-las-ultimas-versiones-del-kernel-de-linux-%C2%BFverdad-o-mito/
    "este elevado consumo podría deberse a un fallo"
  [parámetros del kernel]: http://www.fewt.com/2011/09/about-kernel-30-power-regression-myth.html
    "parámetros del kernel"
  [interrupciones no enmascarables]: http://www.mjmwired.net/kernel/Documentation/nmi_watchdog.txt
    "interrupciones no enmascarables"
  [controlar la potencia de la CPU]: http://lwn.net/Articles/186469/
    "controlar la potencia de la CPU"
  [módulo de sonido]: http://www.thinkwiki.org/wiki/How_to_enable_audio_codec_power_saving
    "módulo de sonido"

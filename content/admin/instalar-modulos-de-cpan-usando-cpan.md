Title: Instalar módulos de CPAN usando CPAN
Date: 2011-07-22 02:45
Author: Nacho Cano
Tags: aptitude, cpan, local::lib, módulos, perl
Slug: instalar-modulos-de-cpan-usando-cpan

Una de las razones para querer instalar módulos del repositorio CPAN de
Perl utilizando, a su vez, el módulo `cpan`, es que los módulos están
más actualizados que en los paquetes de los repositorios. Para
conseguirlo, podemos seguir los siguientes pasos

Necesitamos tener instalado el paquete `build-essential`. Lanzamos la
consola CPAN, con [privilegios de administrador][]:

```bash
$ sudo perl -MCPAN -e shell
```

o también podríamos ejecutar:

```bash
$ sudo cpan
```

Si no tuviéramos permisos, parece que también es posible [instalar
módulos de Perl sin tener privilegios de administrador][], mediante el
módulo `local::lib`.

Una vez en la consola CPAN, el comando `help` nos muestra información
acerca de varios comandos disponibles.

```bash
cpan> help

Display Information                                                (ver 1.9600)
 command  argument          description
 a,b,d,m  WORD or /REGEXP/  about authors, bundles, distributions, modules
 i        WORD or /REGEXP/  about any of the above
 ls       AUTHOR or GLOB    about files in the author's directory
    (with WORD being a module, bundle or author name or a distribution
    name of the form AUTHOR/DISTRIBUTION)

Download, Test, Make, Install...
 get      download                     clean    make clean
 make     make (implies get)           look     open subshell in dist directory
 test     make test (implies make)     readme   display these README files
 install  make install (implies test)  perldoc  display POD documentation

Upgrade
 r        WORDs or /REGEXP/ or NONE    report updates for some/matching/all modules
 upgrade  WORDs or /REGEXP/ or NONE    upgrade some/matching/all modules

Pragmas
 force  CMD    try hard to do command  fforce CMD    try harder
 notest CMD    skip testing

Other
 h,?           display this menu       ! perl-code   eval a perl command
 o conf [opt]  set and query options   q             quit the cpan shell
 reload cpan   load CPAN.pm again      reload index  load newer indices
 autobundle    Snapshot                recent        latest CPAN uploads
```

Ahora, seguimos los siguientes [pasos][]. Ejecutamos:

```bash
cpan> make install
```

Actualizamos nuestro CPAN:

```bash
cpan> install Bundle::CPAN
```

[Recargamos][]:

```bash
cpan> reload cpan
(CPAN.....................................v1.9600)
(CPAN::Author..........v5.5001)
(CPAN::CacheMgr.........v5.5001)
(CPAN::Complete......v5.5)
(CPAN::Debug.v5.5001)
(CPAN::DeferredCode.v5.50)
(CPAN::Distribution................................................................................v1.9602)
(CPAN::Distroprefs..................................................v6)
(CPAN::Distrostatus......v5.5)
(CPAN::Exception::RecursiveDependency..v5.5)
(CPAN::Exception::yaml_not_installed....v5.5)
(CPAN::FTP..................v5.5005)
(CPAN::FTP::netrc.....v1.01)
(CPAN::HandleConfig..............v5.5003)
(CPAN::Index...........v1.9600)
(CPAN::InfoObj..........v5.5)
(CPAN::LWP::UserAgent...v1.9600)
(CPAN::Module...................................v5.5001)
(CPAN::Prompt..v5.5)
(CPAN::Queue............v5.5001)
(CPAN::Shell...............................................................v5.5002)
(CPAN::Tarzip...........v5.5011)(CPAN::Version........v5.5001)
398 subroutines redefined


cpan shell -- CPAN exploration and modules installation (v1.9600)
Enter 'h' for help.
```

Y ya podemos instalar cualquier módulo, por ejemplo:

```bash
cpan> install IO::Pty::Easy
Running install for module 'IO::Pty::Easy'
Running make for D/DO/DOY/IO-Pty-Easy-0.08.tar.gz
```

Para terminar la sesión:

```bash
cpan> exit
Lockfile removed.
```

Si queremos eliminar todos los módulos instalados basta con ejecutar:

```bash
$ rm -fr ~/.cpan
```

Las librerías de CPAN en los respositorios
------------------------------------------

Si queremos [instalar las librerías usando el gestor de paquetes][]:

```bash
$ echo "XML::Simple" | perl -e '$x=<>; chomp($x); $x=~s/::/-/; $x=lc($x); print "lib$x-perl"' | xargs aptitude install
```

Este comando obtiene el nombre de la librería de los repositorios que
contiene el módulo XML::Simple, convirtiendo el nombre del módulo a
minúsculas, reemplazando los "::" por "-" y añadiendo el prefijo "lib".

  [privilegios de administrador]: http://www.troubleshooters.com/codecorn/littperl/perlcpan.htm
    "privilegios de administrador"
  [instalar módulos de Perl sin tener privilegios de administrador]: http://perl.jonallen.info/writing/articles/install-perl-modules-without-root
    "instalar módulos de Perl sin tener privilegios de administrador"
  [pasos]: http://egoleo.wordpress.com/2008/05/19/how-to-install-perl-modules-through-cpan-on-ubuntu-hardy-server/
    "pasos"
  [Recargamos]: http://twiki.org/cgi-bin/view/TWiki/HowToInstallCpanModules#Install_CPAN_modules_into_your_l
    "Recargamos"
  [instalar las librerías usando el gestor de paquetes]: http://www.deepakg.com/prog/2009/01/cpan-modules-on-ubuntu-apt-get-vs-perl-mcpan/
    "instalar las librerías usando el gestor de paquetes"

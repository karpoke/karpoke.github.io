Title: Conectarse por SSH utilizando sshpass
Date: 2013-06-09 15:47
Author: Nacho Cano
Tags: contraseña, ssh, sshpass
Slug: conectarse-por-ssh-utilizando-sshpass
Related: conectarse-por-ssh-utilizando-expect,conectarse-por-ssh-solo-usando-la-clave,servicio-de-ssh-con-sistema-de-verificacion-en-dos-pasos-de-google-en-ubuntu-natty-narwhal,evitar-el-registro-de-comandos-en-el-historial,fwknop-single-packet-authorization-y-port-knocking,sslh-compartiendo-el-puerto-443,detectando-intrusos-en-ubuntu-maverick-meerkat

`sshpass` es un programa que nos permite iniciar sesión en un servidor
SSH de forma no interactiva y sin utilizar claves, para lo que deberemos
proporcionar la contraseña como argumento del programa.

Para conectar a un servidor SSH, es preferible [utilizar claves][],
además de tener en cuenta otros sistemas de seguridad, como la
[autenticación en dos pasos][], pero puede haber escenarios en los que
`sshpass` sea una alternativa a considerar.

Su uso es sencillo:

```bash
$ sshpass -p password ssh example.com
```

El hecho de que la contraseña se escriba directamente en el terminal,
además de que es posible que [quede escrita en el historial][], podría
hacer que fuese visible al ejecutar otro usuario el comando `ps`. Sin
embargo, `sshpass` se encarga de sustituir la contraseña por zetas:

```bash
$ ps a | grep sshpass
18998 pts/6    S+     0:00 sshpass -p zzzzzzzz ssh example.com
```

Referencias
-----------

» [sshpass: Login To SSH Server / Provide SSH Password Using A Shell
Script][]

  [utilizar claves]: {filename}/admin/conectarse-por-ssh-solo-usando-la-clave.md
    "utilizar claves"
  [autenticación en dos pasos]: {filename}/admin/servicio-de-ssh-con-sistema-de-verificacion-en-dos-pasos-de-google-en-ubuntu-natty-narwhal.md
    "autenticación en dos pasos"
  [quede escrita en el historial]: {filename}/admin/evitar-el-registro-de-comandos-en-el-historial.md
    "quede escrita en el historial"
  [sshpass: Login To SSH Server / Provide SSH Password Using A Shell Script]: http://www.cyberciti.biz/faq/noninteractive-shell-script-ssh-password-provider/
    "sshpass: Login To SSH Server / Provide SSH Password Using A Shell Script"

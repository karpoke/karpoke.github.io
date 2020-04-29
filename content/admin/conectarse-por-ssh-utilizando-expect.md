Title: Conectarse por SSH utilizando expect
Date: 2011-06-17 14:59
Author: Nacho Cano
Tags: clave pública, contraseña, expect, ftp, inicio de sesión, openssh, rsa, script, ssh
Slug: conectarse-por-ssh-utilizando-expect
Related: servicio-de-ssh-con-sistema-de-verificacion-en-dos-pasos-de-google-en-ubuntu-natty-narwhal,sslh-compartiendo-el-puerto-443,compartiendo-una-conexion-por-ssh,conectarse-por-ssh-solo-usando-la-clave

`expect` es un comando que "habla" con otros programas interactivos. Se
definen unas reglas en función de lo que esperamos que nos digan esos
programas y lo que queremos contestar.

Un típico ejemplo es realizar una conexión a un servicio de FTP o SSH, y
utilizar `expect` para que introduzca la contraseña por nosotros y lleve
a cabo diferentes acciones. La ventaja que tiene es que podemos
automatizar acciones en esos servicios. El gran inconveniente es que, si
esos servicios requieren autenticación, deberemos escribir la
contraseña, ya sea en un _script_ o directamente en el terminal,
pudiendo quedar reflejada en el historial. (Dependiendo de la
configuración, si incluimos espacios antes de ejecutar un comando, éste
no queda reflejado en el historial).


Conectarse a un servidor SSH y mostrar una consola interactiva
--------------------------------------------------------------

Aunque el resultado pueda ser similar a [conectarse utilizando la
clave][], ya que no nos pedirá contraseña, el nivel de seguridad es muy
diferente, no sólo por lo que ya hemos comentado, sino porque nuestra
contraseña seguramente es más débil que una clave RSA (de al menos 2048
bits). Siempre que sea posible, es preferible utilizar una clave para
conectarnos.

El siguiente _script_ [muestra cómo podemos conectarnos][] utilizando el
usuario y la contraseña escritos en el propio _script_:

    #!/usr/bin/env expect
    # http://ubuntuforums.org/showpost.php?p=5433300&postcount=5

    #trap sigwinch and pass it to the child we spawned
    trap {
     set rows [stty rows]
     set cols [stty columns]
     stty rows $rows columns $cols < $spawn_out(slave,name)
    } WINCH

    set username yourUserNameHere
    set pass yourPasswordHere
    set host theIpAddressToConnectTo

    spawn ssh ${username}@${host}

    expect -re "password:"
    send "${pass}\r"

    expect -re "$"

    # now interact with the session
    interact

Podríamos modificar el _script_ para que nos pida los parámetros, y
pasárselos como argumentos desde el terminal. Deberíamos cambiar las
líneas dónde se definen dichas variables por:

    set username [lrange $argv 0 0]
    set pass [lrange $argv 1 1]
    set host [lrange $argv 2 2]

Y desde el terminal, lo invocaríamos mediante:

    $ ./sshlogin.ssh username pass host

Conectarse a un servidor SSH, ejecutar un comando y salir
---------------------------------------------------------

Otra opción es que nos queramos [conectar para ejecutar un comando][],
ver el resultado y salir. Un sencillo _script_ que nos permite hacer
esto es el siguiente:

    #!/usr/bin/expect -f
    # http://bash.cyberciti.biz/security/expect-ssh-login-script/
    set user [lrange $argv 0 0]
    set ip_or_domain [lrange $argv 1 1]
    set password [lrange $argv 2 2]
    set scriptname [lrange $argv 3 3]
    set arg1 [lrange $argv 4 4]
    set timeout -1
    # now connect to remote UNIX box (ip_or_domain) with given script to execute
    spawn ssh $user@$ip_or_domain $scriptname $arg1

    match_max 100000
    # Look for passwod prompt
    expect "*?assword:*"
    # Send password aka $password
    send -- "$password\r"
    # send blank line (\r) to make sure we get back to gui
    send -- "\r"
    expect eof

Para ejecutarlo:

    $ ./sshlogin.exp user host pass who

La principal diferente entre estos dos _scripts_ es que, después de
enviar la contraseña, uno espera a que se muestre el _prompt_ para
iniciar una sesión interactiva mediante la orden `interact` y el otro
simplemente cierra la sesión.

Utilizar `expect` en el terminal
--------------------------------

También podríamos ejecutar `expect` directamente en el terminal de la
siguiente manera:

    $ expect -c "
       set password pass
       spawn ssh user@host who
       match_max 100000
       expect \"_?assword:_\"
       send -- \"${password}\r\"
       send -- \"\r\"
       expect eof
    "

  [conectarse utilizando la clave]: {filename}/admin/conectarse-por-ssh-solo-usando-la-clave.md
    "conectarse por ssh usando sólo la clave"
  [muestra cómo podemos conectarnos]: http://ubuntuforums.org/showpost.php?p=5433300&postcount=5
    "muestra cómo podemos conectarnos"
  [conectar para ejecutar un comando]: http://bash.cyberciti.biz/security/expect-ssh-login-script/
    "conectar para ejecutar un comando"

Title: Secuencias de escape en SSH
Date: 2011-06-18 19:44
Author: Nacho Cano
Tags: ssh
Slug: secuencias-de-escape-en-ssh

Secuencias de escape en SSH:

    user@remotehost:~$ ~?
    Supported escape sequences:
      ~.  - terminate connection (and any multiplexed sessions)
      ~B  - send a BREAK to the remote system
      ~C  - open a command line
      ~R  - Request rekey (SSH protocol 2 only)
      ~^Z - suspend ssh
      ~#  - list forwarded connections
      ~&  - background ssh (when waiting for connections to terminate)
      ~?  - this message
      ~~  - send the escape character by typing it twice
    (Note that escapes are only recognized immediately after newline.)

La primera, `~.`, se puede utilizar para [cerrar la sesión cuando se nos
queda colgada][], por ejemplo, al reiniciar la máquina remota.

Podemos hacer que nos muestre una consola:

    user@remotehost:~$ ~C
    ssh> help
    Commands:
        -L[bind_address:]port:host:hostport    Request local forward
        -R[bind_address:]port:host:hostport    Request remote forward
        -D[bind_address:]port                  Request dynamic forward
        -KR[bind_address:]port                 Cancel remote forward

O que nos muestre las conexiones abiertas:

    user@remotehost:~$ ~#
    The following connections are open:
    #1 client-session (t4 r0 i0/0 o0/0 fd 5/6 cc -1)

Si estamos [compartiendo una conexión SSH][], y nos conectamos desde
otro terminal, veremos algo parecido a esto:

    user@remotehost:~$ ~#
    The following connections are open:
    #1 client-session (t4 r0 i0/0 o0/0 fd 5/6 cc -1)
    #3 client-session (t4 r1 i0/0 o0/0 fd 9/10 cc 2)

  [cerrar la sesión cuando se nos queda colgada]: http://www.commandlinefu.com/commands/view/8665/control-ssh-connection
    "cerrar la sesión cuando se nos queda colgada"
  [compartiendo una conexión SSH]: {filename}/admin/compartiendo-una-conexion-por-ssh.md
    "compartiendo una conexión SSH"

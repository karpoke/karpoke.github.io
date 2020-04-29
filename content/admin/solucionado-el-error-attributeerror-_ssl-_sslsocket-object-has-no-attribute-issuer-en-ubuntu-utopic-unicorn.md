Title: Solucionado el error «AttributeError: '_ssl._SSLSocket' object has no attribute 'issuer'» en Ubuntu Utopic Unicorn
Date: 2015-02-03 00:50
Author: Nacho Cano
Tags: 14.10, patch, python-xmpp, ubuntu utopic unicorn, wget
Slug: solucionado-el-error-attributeerror-_ssl-_sslsocket-object-has-no-attribute-issuer-en-ubuntu-utopic-unicorn

Si al usar la librería de Python para XMPP nos aparece el error:

    Traceback (most recent call last):
      File "./test_xmpp.py", line 12, in
        cl.connect()
      File "/usr/lib/python2.7/dist-packages/xmpp/client.py", line 205, in connect
        while not self.TLS.starttls and self.Process(1): pass
      File "/usr/lib/python2.7/dist-packages/xmpp/dispatcher.py", line 303, in dispatch
        handler['func'](session,stanza)
      File "/usr/lib/python2.7/dist-packages/xmpp/transports.py", line 330, in StartTLSHandler
        self._startSSL()
      File "/usr/lib/python2.7/dist-packages/xmpp/transports.py", line 309, in _startSSL
        tcpsock._sslIssuer = tcpsock._sslObj.issuer()
    AttributeError: '_ssl._SSLSocket' object has no attribute 'issuer'

parece que es debido a un [fallo en dicha librería][].

La versión que viene en los repositorios es la 0.4.1:

    $ aptitude versions python-xmpp
    Paquete python-xmpp:
    i   0.4.1-cvs20080505.3build1                                 utopic                                 500

Afortunadamente, hay disponible un [parche][]:

    $ wget -P /tmp https://raw.githubusercontent.com/freebsd/freebsd-ports/master/net-im/py-xmpppy/files/patch-xmpp-transports.py
    $ sudo su
    # cd /usr/lib/python2.7/dist-packages/xmpp
    # patch < /tmp/patch-xmpp-transports.py
    patching file transports.py
    Hunk #2 succeeded at 305 (offset -7 lines).

  [fallo en dicha librería]: https://github.com/eventlet/eventlet/issues/124#issuecomment-68836258
    "fallo en dicha librería"
  [parche]: https://raw.githubusercontent.com/freebsd/freebsd-ports/master/net-im/py-xmpppy/files/patch-xmpp-transports.py
    "parche"

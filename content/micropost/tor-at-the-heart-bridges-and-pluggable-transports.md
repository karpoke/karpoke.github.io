Title: Tor at the heart: bridges and pluggable transports
Date: 2016-12-11 22:43
Author: Nacho Cano
Tags: Tor, censura, anonimato, protocolos ofuscados, repetidores anónimos
Slug: tor-at-the-heart-bridges-and-pluggable-transports

> Censors block Tor in two ways: they can block connections to the IP addresses
> of known Tor relays, and they can analyze network traffic to find use of the
> Tor protocol. Bridges are secret Tor relays—they don’t appear in any public
> list, so the censor doesn’t know which addresses to block. Pluggable
> transports disguise the Tor protocol by making it look like something
> else—for example like HTTP or completely random.
>
> There are several pluggable transports, and it can be hard to know which one
> to use. If it is your first time, try obfs4: it is a randomizing transport
> that works for most people. If obfs4 doesn’t work, try fte. If that doesn’t
> work, it may mean that the default bridges are blocked, and you should get a
> custom bridge from bridges.torproject.org. If the custom bridge doesn’t work,
> try meek-azure or meek-amazon.

» ssteele | [torproject.org][]

  [torproject.org]: https://blog.torproject.org/blog/tor-heart-bridges-and-pluggable-transports
    "Tor at the heart: bridges and pluggable transports"

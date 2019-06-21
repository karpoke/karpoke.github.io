Title: How Dropbox securely stores your passwords
Date: 2016-09-24 13:32
Author: Nacho Cano
Slug: how-dropbox-securely-stores-your-passwords

> It’s universally acknowledged that it’s a bad idea to store plain-text
> passwords. If a database containing plain-text passwords is compromised,
> user accounts are in immediate danger. For this reason, as early as 1976,
> the industry standardized on storing passwords using secure, one-way hashing
> mechanisms (starting with Unix Crypt). Unfortunately, while this prevents
> the direct reading of passwords in case of a compromise, all hashing
> mechanisms necessarily allow attackers to brute force the hash offline, by
> going through lists of possible passwords, hashing them, and comparing the
> result. In this context, secure hashing functions like SHA have a critical
> flaw for password hashing: they are designed to be fast. A modern commodity
> CPU can generate millions of SHA256 hashes per second. Specialized GPU
> clusters allow for calculating hashes at a rate of billions per second.

- Devdatta Akhawe | [blogs.dropbox.com][]

  [blogs.dropbox.com]: https://blogs.dropbox.com/tech/2016/09/how-dropbox-securely-stores-your-passwords/
    "How Dropbox securely stores your passwords"

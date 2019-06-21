Title: Unsafe cookies leave WordPress accounts open to hijacking, 2-factor bypass
Date: 2014-05-26 21:50
Author: Nacho Cano
Slug: unsafe-cookies-leave-wordpress-accounts-open-to-hijacking-2-factor-bypass

> Yan Zhu, a staff technologist at the Electronic Frontier Foundation,
> came to that determination after noticing that WordPress servers send
> a key browser cookie in plain text, rather than encrypting it, as long
> mandated by widely accepted security practices. The cookie, which
> carries the tag ”wordpress_logged_in,” is set once an end user has
> entered a valid WordPress user name and password. It’s the website
> equivalent of a plastic bracelets used by nightclubs. Once a browser
> presents the cookie, WordPress servers will usher the user behind a
> velvet rope to highly privileged sections that reveal private
> messages, update some user settings, publish blog posts, and more. The
> move by WordPress engineers to allow the cookie to be transmitted
> unencrypted makes them susceptible to interception in many cases.

- Dan Goodin | [arstechnica.com][]

  [arstechnica.com]: http://arstechnica.com/security/2014/05/unsafe-cookies-leave-wordpress-accounts-open-to-hijacking-2-factor-bypass/
    "Unsafe cookies leave WordPress accounts open to hijacking, 2-factor bypass"

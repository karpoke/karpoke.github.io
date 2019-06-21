Title: Why you should never use hash functions for message authentication
Date: 2012-06-27 23:54
Author: Ignacio Cano
Slug: why-you-should-never-use-hash-functions-for-message-authentication

> The general thrust of this post is: use a MAC function like HMAC to
> sign data, don’t use hash functions. Although not all hash functions
> suffer from the problem I’m going to illustrate, in general using a
> hash function for message authentication comes with a lot of potential
> problems because those functions aren’t designed for this task. You
> shouldn’t try to work around it by creatively processing the inputs or
> inventing some fancy way of chaining hash functions. Just use the
> functions that were designed for this task instead of inventing your
> own crypto schemes.

- [jcoglan.com][]

  [jcoglan.com]: http://blog.jcoglan.com/2012/06/09/why-you-should-never-use-hash-functions-for-message-authentication/
    "Why you should never use hash functions for message authentication"

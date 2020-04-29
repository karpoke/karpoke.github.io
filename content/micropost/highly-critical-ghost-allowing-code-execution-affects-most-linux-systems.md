Title: Highly critical “Ghost” allowing code execution affects most Linux systems
Date: 2015-02-06 16:11
Author: Nacho Cano
Slug: highly-critical-ghost-allowing-code-execution-affects-most-linux-systems

> The vulnerability in the GNU C Library (glibc) represents a major
> Internet threat, in some ways comparable to the Heartbleed and
> Shellshock bugs that came to light last year. The bug, which is being
> dubbed ”Ghost” by some researchers, has the common vulnerability and
> exposures designation of CVE-2015-0235. While a patch was issued two
> years ago, most Linux versions used in production systems remain
> unprotected at the moment. What’s more, patching systems requires core
> functions or the entire affected server to be rebooted, a requirement
> that may cause some systems to remain vulnerable for some time to
> come. The buffer overflow flaw resides in
> __nss_hostname_digits_dots(), a glibc function that’s invoked by
> the gethostbyname() and gethostbyname2() function calls. A remote
> attacker able to call either of these functions could exploit the flaw
> to execute arbitrary code with the permissions of the user running the
> application.

» Dan Goodin | [arstechnica.com][]

  [arstechnica.com]: http://arstechnica.com/security/2015/01/highly-critical-ghost-allowing-code-execution-affects-most-linux-systems/
    "Highly critical “Ghost” allowing code execution affects most Linux systems"

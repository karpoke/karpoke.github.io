Title: Demystifying the regular expression that checks if a number is prime
Date: 2016-09-10 18:02
Author: Nacho Cano
Slug: demystifying-the-regular-expression-that-checks-if-a-number-is-prime

> A while back I was researching the most efficient way to check if a number
> is prime. This lead me to find the following piece of code:
>
>     public static boolean isPrime(int n) {
>         return !new String(new char[n]).matches(”.?|(..+?)\\1+”);
>     }
>
> I was intrigued. While this might not be the most efficient way, it’s
> certainly one of the less obvious ones, so my curiosity kicked in. How on
> Earth could a match for the .?|(..+?)\1+ regular expression tell that a
> number is not prime (once it’s converted to its unary representation)?

» iluxonchik | [iluxonchik.github.io][]

  [iluxonchik.github.io]: https://iluxonchik.github.io/regular-expression-check-if-number-is-prime/
    "Demystifying the regular expression that checks if a number is prime"

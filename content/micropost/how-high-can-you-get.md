Title: How High Can You Get?
Date: 2013-03-20 01:21
Author: Nacho Cano
Slug: how-high-can-you-get

> So I wanted to find out: what exactly is the bug in the program that
> causes this behavior and also, can it be fixed?
>
> First I looked on the Internet to see if the answer has already been
> found. Some good starting information is located at
> http://www.jeffsromhack.com/products/donkeykong_tech.htm. There, Jeff
> Kulczycki breaks down the math of the kill screen, showing the formula
> that is used to compute the bonus for each level. The formula says the
> level times 10, plus 40, gives the number of hundreds in the bonus
> timer. If the result is too large it is forced back down. The key to
> this is that the level number is used in the calculation. On level 22
> an overflow occurs, leaving the player with just 400 points on the
> timer because the multiplication and addition yields a number larger
> than 256.

[!embed](https://www.youtube.com/watch?v=UmkhXdSC62w)

» Don Hodges | [donhodges.com][]

  [donhodges.com]: http://www.donhodges.com/how_high_can_you_get.htm
    "How High Can You Get?"

Title: Statistical functions in MySQL
Date: 2012-07-14 19:38
Author: Ignacio Cano
Slug: statistical-functions-in-mysql

> Even in times of a growing market of specialized NoSQL databases, the
> relevance of traditional RDBMS doesn’t decline. Especially when it
> comes to the calculation of aggregates based on complex data sets that
> can not be processed as a batch like Map&Reduce. MySQL is already
> bringing in a handful of aggregate functions that can be useful for a
> statistical analysis. The best known of this type are certainly:
>
> ```bash
> COUNT(x), SUM(x), AVG(x), MIN(x), MAX(x), STD(x)
> ```
>
> In addition, there are a number of statistical evaluations which are
> also worthwhile - if not even more interesting and meaningful, but
> with MySQL only producible with greater efforts. What about the
> different averages? The harmonic average, a weighted average or the
> geomean? What is in the course of this with the aggregate product? How
> do we determine the mode, the median? The covariance?
>
> In the following article I want to go to the bottom of these questions
> and develop a list of standard formulas for a statistical evaluation.
> Presumably the article is meant more for beginners. In addition, a few
> new features have been poured into my infusion UDF, which simplifies
> some of the calculations. You can check out the source of the UDF on
> Github:

- Robert Eisele | [xarg.org][]

  [xarg.org]: http://www.xarg.org/2012/07/statistical-functions-in-mysql/
    "Statistical functions in MySQL"

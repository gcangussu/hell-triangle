Hell Triangle
=============

Notes
-----
- If a function should be used for tests please use `hell_triangle.max_path_iterative()` as it is the most robust solution.
- This code uses the `typing` module available only from Python 3.5 and fowards, if you want to run it with versions below 3.5 install the `typing` module available on pypi or just remove the import statement and the aliases declarations. Then, everything should run as expected since annotations can be anything in Python.
- If you want to run it in Python 2.7 you'll need to provide a substitute to `functools.lru_cache()`. But beaware, I did not test this in Python 2.7.

The Problem
-----------
Find the maximum sum in a path of top to bottom in a triangle. The
movement from one element to the next is restricted to only the
nearest elements right below the previous element. Example:
```
   6
  3 5
 9 7 1
4 6 8 4
```
The maximum path is 6 + 5 + 7 + 8 = 26.

The Solution
------------
To solve this problem we can use a divide and conquer strategy. For
instance, if we have this triangle
```
 9
4 6
```
We can find the maximum path by comparing 4 and 6. So this triangle
would have a sum of `9 + max(4, 6)` wich yields 15. Then, if we get
a bigger triangle such as
```
  3
 9 8
4 6 8
```
We can first find the sum in the two smaller subtriangles. The one
in the left is the previous example and the one in the right is
`([8], [6, 8])` which max sum is `8 + max(6, 8)` that equals 16.
Then we can look at our triangle as the following:
```
  3
15 16
```
So if we choose to go left the maximum path there is 15, but if we 
choose right the path is 16. The optimal choice will be the path
that maximizes the total sum of the triangle, which in this case is 
the right path. So we can rewrite that as something like
```
3 + max(sum_at_left + sum_at_right)
```

Let's implement this. We are going to use Python 3.5. Python in general is a great language for implementing algorithms due to its high readability, what helps others understand your code, and because of its high expressiveness, what allows you to do more with less lines of code.

First we define our data type as aliases to the primitive types.
```python
from typing import Sequence

Row = Sequence[int]
Triangle = Sequence[Row]
```

To get the left and right triangles we define the function `split()` as
```python
from typing import Tuple

def split(tri: Triangle) -> Tuple[Triangle, Triangle]:
    """Return the left and right subtriangles as (left, right)."""
    left_right_pairs = ((row[:-1], row[1:]) for row in tri[1:])
    left, right = zip(*left_right_pairs)  # Unzip pairs
    return (left, right)
```
Note that if we discard the top element of the triangle we can get the left triangle by discarding the last element of each row. Similarly we can get the right triangle by discarding the first element of each row.

So the function to calculate the maximum sum can be defined as
```python
def max_path(tri: Triangle) -> int:
    """Return the maximum sum on a path from top to bottom."""
    if len(tri) == 1:
        return tri[0][0]

    left, right = split(tri)
    return tri[0][0] + max(max_path(left), max_path(right))
```
It first checks if the triangle is just a single element, a case that the maximum sum would be just itself. If not, it splits the triangle in left and right and returns the expression that will yield its maximum sum, which is its own value plus either the maximum sum of the left subtriangle or the right, whichever is larger.

This solution is very close to what we did by hand, but it is not very efficient. It took 75 seconds to get the max sum of a 25 rows triangle on my machine. This is a reality for two reasons. First it creates two new triangles with repetitive information for every call of the `split()` function. And also, it will recalculate a lot of identical function calls. For example, look at this triangle:
```
     0
    0 0
   0 6 0
  0 3 5 0
 0 9 7 1 0
0 4 6 8 4 0
```
Yes, it is the first triangle covered with zeros. The inner triangle topped by 6 is going to have its max sum calculated two times because of the zeros addition. This happens because on the first split we have these two:
```
  Left         Right
    0            0
   0 6          6 0
  0 3 5        3 5 0
 0 9 7 1      9 7 1 0
0 4 6 8 4    4 6 8 4 0
```
And worse, the subtriangles topped by 3 and 5 will be recalculated 4 times each, and its subtriangles even more times.

Well, so let's do a function that doesn't copy any information and also it is easy to implement a cache a lá dynamic programing.
```python
from functools import lru_cache

def max_path_cached(tri: Triangle) -> int:
    """Return the maximum sum on a path from top to bottom."""
    last_row_index = len(tri) - 1

    @lru_cache(maxsize=None)  # Avoid repetitive calculations
    def max_path_from(i: int, j: int) -> int:
        """Return the maximum possible sum from subtriangle [i][j]."""
        if i < last_row_index:
            left = max_path_from(i + 1, j)
            right = max_path_from(i + 1, j + 1)
            return tri[i][j] + max(left, right)
        return tri[i][j]

    return max_path_from(0, 0)
```
This function defines a constant of the triangle's `last_row_index`,defines another function called `max_path_from()` and return it with parameters `i=0, j=0`. Note that this last function have access to `last_row_index` and the `tri` parameter. The `max_path_from()` function returns the maximum sum of the subtriangle that starts at the row `i` and column `j`. It works by same principle of the previous algorithm, but navigates the triangle with indices to prevent copying and facilitate the caching. First it goes to the left on the triangle, untill it reaches a last row element, which the sum is istself. Then it goes back one stack frame and it will have the value for the left variable. Following, it will get the value for the right subtriangle, return its maximum path and go back a stack frame again. And so on. This and more would correspond to something like
```
  3          3          3        19
 9 8   =>  15 8   =>  15 16  =>  
4 6 8        6 8
```
By using the indices, which are hashable objects, we can use the `functools.lru_cache()` decorator to avoid repetitive calculations. The decorator works by saving the results for a given function call in a dictionary where the key is the call parameters and the value is the result. When the decorated function is called it will be checked for an entry in the dictionary with the same parameters, if it exists the value is returned right away, if not it is calculated as defined by the original function.

So let's compare `max_path_cache()` with `max_path()`. With the same triangle of 25 rows the cached function finishes in 0.001 seconds, 75000 times faster than oldie `max_path()`. `max_path_from()` is called 325 times to solve this triangle, where `max_path()` is called astonishing 33554431 times, the cache greatly reduces the number of calls.

The `max_path_cache()` seems great, but it still have a problem. When used with very big triangles it will cause a `RecursionError: maximum recursion depth exceeded` exception. This exeption is to safe guard Python from a stack overflow, but this limit can be increased manualy with the `sys.setrecursionlimit()` function. But be aware, Python stack frames are not as small as in some purely functional programming languages and your memory is not infinite.

If that is a problem, one fast solution  is to implement an hybrid iterable-recursive algorithm that, for example, given a triangle with 1000 rows first calculates the maximum sum for each subtriangle at row 500. Then it could compose a new triangle with the original rows untill row 499 and the new row of maximum sums as the row 500. Then you would have a triangle of 500 rows that can be recursively solved.

Another solution is to implement an iterative algorithm. And that's what was done in `max_path_iterative()`.
```python
def max_path_iterative(tri: Triangle) -> int:
    """Return the maximum sum on a path from top to bottom."""
    below_max = (0,) * len(tri[-1])  # Initialize to a row of zeros
    for row in reversed(tri):
        acc_row = tuple(bm + r for bm, r in zip(below_max, row))
        below_max = tuple(max(acc_row[i - 1], acc_row[i])
                          for i in range(1, len(acc_row)))
    return acc_row[0]
```
To understand this algorithm let's view a inversed triangle:
```
4 6 8
 9 8
  3
```
Now we have single results in the first row, the max path of 4 is 4, of 6 is 6 and 8 is 8. In the second row we need to compare the two numbers above, chose the larger and sum with it. So, in the second row, the max sum for 9 is `9 + max(4, 6)` and for 8 is `8 + max(6, 8)`. Then we have
```
15 16
  3
```
And we would do `3 + max(15, 16)` to solve it. What we are doing repetitively is calculating the maximum of every first row adjacent values (or the last row adjacent values if you think in the not inversed triangle). So for row `[4, 6, 8]` this would be `[max(4, 6), max(6, 8)]` yielding `[6, 8]`. We then take each value and sum it with the number right below it (`[6+9, 8+8]`). And repeat like so
```
4 6 8     6 8
 9 8  =>  9 8  =>  15 16  =>  16  =>
  3        3         3         3      19
```
`max_path_iterative()` does just that. It iterates the triangle's row from last to first, for each row it sums the last adjacent maximuns (`below_max`) in variable `acc_row`, which is used to get the new adjacent maximuns. Note that we initialize `below_max` with zeros for the first iteration. In the end its returned the first and only element at the accumulated row.

To compare with `max_path_cached()` lets use a 100 rows triangle. The recursive and iterative consistently get results below 0.02 seconds, but its not clear who is fastest. The real diference comes from the 1000 rows triangle test. The iterative function does it below 0.5 seconds and the recursive gets you a `RecursionError: maximum recursion depth exceeded`.

All those functions are defined in the file `hell_triangle.py`.

Tests
-----
There are tests for the `hell_triangle.py`'s functions in the file `hell_triangle_test.py`. The tests were itended to be runed with `pytest`, but since it does not uses any auxiliary function from `pytest` it can be executed without `pytest`.

You can also use `mypy` or other static checker to test the typing of the code.

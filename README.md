rithm
=====

A language designed for processing, analyzing, and visualizing data[^1].

`rithm` has a number of features designed to make working with data easier:
- dataframes (a.k.a. data tables) are a _first class data type_.
- _algorithms_ provide a way to describe multi-step processes that is both _boilerplate free_ and _easy to debug and adapt_.

[^1]: *data* here refers to *tabular data*—that is, rows and columns, where every column has the same number of elements (i.e. rows) and every element of a given column is of the same type, but where different columns can have different types (i.e., not just matrices).

Why?
----

I created rithm because I was tired of using Pandas but didn't want to go back to using R.

Working with data involves a lot of hidden state; you can read all the code you want, but that code is going to be applied to data which is usually loaded from some external source, and if you don't know what the data *looks like*, then good luck trying to understand what the code is actually *doing*.

This is, of course, true of any non-trivial program: hidden state inevitably creeps in. *Typing* is the primary way that programming languages have used to handle the difficulties of hidden state. For example, here's a Python function with no types specified:

```python
def foo(x):
    return x + x
```

What does this function `foo` do? Depending on what *x* is, it could be either adding a number (integer or float) to itself, or it could be appending a string to another string, or it could be just calling some custom `__add__` method of who-knows-what class. Typing greatly improves our ability to know what `foo` does *without having to understand how `foo` is used in the broader context of the program*.

```python
def foo(x: int) -> int:
    return x + x
```

I may not know what the *value* of *x* is, but I know that it's *an integer*, which allows me to understand what is going to happen within the function.

But typing doesn't solve our problem if we're using `DataFrame`s:

TODO: Check code:

 ```python
 def clean_data(df: pd.DataFrame):
    df['foo'] = df['foo'].fillna(0)
    df['foo'] = df['foo'].round().astype(int)
    df['bar'] = df['foo'] * df['baz']
    df['stdize_bar'] = df['bar'] / df['bar'].stddev()
```

Does the first line of this function change `df['foo']` at all? How many missing values were there, if any? What about the second line: what does it do? Since integer columns cannot be missing, `df['foo']` must have been a float type, so we're converting it to an integer, but did the `round()` method actually change values, or was it just there to be safe, or suppress a warning? All we can do is
*assume* that the `round()` wouldn't be there if it didn't *need to be*.

Now, the third line: it's clearly multiplying (row-wise) two columns, but what is
`df['bar']` going to look like? Is *it* a integer, or a float? Is it ever missing (`np.nan`)?

When you start building up more complicated procedures, where we're grouping and aggregating and stacking and unstacking and merging, etc., etc., even if you know what the starting data looks like[^2], it's very difficult to—through reading the code—follow along such that the abstraction in your head is an accurate representation of what the actual data structure will look like through every step of the process. Nor will typing alone save you: if `df['foo']` is all missing values, then `df['bar']` will be all zero, and thus the standard deviation will be zero, and you'll get an error on the fourth line when you try to divide by zero—and knowing that `df['bar']` is a float won't help you at all.

This is why *notebooks* and other *interactive* workflows[^3] have been so widely adopted by people who do data analysis; flipping back and forth between *manipulating* the data and *inspecting the results* makes it infinitely easier to keep up with what's happening and make sure things look the way you expect.

Notebooks and interactive workflows work great for a one-off analysis, but when an analysis is being repeated on different datasets, or built on and expanded, or maintained over time, the interactivity becomes a burden: the very mutability of the system, which makes it easier to do analysis in the first place, makes understanding and modifying the program more difficult. Often, you have to inspect the data at each step in a complex process, which then requires *changing* the process itself (say, adding cells with exploratory data analysis of an intermediate dataset), and essentially stepping back into the role of the original developer. Then, once you've, say, found and resolved a bug or handled an edge case, you need to go *back* to the *non*-interactive way of using the code, you have to clean up all of that exploration and inspection—and hope a new but similar issue doesn't require you to re-create it again in the future.

There are ways to mitigate this. For example, you can have a lot of data validation, to ensure that the input and output of every step looks as it should. But this requires the time and skill to anticipate all possible edge cases.

[^2]: Even if you know what the data *should* look like, that code could be applied to *incorrect* or *malformed* data, and then who knows what could happen.
[^3]: Programs like Stata, SAS, and RStudio allow you to view data interactively, for example.

Why Python?
-----------
Simple: Because that's the language I know the best!
Also, Python is used a lot for data science, and so having `rithm` interoperate with Python opens up a host of libraries.

## Primitive data types

- int (Integers)
- float
-

## Algorithms

Use the keyword `algo` to create a new algorithm. An algorithm is simply a process that has multiple _steps_, which are executed one after another. When working with data, you frequently need to do a lot of little procedures, which are often clunky to work with and hard to debug. `algo`s make this much easier.

For example, let's say you have a dataframe `df` and you want to:

1. Rename a few cryptically named variables
2. Convert column names to camel_case
3. Split a string column on `,`, and create two new columns from it (and delete the old column)

Here's how you would do that in Python using pandas:

```python
from rithm.examples import titanic

def clean_data(df):
    df.rename(columns={
        "Pclass": "passenger_class",
        "SibSp": "num_siblings_spouses",
        "Parch": "num_parents_children"
    }, inplace=True)
    df.columns = to_camel_case(df.columns)
    df[['last_name', 'first_name']] = df['name'].str.split(', ')
    df.drop(columns='name', inplace=True)
```

Then, I can call `clean_data(titanic)`
and change the `titanic` dataframe.

Now, what happens if the name splitting code is not behaving as you expect (for example, maybe some rows have zero commas, or more than one)? Well, what you want to do is get the result of the splitting line _before_ the original `name` column has been dropped, so you can inspect the inputs and the outputs and see what's going on. So, you need to comment out that last line (which drops the column), re-run the code, and then you can interact with the `titanic` dataframe.

With `algo`s in `rithm`, you can do this:

```rithm
algo clean_data(df) do
    df -rename-> do
        @Pclass as @passenger_class
        @SibSp as @num_siblings_spouses
        @Parch as @num_parents_children
        .columns => to_camel_case
    end
    -split_names-> do
        @name => split(", ")
        => to_columns(@last_name, @first_name)
    end
end
```

Now, to get the state of titanic 

`titanic -> clean_data@split_names#1st`

This will apply the `clean_data` algorithm to `titanic` _up until the 1st step of the `split_names` step_.

Use `->` to pipe an argument to a function
Use `=>` to _modify_ an argument in place
Use `as` to rename a variable or column.




## Integer
int or np.int64?

## Float
Decimal? Python float or np.float64?

## Collections

### Tuple (immutable sequence)

Python tuple?

```
1, 2, 3
~[1 2 3]
![1 2 3]
[1 2 3]
[! 1 2 3 !]
[|1 2 3|]
```

### List (mutable sequence)

```
[1 2 3]
[1; 2; 3]
```

### Set (mutable set)

```
{1 2 3}
```

### Frozen set (immutable set)

```
{! 1 2 3 !}
!{1 2 3}
{1, 2, 3}
{1  2   3}
```

### Dictionary (mutable mapping)

```
{a=1, b=2, c=3}
{a: 1, b: 2, c: 3}
{a :> 1, b :> 2, c :> 3}
{@a=1, @b=2, @c=3}
{@a=1 @b=2 @c=3}
{@a=1; @b=2; @c=3}
```

### Frozen dictionariy (immutable mapping)


### Series (indexed mutable sequence)
```
[
    #1: 1;
    #2: 2;
    #3: 3;
]
Column[1; 2; 3;]
Col[1; 2; 3;]
Col[@1: 1; @2: 2; @3: 3]
```

### Array (multi-dimensional, single-type)

```
[[1 2 3]]
[1 2 3;]
[1 2 3; 
 4 5 6;]
Array(1 2 3; 4 5 6)
```

### DataFrame (DF)
```
{
    @col1: [#1: 1; #2: 2; #3: 3;]
    @col2: [4 5 6]
}
[
    @col1   @col2   @col3;
    1       "hello" "bar";
    1.3     
]
```py
'''
df = ```csv
col1,col2,col3
1,"hello","bar"
2,"goodbye","foo"
'''
"""
end
[
    #1: {@col1: 1, @col2: 2}
    #2: {@col1: 3, @col2: 4}
]
```

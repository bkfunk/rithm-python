# Open questions

1. Should we have implicit variable declaration, like Python? Or use `let`? Or `var`? `const`?
- `let` for local to block?
- Or, should we make the block an object accessible by like `this`, and then everything is a class attribute? So, `block.foo = 3`, and anything else is global variable?

2. Should blocks return the last value in the block?

3. Should blocks always be do/end?

4. Should we return values from variable assignment?

5. Should we use Empty for None? Or is ? enough? Is there a difference between a null value and an unknown value?

6. How should the if condition be terminated? A `then` keyword? Or a `do` block? Either?

7. How to avoid or handle dangling else clause? use `endif`? or `end`?

8. Should and/or return the arguments, or True/False? Should `x = 0 or 10` be 10, or True?

9. Should we have a `new` keyword? Or create instances as Python does?

10. Should we require spaces on either side of arrows?

Pros:
- easier to scan / parse
- Cleaner to read? Sets off arrows?

Considerations:
- Are arrows special? Or should spaces be used meaningfully throughout? As delimiters? Is there any reason not to require spaces around operators etc.?


Thoughts:
Classes with methods, but methods are the only things that can modify an object
All objects are immutable by functions, but not methods.
Functions are multiple dispatch, referred to by types

sum[G, G] -> G
sum[int, int] -> int
sum[float, float] -> float
sum[int, float] -> float
sum(1, 1) # ==> sum[int, int]
sum[float, float](1, 1) # ==> coerce 1 to float
which(sum, 1, 1) ==> tells you which version of sum will get called
methods(sum) ==> lists the different types

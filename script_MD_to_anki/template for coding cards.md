
Stuff that is added here is not picked up
# Front side

## Left tabs

### ArgParser
Initializing the parser 
```python
import argparse

# Instantiate the parser
parser = argparse.{{c1::ArgumentParser}}(description='Optional app description')
```

Adding arguments to the parser
```python
# Required positional argument
parser.{{c1::add_argument}}('pos_arg', type=int,
                    help='A required integer positional argument')
```

Parse
```python
args = parser.{{c1::parse_args}}()
```

Accessing the value
```python
print("Argument values:")
print(args.{{c1::pos_arg}})
```

# Back side

## Right tabs

### Explanation
To parse cli args you can use the built-in module`argparse`. See [[argparse]]

The steps are:
1. Initializing
2. Adding args (via `add_argument`), which can be:
	- Positional 
	- Positional optional (`nargs="?"`)
	- Optional args (by adding -- before the argument's name)
	- Switch arguments (`action="store_true"`)
3. Parse
4. Accessing the value

---

# Front side

## Left tabs

### - Question
# What are microservices?

# Back side

## Left tabs

### Answer
*Microservices* is an architecture which splits up one big backend (also called monolith) into smaller backends (microservices); each backend application can be created with a different programming language, while all backends are able to communicate with each other via APIs.

See [[Microservices architecture]]

## Right tabs

### Extra Explanation
![Microservices picture](https://www.robinwieruch.de/static/b8ed3e68e8e64b31d4556acc93694182/57e27/16.webp)


*********

# Front side

## Left tabs

### Cloze
Encode a given string to a url-safe string
```python
import {{c1::urllib.parse}}
print(urllib.parse.{{c1::quote}}("Müller".encode('utf8')))
```

Notice: `.encode` is added to make sure the url can support languages other than English.

---
---
***
---

# Back side

## Left tabs

### Card
This is a bad card

---

# Front side

## Right tabs

### Bad card 2
Another one

---

# frontside
## lefttabs
### forEach()
How does forEach differ from map()?

```js

function addOne(number) {
	return number + 1
}

result = [1, 2, 3, 4].forEach(addOne)

```

## rightside
### map()
# Map version:
```js

function addOne(number) {
	return number + 1
}

result = [1, 2, 3, 4].map(addOne)

```

---

# frontside
## lefttabs
### Fast inverse square root


---

# Front side

## Left tabs

### Fast inverse square root
How does this work?
```C
float Q_rsqrt( float number )
{
	long i;
	float x2, y;
	const float threehalfs = 1.5F;

	x2 = number * 0.5F;
	y  = number;
	i  = * ( long * ) &y;                       // evil floating point bit level hacking
	i  = 0x5f3759df - ( i >> 1 );               // {{c1::what the fuck?}} 
	y  = * ( float * ) &i;
	y  = y * ( threehalfs - ( x2 * y * y ) );   // 1st iteration
//	y  = y * ( threehalfs - ( x2 * y * y ) );   // 2nd iteration, this can be removed

	return y;
}
```

---

#frontside
##lefttabs
### Image test
![mochitto](https://avatars.githubusercontent.com/u/98263539?v=4)
![Local demo](./test_images/Demo.png)
![[old_cards.png | 400]]
![[Highlight_component_concept_art.jpg | 400]]
![[Capycorn.jpg | 400]]

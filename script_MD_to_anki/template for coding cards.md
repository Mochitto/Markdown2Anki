
Stuff that is added here is not picked up
# Front side

## Left tabs

### - JS Hello world 
```js
console.log("hello world!>>>>>>")
```
### PY hello world
```python
print("hello world!")
```


## Right tabs

### Answer 
This will probably go instead of first old right tab

### Extra-tab!
This is added after the second one!

---

# Front side

## Left tabs

### JS Hello world AND PYTHON

What if I have something before?
```js
console.log("hello world!")
```

*THIS IS PYTHON*
```python
def main():
    # logging.basicConfig(filename='process.log', level=logging.INFO)
    logging.basicConfig(level=logging.INFO)
    logging.info('Starting cards extraction')
    
    
    cards = extract_cards(markdown_input)
    for index, card in enumerate(cards):
        back_front_sides = extract_front_back(card, index)
        left_and_right_tabs = extract_left_right_tabs(back_front_sides["front"])
        left_tabs = extract_tabs(left_and_right_tabs["left_tabs_block"])
```
I actually still have some stuff here...
Such as a list!
1. AHAHAHAHA
2. THIS SHSHSHS
	- And that

where is this??

### PY hello world
```python
print("hello world!")
```

## Right tabs

### Question 
This is what goes in the right side of the card.
The markdown that is in it *goes* in the card.
So you can for example:
1. Add markdown to your explanations
2. I don't know what else
		- You can have lists!
| and tables? | I think |
| --- | ----|
| yeah like this! |Ayy! |

### Microservices structure
I would like to keep this image as well!
![This image](something.png)


*********

# Front side

## Left tabs

### - JS Hello world 
```js
console.log("hello world!")
```
### PY hello world
```python
print("hello world!")
```

## Right tabs

### - Question 
This is what goes in the right side of the card.
The markdown that is in it *goes* in the card.
So you can for example:
1. Add markdown to your explanations
2. I don't know what else
		- You can have lists!
| and tables? | I think |
| --- | ----|
| yeah like this! |Ayy! |

### Microservices structure
I would like to keep this image as well!
![This image](something.png)

# Backside

## Left tabs

### JS Hello world with comment 
```js
console.log("hello world!")
```
This is how you would write this! :)

### Answer
This **SHALL BE** added to the left side.

## Right tabs

### Answer 
This will probably go instead of first old right tab

### Extra-tab!
This is added after the second one!
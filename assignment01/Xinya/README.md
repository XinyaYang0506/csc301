## Xinya Yang, Ben Gafford

## Compile/run instructions:
`java Main.java < <input_file>`

## Running time analysis:

### `findkthDistance()`:  
This function will run in `O(s)`, where `s` is the size of the tree. The function traverses each node of the tree without repitition. 

### `findStructure()`:
This function will run in `O(s)`, where `s` is the size of the tree. The function traverses each node of the tree without repitition.   

### `calculateKInChain()`:
This function will run in `O(s)`, where `s` is the size of the tree. The function traverses each node of the tree without repitition. 

### `Solution()`:  
The first `for` loop, lines `70-92` will run in `O(n)`, where `n` is the number of stations.

The second `for` loop, lines `98-106` will run in `O(n)`, where `n` is the number of stations. Because each tree contains unique elements, then all of the nodes of all of the trees add up to be the stations.

The third `for` loop, lines `110-124`, run in `O(n)`, where `n` is the number of stations. The outer loop will run `n` times, and then the body of the `while` loop from `116-122` will add up to be run at most `n` times. 

The fourth `for` loop, lines `127-130` will run `n` times. 

### main:

This function is comprised of two main parts:

- Parsing the input: 
	- `O(n)`, where `n` is the number of lines (which is the number of stations + 1). 
- Running `Solution()`: 
	- `O(n)` as described above, where `n` is the number of stations.  
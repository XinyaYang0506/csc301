# Assignment 5 – Red-black tree
## Ben Gafford, Xinya Yang

## Problem Description
This project includes an implementation of a red-black tree that does not allow for duplicate values.

Our implementation includes three 'phases' as follows:

- Initialization phase  
  - A red black tree is initialized using random node values from the Linear Feedback Shift Register (LFSR) algorithm. The tree starts with 10 nodes, and the tree structure is printed with level-order traversal. 
- Update phase  
  - User can insert and delete nodes from the tree
  - After each operation, the new tree will be printed
- Information phase  
  - User can query for the black height of a node by referring to its value

The LFSR algorithm consists of a seed value and a set of 'tap bits', and will create a stream of psuedo-random values accordingly. We use little-endian bit representation. 

## Implementation details 

### `lfsr()`
* Args:
  * 8 bit seed
  * set of 'tap' values
* Running time:
  * `O(n)`, where `n` is the number of `tap` values. Notice that the upper limit on `n` is 8. Therefore in our case it is `O(1)`. 

### Initialize RB Tree
Generate 10 pseudo-random values and insert them all into the tree. In a general case, this takes `O(nlogn)` time, where n is the number of nodes to be inserted. 

In our case, however, it is done in `O(1)` time because we always initialize the tree with 10 nodes.

### Print tree
We print the tree in level-order traversal. This takes `O(n)`, as we have to touch every node in the tree exactly once.

### Inserting values
Node insertion is worst-case `O(logn)`, where n is the number of nodes, because it is by construction a balanced binary tree. 

### Deleting values
Node insertion is worst-case `O(logn)`, where n is the number of nodes, because it is by construction a balanced binary tree. 

### Get black_height
`black_height(uint8_t val)`  
Gets the black height of a given key. This consists of finding the node in the tree in `O(logn)`, and then finding the black height of the given node `O(logn)`. The total time complexity is `O(logn)`. 

## Instructions to execute code
### Build:
`make rbtree`

### Execute:
`./rbtree`

The program `rbtree` is interactive. Users can add, delete, or query the black height of a given node. These are done using the following commands, respectively:
`ADD <value>`  
`DEL <value>`  
`BLKH <value>`

Notice that duplicate nodes are not allowed by construction, and attempting to add duplicate nodes will result in an error. 




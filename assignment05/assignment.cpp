#include <string>
#include <iostream>
#include <fstream>
#include <vector>
#include <iterator>
#include <algorithm>
#include <unordered_set> 
#include <stdint.h>

#include <memory>

using namespace std;

uint8_t lsfr(uint8_t seed, const vector<int> & tap) {
    bool new_bit = 0; 
    for (auto index : tap) { 
        new_bit ^= (seed & (1 << index)) != 0; 
    }

    seed = seed >> 1; 
    seed += new_bit << 7; 

    return seed; 
}

class tree_node {
public: 
    uint8_t value; 
    bool is_red; 
    shared_ptr<tree_node> parent; 
    shared_ptr<tree_node> left_child; 
    shared_ptr<tree_node> right_child;
    tree_node(int val, shared_ptr<tree_node> parent_ptr)
        : value(val), is_red(true), left_child(nullptr), right_child(nullptr), parent(parent_ptr){}
};

ostream& operator<<(ostream& os, tree_node const & tn) {
  os << "(" << tn.value <<  ", " << (tn.is_red ? "red)" : "black)");
  return os;
}

class redblack_tree {
private:
shared_ptr<tree_node> get_node(uint8_t value) {
  if(root == nullptr) {
    return nullptr;
  }
  auto cur_node = root;
  while(cur_node != nullptr) {
    if(cur_node->value == value) {
      return cur_node;
    } else if(cur_node->value < value) {
      cur_node = cur_node->right_child;
    } else {
      cur_node = cur_node->left_child;
    }
  }
  return nullptr;
}
  
void restore(shared_ptr<tree_node> node); 
void counter_clockwise_rotate(shared_ptr<tree_node> little_node) {
    shared_ptr<tree_node> large_node = little_node->right_child; 
    little_node->right_child = large_node->left_child; 
    if (large_node->left_child != nullptr) {
        large_node->left_child->parent = little_node; 
    }

    //change their parents
    large_node->parent = little_node->parent; 
    if (little_node->parent == nullptr) {
        root = large_node; 
    } else {
        if (little_node == (little_node->parent->left_child)) {
            little_node ->parent->left_child = large_node; 
        } else {
            little_node ->parent->right_child = large_node; 
        }
    }

    //put little_node as large_node's left child
    large_node->left_child = little_node; 
    little_node->parent = large_node; 

    return;
}

void clockwise_rotate(shared_ptr<tree_node> large_node) {
    shared_ptr<tree_node> little_node = large_node->left_child; 
    //transfer sub-tree ownership
    large_node->left_child = little_node->right_child; 
    if (large_node->left_child != nullptr) {
        large_node->left_child->parent = large_node; 
    }

    //change how grandparents are connected
    little_node->parent = large_node->parent; 
    if (little_node->parent == nullptr) {
        root = little_node; 
    } else {
        if (large_node == (large_node->parent->left_child)) {
            large_node ->parent->left_child = little_node; 
        } else {
            large_node ->parent->right_child = little_node; 
        }
    }

    //put large_node as little_node's right child
    little_node->left_child = large_node; 
    large_node->parent = little_node; 

    return;
}
  void delete_node_fixcolor(shared_ptr<tree_node> node);
public: 
    shared_ptr<tree_node> root = nullptr; 
    redblack_tree(vector<uint8_t> values);
    bool insert_node(uint8_t value);
    void print_tree(void);
    bool delete_node(uint8_t value); 
    int black_height(shared_ptr<tree_node> node); 
    int black_height(uint8_t value); 
    shared_ptr<tree_node> find(uint8_t value); 
};


bool redblack_tree::delete_node(uint8_t value) {
  // Why do we have to implement this
  
  auto node = get_node(value);

  // Case: Empty tree
  if(node == nullptr) {
    return false;
  }

  // Case: 1 element tree
  if(node == root) {
    if(node->value == value) {
      root = nullptr;
      return true;
    } else {
      return false;
    }
  }

  bool fix_color = false;
  
  // Case: 2+ element tree
  bool is_left_child = 0;
  if(node == root || node->value < node->parent->value) {
    is_left_child = 1; // left-child
  } else {
    is_left_child = 0; // right-child
  }

  // Determine replacement node
  shared_ptr<tree_node> replacement_node = nullptr;
  // No children
  if(node->left_child == nullptr && node->right_child == nullptr) {
    replacement_node = nullptr;
    if(!node->is_red) {
      fix_color = true;
    }
  // only right child 
  } else if(node->left_child == nullptr) {
    replacement_node = node->right_child;
    // Update parent
    if(node != root) {
      if(is_left_child) {
	node->parent->left_child  = replacement_node;
      } else {
	node->parent->right_child = replacement_node;
      }
    }
    // Update replacement_node
    if(replacement_node != nullptr) {
      replacement_node->parent = node->parent;
      replacement_node->is_red = false;
      fix_color = false;
    }
  // only left child 
  } else if(node->right_child == nullptr) {
    replacement_node = node->left_child;
    // Update parent
    if(node != root) {
      if(is_left_child) {
	node->parent->left_child  = replacement_node;
      } else {
	node->parent->right_child = replacement_node;
      }
    }
    // Update replacement_node
    if(replacement_node != nullptr) {
      replacement_node->parent = node->parent;
      replacement_node->is_red = false;
      fix_color = false;
    }
  // both children
  } else {
    // Get in-order successor to node
    replacement_node = node->right_child;
    while(replacement_node->left_child != nullptr) {
      replacement_node = replacement_node->left_child;
    }

    // Recursively remove replacement node
    delete_node(replacement_node->value);
    
    // Update node
    node->value = replacement_node->value;
    node = replacement_node;
    fix_color = false; // should be fixed in recursive case
  }

  // If we removed a black node, we need to fix things
  if(fix_color) {
    delete_node_fixcolor(node);
  }
  return true;
}

void redblack_tree::delete_node_fixcolor(shared_ptr<tree_node> node) {
  bool is_left_child = 0;
  if(node == root || node->value < node->parent->value) {
    is_left_child = 1; // left-child
  } else {
    is_left_child = 0; // right-child
  }
    shared_ptr<tree_node> sibling = nullptr;
    if(!is_left_child) { // Sibling is right-child
      sibling = node->parent->right_child;
      if(sibling == nullptr) { // No sibling
	delete_node_fixcolor(node->parent);
      } else if(sibling->is_red) { // Red right sibling
	node->parent->is_red = true;
	sibling->is_red = false;
	counter_clockwise_rotate(node->parent);
	delete_node_fixcolor(node);
      } else { // Sibling black
	if(sibling->right_child->is_red) { // R-R case
	  sibling->right_child->is_red = sibling->is_red;
	  sibling->is_red = node->parent->is_red;
	  counter_clockwise_rotate(sibling);
	} else if(sibling->left_child->is_red) { // R-L case
	  sibling->left_child->is_red = node->parent->is_red;
	  clockwise_rotate(sibling); 
	  counter_clockwise_rotate(node->parent);
	}
	node->parent->is_red = false;
      }
    } else { // Sibling is left child
      sibling = node->parent->left_child;
      if(sibling->is_red) { // Red left sibling
	node->parent->is_red = true;
	sibling->is_red = false;
	clockwise_rotate(node->parent);
	delete_node_fixcolor(node);
      } else { // Sibling black
	if(sibling->left_child->is_red) { // L-L case
	  sibling->left_child->is_red = sibling->is_red;
	  sibling->is_red = node->parent->is_red;
	  clockwise_rotate(node->parent);
	} else if(sibling->right_child->is_red) { // L-R case
	  sibling->right_child->is_red = node->parent->is_red;
	  counter_clockwise_rotate(sibling);
	  clockwise_rotate(node->parent);
	}
	node->parent->is_red = false;
      }
    }
    if(!sibling->left_child->is_red && !sibling->right_child->is_red) {
      sibling->is_red = true;
      if(!node->parent->is_red) {
	delete_node_fixcolor(node->parent);
      } else {
	node->parent->is_red = false;
      }
    }
  
}

redblack_tree::redblack_tree(vector<uint8_t> values) {
    for(auto val : values) {
        insert_node(val);
    }
}

void redblack_tree::print_tree() {
  if(root == nullptr) {
    return;
  }

  cout << root << endl;

  vector<shared_ptr<tree_node> > parents;
  parents.push_back(root);

  vector<shared_ptr<tree_node> > new_parents;
  
  while(parents.size() > 0) {
    for(auto parent : parents) {
      if(parent == nullptr) {
	continue;
      }
      if(parent->left_child != nullptr) {
	new_parents.push_back(parent->left_child);
	cout << parent->left_child << " ";
      }
      if(parent->right_child != nullptr) {
	new_parents.push_back(parent->right_child);
	cout << parent->right_child << " ";
      }      
    }
    parents = new_parents;
    new_parents.clear();
  }
}

bool redblack_tree::insert_node(uint8_t value) {
    if (root == nullptr) {
        root = make_shared<tree_node>(tree_node(value, nullptr)); 
        return true; 
    } else {
        shared_ptr<tree_node> cur_node = root; 
        // uint8_t cur_value = root->value; 
        while (true) {
            if (value < cur_node->value) {
                if (cur_node->left_child == nullptr) { // touch the bottom
                    cur_node->left_child = make_shared<tree_node>(tree_node(value, cur_node)); 
                    cur_node = cur_node->left_child; 
                    break; 
                } else {
                    cur_node = cur_node->left_child; 
                }
            } else if (value > cur_node->value){ // value > cur_value
                if (cur_node->right_child == nullptr) {
                    cur_node->right_child = make_shared<tree_node>(tree_node(value, cur_node)); 
                    cur_node = cur_node->right_child; 
                    break; 
                } else {
                    cur_node = cur_node->right_child; 
                }
            } else {
                cerr << "ERROR: inserting a duplicated value. " << endl; 
                return false; 
            }
        }

        redblack_tree::restore(cur_node);
        return false; //should not need to get here
    }
}

int redblack_tree::black_height(uint8_t value) {
  if(root == nullptr) {
    return -1;
  } else {
    auto node = get_node(value);
    
    // Overcounts by one in the beginning, but undercounts at the end, so this is fine
    int count = 0; 
    while(node->left_child != nullptr && node->right_child != nullptr) {
      if(!node->is_red) {
	count++;
      }
      if(node->left_child != nullptr) {
	node = node->left_child;
      } else {
	node = node->right_child;
      }
    }
    return count;
  }
}

int main() {
  return 0;
}

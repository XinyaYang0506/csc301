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

public: 
    shared_ptr<tree_node> root = nullptr; 
    redblack_tree(vector<uint8_t> values);
    bool insert_node(uint8_t value);
    void print_tree(void);
    void delete_node(uint8_t value); 
    int black_height(shared_ptr<tree_node> node); 
    int black_height(uint8_t value); 
    shared_ptr<tree_node> find(uint8_t value); 
};


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
    int count = -1;
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

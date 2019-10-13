#include <string>
#include <iostream>
#include <fstream>
#include <vector>
#include <iterator>
#include <algorithm>

using namespace std;

string VALID_CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-";

int edit_distance (std::string & w1, std::string & w2) {
    int len1 = w1.length(); 
    int len2 = w2.length(); 

    int edit_table[len1+1][len2+1];

    for (int i = 0; i < len1 + 1; i++) {
        for (int j = 0; j < len2 + 1; j++) {
            if (i == 0) {
                edit_table[i][j] = j; 
            } else if (j == 0) {
                edit_table[i][j] = i; 
            } else {
                if (w1.at(i - 1) == w2.at(j - 1)) {
                    edit_table[i][j] = edit_table[i -1][j-1]; 
                } else {
                    edit_table[i][j] = 1 + min(min(edit_table[i][j -1], edit_table[i - 1][j]), edit_table[i - 1][j -1]);
                }
            }
        }
    }

    return edit_table[len1][len2]; 
}

void fix_spelling (std::string str, vector<std::string> & dict) {
  std::size_t current, previous = 0;
  std::vector<string> words;

  current = str.find(' ');

  while(current != std::string::npos) {
      words.push_back(str.substr(previous, current - previous)); 
      previous = current + 1; 
      current = str.find(' ', previous); 
  }
  words.push_back(str.substr(previous, current - previous)); 
  std::vector<std::string> fixed_words;
  for(auto word : words) {
      auto clean_word = 
      if (find(dict.begin(), dict.end(), word) == dict.end()) {
          int distance = 10000; 
          std::string candidate; 
          for (auto dict_word : dict) {
              int cur_distance = edit_distance(dict_word, word); 
              if (cur_distance < distance) {
                  distance = cur_distance;
                  candidate = dict_word;  
              }
          }
          fixed_words.push_back(candidate); 
      } else {
        fixed_words.push_back(word);
      }
  }

  for(auto word : fixed_words) {
    std::cout << word << std::endl; 
  }

  return; 

}

int main () {
    std::ifstream dictfile("words.txt");
    vector<std::string> dict;

    copy(std::istream_iterator<std::string>(dictfile),
         std::istream_iterator<std::string>(),
         back_inserter(dict));

    fix_spelling("The quik brwn fox jmped over the lazy dag.", dict);
    return 0; 
}
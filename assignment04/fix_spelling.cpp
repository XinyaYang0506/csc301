#include <string>
#include <iostream>
#include <fstream>
#include <vector>
#include <iterator>
#include <algorithm>
#include <unordered_set> 

using namespace std;

string VALID_CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-/";


//This function calculates the Levenshtein distance of the two words. 
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

//This function check every word in the string str and correct each word if it is not in the dict
void fix_spelling_str (std::string str, unordered_set<std::string>& dict) {
    //tokenize the Your string input: minimun

    std::size_t current, previous = 0;
    std::vector<string> words;

    current = str.find(' ');

    while(current != std::string::npos) {
        words.push_back(str.substr(previous, current - previous)); 
        previous = current + 1; 
        current = str.find(' ', previous); 
    }
    words.push_back(str.substr(previous, current - previous)); 

    // traverse the vector words and fix each one if needed 
    std::vector<std::string> fixed_words;
    for(auto word : words) {
        int i = word.length() - 1; 
        while (i >= 0) {
            char c = word.at(i); 
            if ((c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z') || c == '-' || c == '/') {
                break;  
            }
            i--; 
        }
            
        auto clean_word = word.substr(0, i + 1); 
        auto punctuation = word.substr(i + 1, word.length()); 
        std::string candidate = clean_word; 

        // go through the dict to find the closest string
        if (!clean_word.empty() && dict.find(clean_word) == dict.end()) {
            int distance = 1000000; //A really big number
            for (auto dict_word : dict) {
                int cur_distance = edit_distance(dict_word, clean_word); 
                if (cur_distance < distance) {
                    distance = cur_distance;
                    candidate = dict_word;  
                }
            }
        }
        fixed_words.push_back(candidate + punctuation); 
    }

    //print it out
    for(auto word : fixed_words) {
        cout << word << " "; 
    }
    return; 
}


int main () {
    std::ifstream dictfile("words.txt");
    vector<std::string> dict;

    copy(std::istream_iterator<std::string>(dictfile),
        std::istream_iterator<std::string>(),
        back_inserter(dict));
    
    unordered_set<string> word_dict(dict.begin(), dict.end());

    string input; 
    cout << "Your string input: "; 
    std::getline (std::cin,input);
    cout << "Corrected version: "; 
    fix_spelling_str(input, word_dict);
    cout << endl; 
    return 0; 
}

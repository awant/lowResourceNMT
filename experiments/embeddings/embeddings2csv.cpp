#include <iostream>
#include <fstream>
#include <string>


using std::string;
using std::cin;
using std::cout;
using std::endl;

const size_t EMB_SIZE = 300;


void fixEmbeddings() {
    string s;
    long double val;
    char c;
    while(true) {
        cin >> s;
        if(cin.eof()) {
            break;
        }
        cin >> s; // <number> <token>
        cout << s << ",";
        cin >> c; // [
        for(size_t i = 0; i < EMB_SIZE; ++i) {
            cin >> val;
            cout << val << ",";
        }
        cout << "\n";
        cin >> c; // ]
    }
}

int main (int argc, char *argv[]) {
    if(argc < 2) {
        cout << "Need args" << endl;
        return 0;
    } 
    cin.tie(0);
    std::ios::sync_with_stdio(false);
    freopen(argv[1], "r", stdin);
    freopen(argv[2], "w", stdout);
    fixEmbeddings();
    return 0;
} 

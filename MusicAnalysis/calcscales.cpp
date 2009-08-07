#include <iostream>
#include <iomanip>
#include <cstdlib>
#include <fstream>
#include <vector>
using namespace std;
ifstream fin;

void StringExplode(string str, string separator, vector<int>* results){
    int found;
    found = str.find_first_of(separator);
    while(found != string::npos){
        if(found > 0){
            results->push_back(atoi(str.substr(0,found).c_str()));
        }
        str = str.substr(found+1);
        found = str.find_first_of(separator);
    }
    if(str.length() > 0){
        results->push_back(atoi(str.c_str()));
    }
}

int find(int target, vector<int>* tosearch)
{
    for (int i = 0; i < tosearch->size(); i++)
    {
        if (tosearch->at(i) == target)
        {
            return i;
        }
    }
    return -1;
}

int main(int argc, char* argv[])
{
    if (argc < 6)
    {
        cout << "invalid arguments!" << endl; return -1;
    }

    // get search items, wraparound status, "ordered", and requiring consecutive notes, and filter.
    bool ordered = atoi(argv[1]);
    bool wraparound = atoi(argv[2]);
    bool consecutive = atoi(argv[3]);
    int filter = atoi(argv[4]);
    vector<int> query;
    StringExplode(argv[5], " ", &query);
    /*
    query.push_back(0);
    query.push_back(3);
    query.push_back(7); // A C E
    */
    
    string line;
    fin.open("all_scales.txt");
    vector<int> scale;
    vector<int> matching_scales;
    int temp;
    int current_scale = 0;
    int matching = 0;
    if (fin.is_open())
    {
        while ( !fin.eof() )
        {
            getline(fin, line);
            temp = atoi(line.c_str());
            // check if filter matches.
            if (temp & filter)// TODO: check w/ filter from user.
            {
                for (int i = 0; i < 12; i++)
                {
                    bool matched = true;
                    scale = vector<int>();
                    getline(fin, line);
                    StringExplode(line, " ", &scale);
                    if (ordered) // this only matters if search is consecutive and ordered, right?
                    {
                    }
                    else
                    {
                        // if ordered is not set, we don't care about any other results.
                        for (int i = 0; i < query.size(); i++)
                        {
                            if (find(query.at(i), &scale) < 0)
                            {
                                matched = false;
                            }
                        }
                    }
                    
                    if (matched)
                    {
                        // if it matches, print current scale #
                        cout << current_scale << endl;
                        matching++;
                    }
                    current_scale++;
                }
            }
            else
            {
                // just throw away 12 lines.
                for (int i = 0; i < 12; i++)
                {
                    getline(fin, line);
                    current_scale++;
                }
            }
                
            
        }
        fin.close();
    }
    //cout << matching << " matching!" << endl;

    //system("PAUSE");
    return 0;
}

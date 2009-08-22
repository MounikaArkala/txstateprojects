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
    if (argc < 7)
    {
        cout << "invalid arguments!" << endl; return -1;
    }

    // get search items, wraparound status, "ordered", and requiring consecutive notes, filter, and starting notes.
    bool ordered = atoi(argv[1]);
    bool wraparound = atoi(argv[2]);
    bool consecutive = atoi(argv[3]);
    int filter = atoi(argv[4]);
    vector<int> start;
    vector<int> query;
    StringExplode(argv[5], " ", &start);
    StringExplode(argv[6], " ", &query);
    /*
    query.push_back(0);
    query.push_back(3);
    query.push_back(7); // A C E
    */
    
    string line;
    fin.open("all_scales.txt");
    vector<int> scale;
    vector<int> matching_scales;
    vector<int> locations;
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
            if (temp & filter)
            {
                for (int i = 0; i < 12; i++)
                {
                    bool matched = true;
                    scale = vector<int>();
                    getline(fin, line);
                    StringExplode(line, " ", &scale);
                    
                    // check starting pitches.
                    if (find(scale.at(0), &start) < 0)
                    {
                        matched = false; // skip scale if it doesn't start with a target note.
                    }
                    if (matched)
                    {
                        locations = vector<int>();
                        for (int i = 0; i < query.size(); i++)
                        {
                            int location = find(query.at(i), &scale);
                            if (location < 0)
                            {
                                matched = false;
                            }
                            else
                            {
                                locations.push_back(location);
                            }
                        }
                    }
                    if (matched)
                    {
                        if (ordered)
                        {
                            /* first check if they're in the correct order. */
                            if (!wraparound)
                            {
                                for (int i = 0; i < locations.size() - 1; i++)
                                {
                                    if (locations.at(i+1) < locations.at(i))
                                    {
                                        matched = false;
                                    }
                                    if (consecutive)
                                    {
                                        if (locations.at(i+1) != locations.at(i) + 1)
                                        {
                                            matched = false;
                                        }
                                    }
                                }
                            }
                            /* if there's wraparound then the check is slightly more complicated. */
                            else
                            {
                                int prevloc = 100000;
                                for (int i = 0; i < locations.size() - 1; i++)
                                {
                                    if (locations.at(i+1) < locations.at(i) &&
                                        locations.at(i+1) > prevloc)
                                    {
                                        matched = false;
                                    }
                                    prevloc = locations.at(i);
                                    if (consecutive)
                                    {
                                        if (locations.at(i) == scale.size() - 2) // -2 because we want to wrap around not including the final note (since it's same as first note.)
                                        {
                                            if (locations.at(i+1) != 0)
                                            {
                                                matched = false;
                                            }
                                        }
                                        else
                                        {
                                            if (locations.at(i+1) != locations.at(i) + 1)
                                            {
                                                matched = false;
                                            }
                                        }
                                    }
                                }
                            }
                        }
                        else
                        {
                            if (consecutive)
                            {
                                int state_transitions = 0, state;
                                int location = find(scale.at(0), &query);
                                if (location < 0) // not a queried item.
                                {
                                    state = false;
                                }
                                else
                                {
                                    state = true;
                                }
                                for (int i = 1; i < scale.size(); i++)
                                {
                                    location = find(scale.at(i), &query);
                                    if (location < 0) // not a queried item.
                                    {
                                        if (state) // it found a queried item last.
                                        {
                                            state = false;
                                            state_transitions++;
                                        }
                                    }
                                    else
                                    {
                                        if (!state)
                                        {
                                            state = true;
                                            state_transitions++;
                                        }
                                    }
                                }
                                if (state_transitions > 2) // not continuous.
                                {
                                    matched = false;
                                }
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

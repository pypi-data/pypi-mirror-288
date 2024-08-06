#include <vector>
#include <map>
#include <string.h>
#include <cassert>
#include <cstring>
#include <algorithm>
#include <cstdint>
#include <numeric>
#include "AlignTools.h"

#define L1 0xC0
#define L2 0x30
#define L3 0x0C
#define L4 0x03
#define ori_index(i, j) l2 * (i) + j
#define arrow_index(i, j) (ori_index(i, j) )/ 4
#define arrow_stitch(i, n)  n << (6-((i) % 4)*2)

using namespace std;

namespace align
{
    class Aligner
    {
        public:
            Aligner();
            ~Aligner();
            
            int align_I(vector<int> &s1, vector<int> &s2, vector<int> &weights1, vector<int> &weights2, bool traceback, int &alignment_score, vector<int> &aln1, vector<int> &aln2);
            int align_C(vector<char> &s1, vector<char> &s2, vector<int> &weights1, vector<int> &weights2, bool traceback, int &alignment_score, vector<int> &aln1, vector<int> &aln2);
        
        private:
            
            uint8_t d_arrow(uint64_t index);
            template<class AlignType>
            int align(vector<AlignType> &s1, vector<AlignType> &s2, vector<int> &weights1, vector<int> &weights2, bool traceback, int &alignment_score, vector<int> &aln1, vector<int> &aln2);
    };

}
#include <iostream>

#include "align.h"

using namespace std;

namespace align{
    Aligner::Aligner(){
    }
    
    
    Aligner::~Aligner(){
    }
    
    // weights 为 map, 快速查询即可
    int Aligner::align_I(vector<int> &s1, vector<int> &s2, vector<int> &weights1, vector<int> &weights2, bool traceback, int &alignment_score, vector<int> &aln1, vector<int> &aln2){
        return align(s1, s2, weights1, weights2, traceback, alignment_score, aln1, aln2);
    }
    
    int Aligner::align_C(vector<char> &s1, vector<char> &s2, vector<int> &weights1, vector<int> &weights2, bool traceback, int &alignment_score, vector<int> &aln1, vector<int> &aln2){
        return align(s1, s2, weights1, weights2, traceback, alignment_score, aln1, aln2);
    }


    uint8_t Aligner::d_arrow(uint64_t index){
        switch (index % 4)
        {
        case 0:
            return L1;
            break;
        case 1:
            return L2;
        case 2:
            return L3;
        case 3:
            return L4;
        default:
            cerr<<"error arrow index: "<<index<<endl;
            exit(1);
            break;
        }
    }

    template<class AlignType>
    int Aligner::align(vector<AlignType> &s1, vector<AlignType> &s2, vector<int> &weights1, vector<int> &weights2, bool traceback, int &alignment_score, vector<int> &aln1, vector<int> &aln2){

        const uint64_t l1 = s1.size();
        const uint64_t l2 = s2.size();
        assert(l1 != 0 || l2 != 0);

        // 滚动数组，只保留当前行和上一行
        int* prev_dp = new int[l2 + 1]{0};
        int* curr_dp = new int[l2 + 1]{0};

        int* last_col = new int[l1 + 1]{0};
        // 完整的箭头矩阵，用于回溯
        uint64_t size = (l1 + 1) * (l2 + 1) / 4 + 1;
        vector<uint8_t> arrow_matrix(size, 0);
        
        int match_score, max_score, gap1_score, gap2_score;
        AlignType x1, x2;
        int w1, w2;
        for (int i = 1; i <= l1; ++i) {
            x1 = s1[i - 1];
            w1 = weights1[i - 1];
            for (int j = 1; j <= l2; ++j) {
                x2 = s2[j - 1];
                w2 = weights2[j - 1];
                match_score = (x1 == x2) ? (prev_dp[j - 1] + w1) : (prev_dp[j - 1] - max(w1, w2));
                gap1_score = prev_dp[j] - w1;
                gap2_score = curr_dp[j - 1] - w2;
                max_score = max({match_score, gap1_score, gap2_score});
                curr_dp[j] = max_score;
                
                if (gap1_score == max_score) {
                    arrow_matrix[arrow_index(i, j)] = arrow_matrix[arrow_index(i, j)] | (arrow_stitch(ori_index(i, j), 1));
                } else if (gap2_score == max_score) {
                    arrow_matrix[arrow_index(i, j)] = arrow_matrix[arrow_index(i, j)] | (arrow_stitch(ori_index(i, j), 2));
                }
            }
            last_col[i] = curr_dp[l2];
            // 交换当前行和上一行
            swap(prev_dp, curr_dp);
        }
        // Traceback to find the optimal alignment
        int* max_element_col = max_element(last_col, last_col + l1 + 1);
        int last_col_max_score = *max_element_col;
        int max_index_col = distance(last_col, max_element_col);

        int* max_element_row = max_element(prev_dp, prev_dp + l2 + 1);
        int last_row_max_score = *max_element_row;
        int max_index_row = distance(prev_dp, max_element_row);

        uint64_t i = 0, j = 0;
        if (last_col_max_score > last_row_max_score) {
            i = max_index_col;
            j = l2;
            alignment_score = last_col_max_score;
        } else {
            i = l1;
            j = max_index_row;
            alignment_score = last_row_max_score;
        }

        if (!traceback) {
            delete[] prev_dp;
            delete[] curr_dp;
            delete[] last_col;
            // delete[] arrow_matrix;
            return 0;
        }
        // 回溯路径
        bool isS1;
        int suffix = 0;
        if(i == l1){
            isS1 = false;
            suffix = l2 - j;
        }else{
            isS1 = true;
            suffix = l1 - i;
        }
        while (i > 0 && j > 0) {
            uint8_t arrow = arrow_matrix[arrow_index(i, j)] & d_arrow(ori_index(i, j));
            if (arrow == 1) {
                aln1.push_back(i - 1);
                aln2.push_back(-1);
                i -= 1;
            } else if (arrow == 2) {
                aln1.push_back(-1);
                aln2.push_back(j - 1);
                j -= 1;
            } else {
                aln1.push_back(i - 1);
                aln2.push_back(j - 1);
                i -= 1;
                j -= 1;
            }
        }
        // 处理剩余部分
        while (i > 0) {
            aln1.push_back(i - 1);
            aln2.push_back(-1);
            i -= 1;
        }
        while (j > 0) {
            aln1.push_back(-1);
            aln2.push_back(j - 1);
            j -= 1;
        }

        reverse(aln1.begin(), aln1.end());
        reverse(aln2.begin(), aln2.end());
        while(suffix > 0){
            if(isS1){
                aln1.push_back(l1-suffix);
                aln2.push_back(-1);
            }else{
                aln1.push_back(-1);
                aln2.push_back(l2-suffix);
            }
            suffix--;
        }
        // 释放内存
        delete[] prev_dp;
        delete[] curr_dp;
        delete[] last_col;
        // delete[] arrow_matrix;

        return 0;
    }
}
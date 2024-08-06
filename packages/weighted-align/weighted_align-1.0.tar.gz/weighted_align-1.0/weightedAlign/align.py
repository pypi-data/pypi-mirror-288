import sys
import os


aligner_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(aligner_path)


import Aligner


if __name__ == '__main__':
    s1 = list("ATCGACTGAG")
    s2 = list("ACATC")
    weight_char1_s1 = [1] * len('ATCGACTGAG')
    weight_char1_s2 = [1] * len('ACATC')
    
    aligner = Aligner.AlignerWrapper()
    Weighted_score, Weighted_aln1, Weighted_aln2 = aligner.align_C(s1, s2, weight_char1_s1, weight_char1_s2, True)
    print(Weighted_score)
    print(Weighted_aln1)
    print(Weighted_aln2)
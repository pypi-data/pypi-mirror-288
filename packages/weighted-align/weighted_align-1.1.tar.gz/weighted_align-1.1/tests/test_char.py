import Aligner
from unittest import TestCase, main, expectedFailure


class Tests(TestCase):

    def test1(self):
        s1 = list("ATCGACTGAG")
        s2 = list("ACATC")
        weight_char1_s1 = [1] * len(s1)
        weight_char1_s2 = [1] * len(s2)
        
        aligner = Aligner.AlignerWrapper()
        Weighted_score, Weighted_aln1, Weighted_aln2 = aligner.align_C(s1, s2, weight_char1_s1, weight_char1_s2, True)
        print(Weighted_score)
        print(Weighted_aln1)
        print(Weighted_aln2)

if __name__ == '__main__':
    main()

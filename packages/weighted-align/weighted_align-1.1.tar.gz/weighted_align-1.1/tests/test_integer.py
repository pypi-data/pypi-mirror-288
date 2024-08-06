import Aligner
from unittest import TestCase, main, expectedFailure


class Tests(TestCase):

    def test1(self):
        s1 = [1, 2, 3, 5, 4]
        s2 = [2, 3, 4]
        weight_char1_s1 = [1] * len(s1)
        weight_char1_s2 = [1] * len(s2)
        
        aligner = Aligner.AlignerWrapper()
        Weighted_score, Weighted_aln1, Weighted_aln2 = aligner.align_C(s1, s2, weight_char1_s1, weight_char1_s2, True)
        print(Weighted_score)
        print(Weighted_aln1)
        print(Weighted_aln2)

if __name__ == '__main__':
    main()

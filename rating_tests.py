import unittest
from rating import RatingCalculator, RatingPlayerResult, recalculate_ratings

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        pass

#     def test_rating_basic(self):
#         rc = RatingCalculator()
#         rc.player_results.append(RatingPlayerResult(101, False, 5000, None, 2312))
#         rc.player_results.append(RatingPlayerResult(102, False, 5000, None, 1212))
#         rc.player_results.append(RatingPlayerResult(103, False, 2222, None, 2311))
#         rc.player_results.append(RatingPlayerResult(104, False, 3333, None, 1055))
#         rc.player_results.append(RatingPlayerResult(105, False, 10000, None, 1055))
#         rc.player_results.append(RatingPlayerResult(106, True, 4444, 1, 2))
#         rc.player_results.append(RatingPlayerResult(107, True, 5555, 1, 1055))
#         rc.player_results.append(RatingPlayerResult(108, True, 2222, 1, 2055))
#         
#         new_ratings = rc.calc_and_get_new_rating_dict()
        
    def test_rating_2v2v2v2(self):
        rc = RatingCalculator()
        rc.player_results.append(RatingPlayerResult(101, True, 47840, 1, 1018))
        rc.player_results.append(RatingPlayerResult(102, True, 22585, 1, 1011))
        rc.player_results.append(RatingPlayerResult(103, False, 19968, 2, 1018))
        rc.player_results.append(RatingPlayerResult(104, False, 19464, 2, 963))
        rc.player_results.append(RatingPlayerResult(105, False, 41169, 3, 1095))
        rc.player_results.append(RatingPlayerResult(106, False, 25659, 3, 947))
        rc.player_results.append(RatingPlayerResult(107, False, 29087, 4, 1030))
        rc.player_results.append(RatingPlayerResult(108, False, 19330, 4, 975))

        new_ratings = rc.calc_and_get_new_rating_dict()
        print new_ratings

    def test_rating_2v2v2v2_example_from_prod(self):
        """
        I tought this was an bugged case because Andriod with 46k score lost more rating than Shrubber with 13k.
        But it is not, the algorithm punishes Andriod + Moderate Bot team more because they had higher total team rating.
        """
        rc = RatingCalculator()
        rc.player_results.append(RatingPlayerResult("Ballisticfire", True, 28427, 1, 1014))
        rc.player_results.append(RatingPlayerResult("Freddiefearless", True, 24741, 1, 988))
        rc.player_results.append(RatingPlayerResult("Andriod", False, 45699, 2, 1306))
        rc.player_results.append(RatingPlayerResult("Moderate Bot", False, 6153, 2, 987))
        rc.player_results.append(RatingPlayerResult("Shrubber", False, 13520, 3, 1059))
        rc.player_results.append(RatingPlayerResult("Lovefrombehind", False, 3643, 3, 870))
        rc.player_results.append(RatingPlayerResult("Slangehiet", False, 22635, 4, 961))
        rc.player_results.append(RatingPlayerResult("Harsem", False, 12127, 4, 1041))

        new_ratings = rc.calc_and_get_new_rating_dict()
        print new_ratings

    def test_rating_FFA(self):
        rc = RatingCalculator()
        rc.player_results.append(RatingPlayerResult(101, True, 47840, 1, 1018))
        rc.player_results.append(RatingPlayerResult(102, False, 22585, 2, 1011))
        rc.player_results.append(RatingPlayerResult(103, False, 19968, 3, 1018))
        rc.player_results.append(RatingPlayerResult(104, False, 19464, 4, 963))
        rc.player_results.append(RatingPlayerResult(105, False, 41169, 5, 1095))
        rc.player_results.append(RatingPlayerResult(106, False, 25659, 6, 947))
        rc.player_results.append(RatingPlayerResult(107, False, 29087, 7, 1030))
        rc.player_results.append(RatingPlayerResult(108, False, 19330, 8, 975))

        new_ratings = rc.calc_and_get_new_rating_dict()
        print new_ratings

    def test_rating_FFA3(self):
        rc = RatingCalculator()
        rc.player_results.append(RatingPlayerResult(101, True, 59861, None, 1201))
        rc.player_results.append(RatingPlayerResult(102, False, 53330, None, 947))
        rc.player_results.append(RatingPlayerResult(103, False, 40837, None, 887))
        rc.player_results.append(RatingPlayerResult(104, False, 5243, None, 978))

        new_ratings = rc.calc_and_get_new_rating_dict()
        print new_ratings

if __name__ == '__main__':
    unittest.main()
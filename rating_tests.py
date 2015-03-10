import unittest
from rating import RatingCalculator, RatingPlayerResult

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        pass
        #self.seq = range(10)

    def test_rating_basic(self):
        rc = RatingCalculator()
        rc.player_results.append(RatingPlayerResult(101, False, 5000, None, 2312))
        rc.player_results.append(RatingPlayerResult(102, False, 5000, None, 1212))
        rc.player_results.append(RatingPlayerResult(103, False, 2222, None, 2311))
        rc.player_results.append(RatingPlayerResult(104, False, 3333, None, 1055))
        rc.player_results.append(RatingPlayerResult(105, False, 10000, None, 1055))
        rc.player_results.append(RatingPlayerResult(106, True, 4444, 1, 2))
        rc.player_results.append(RatingPlayerResult(107, True, 5555, 1, 1055))
        rc.player_results.append(RatingPlayerResult(108, True, 2222, 1, 2055))
        
        new_ratings = rc.calc_and_get_new_rating_dict()
        #print new_ratings
        #self.assertEqual(new_ratings[101], 1020)
        

if __name__ == '__main__':
    unittest.main()
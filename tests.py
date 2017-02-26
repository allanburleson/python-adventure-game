import unittest
import os

import pag

class TestPlayer(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.l = pag.classes.Location('Test')
        self.l.description = 'Test description'
        self.player = pag.classes.Player(pag.classes.location_list, self.l, mute=True)
        
    def test_fist_in_inventory(self):
        self.assertTrue(self.player.inventory[0].name == 'fist')


class TestWords(unittest.TestCase):

    def test_get_word_list(self):
        test_dict_path = '.testdict'
        f = open(test_dict_path, 'w')
        f.write('t1\nt2:test2,testtwo\nt3:test3\n#test comment')
        f.close()
        wl = pag.words.get_word_list(test_dict_path)
        self.assertFalse('#test comment' in wl)
        self.assertEqual(wl['t2'][1], 'testtwo')
        os.remove(test_dict_path)
        
        
if __name__ == '__main__':
    unittest.main()

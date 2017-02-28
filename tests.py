import unittest
import os

import pag

class TestPlayer(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.l = pag.classes.Location('Test')
        self.l.description = 'Test description'
        self.l2 = pag.classes.Location('Test 2', description='t2 description')
        self.l.exits = {'north': self.l2}
        self.l2.exits = {'south': self.l}
        self.player = pag.classes.Player(pag.classes.location_list, self.l, mute=True)
        
    def test_fist_in_inventory(self):
        self.assertTrue(self.player.inventory[0].name == 'fist')
    
    def test_change_score(self):
        score = self.player.score + 1
        self.player._change_score(1)
        self.assertEqual(score, self.player.score)
        score = self.player.score - 4
        self.player._change_score(-4)
        self.assertEqual(score, self.player.score)
    
    def test_typing_error(self):
        score = self.player.score - 1
        self.player._typing_error()
        self.assertEqual(score, self.player.score)
        
    def test_can_carry(self):
        i = pag.classes.Item('test', '', '', 99)
        self.assertTrue(self.player._can_carry(i))
        i = pag.classes.Item('test', '', '', 104.347)
        self.assertFalse(self.player._can_carry(i))
        
    def test_drop_item(self):
        i = pag.classes.Item('test', '', '', 0)
        self.player.inventory.append(i)
        self.assertTrue(i in self.player.inventory)
        self.player._drop_item(i)
        self.assertTrue(i not in self.player.inventory)
        self.player.location.items.remove(i)

    def test_go(self):
        self.player.go('go', 'north')
        self.assertEqual(self.player.location, self.l2)
        self.player.go('', '', self.l)
        self.assertEqual(self.player.location, self.l)


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

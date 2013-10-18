import unittest
import morris_cm

class TestMorrisContentManager(unittest.TestCase):
    def setUp(self):
        self.cm = morris_cm.ExampleMorrisContentManager()
        self.key = self.cm.getAUsefulKey()

    def test_can_call_next(self):
        self.cm.next(self.key)

    def test_can_call_prev(self):
        self.cm.prev(self.key)

    def test_Next_After_Prev_Is_Identity(self):
        curkey = self.key
        self.assertEqual(self.key,self.cm.next(self.cm.prev(self.key)))

    def test_Prev_After_Next_Is_Identity(self):
        curkey = self.key
        self.assertEqual(self.key,self.cm.prev(self.cm.next(self.key)))
        
    def test_getHTML_seems_to_return_something(self):
        self.assertTrue(len(self.cm.getHTML(self.key)) > 0)

    def test_load_urls_from_text(self):
        text = "a\nb\n"
        self.cm.loadUrlsFromText(text)

        self.assertEqual(len(self.cm.keys),2)

        

if __name__ == '__main__':
    unittest.main()


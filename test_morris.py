import unittest
import morris

class TestMorrisDecorator(unittest.TestCase):
    
    def setUp(self):
        self.d = morris.MorrisDecorator()

    def test_canCreatePortfolio(self):
        self.d.createPortfolio("spud")
        p = self.d.getPortfolio("spud")
        self.assertTrue(p is not None)

    def test_canAddRecords(self):
        d = self.d
        d.createPortfolio("spud")
        d.addRecord("test key","test contents","spud")
        p = d.getPortfolio("spud")
        self.assertTrue("test key" in p)

    def test_canDelRecords(self):
        d = self.d
        d.createPortfolio("spud")
        key = "test key"
        d.addRecord(key,"test contents","spud")
        p = d.getPortfolio("spud")
        self.assertTrue(key in p)
        d.delRecord(key,"spud")
        p = d.getPortfolio("spud")
        self.assertFalse(key in p)

# BEGIN tests concerning scoring
    def test_CanVoteUp(self):
        d = self.d
        # Technically speaking this is better suited
        # to be a function of the content manager,
        # but we don't want to become dependent on that 
        # for this test...or do we?
        v0 = d.getRecordInteger("vote","testkey")
        rv = d.changeRecordInteger("vote","testkey",1)
        v1 = d.getRecordInteger("vote","testkey")
        self.assertEqual(int(v1),(int(v0)+1))
        self.assertEqual(int(rv),(int(v0)+1))
# END   tests concerning scoring
    
# Much more is needed to make this complete---but I am a Spiker!

if __name__ == '__main__':
    unittest.main()

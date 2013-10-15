import unittest
import morris

decoration_0 = "ThisIsADecoration"    
decoration_1 = "This is a second decoration"    
content_record_0= "http://yoyodyne"

class TestMorrisDecorator(unittest.TestCase):
    def setUp(self):
        self.d = morris.MorrisDecorator()

    def test_can_create_decorations_without_content(self):
        """ Test that we can create a decoration without content.  This corresponds to 
either an tag not yet attached to any content or an empty portfolio.
        """
        self.d.createDecorations([decoration_0])
        decorations = self.d.getAllDecorations()
        self.assertEqual(decorations[0],decoration_0)
        self.assertEqual(len(decorations),1)


    def test_can_associate_decoration_to_content(self):
        """ Test that we can decorate content (i.e., either attach tag to a content 
object or create a portfolio containing an object.
        """
        self.d.associateDecorationWithContentSingle(decoration_0,content_record_0)
        decorations_out = self.d.getDecorationsForContent(content_record_0)
        self.assertEqual(decorations_out[0],decoration_0)
        contents_out = self.d.getContentsForDecoration(decoration_0)
        self.assertEqual(contents_out[0],content_record_0)

    def test_can_associate_multiple_decorations_to_content(self):
        """ Test that we can decorate content (i.e., either attach tag to a content 
object or create a portfolio containing an object.
        """
        self.d.associateDecorationWithContentSingle(decoration_0,content_record_0)
        self.d.associateDecorationWithContentSingle(decoration_1,content_record_0)
        decorations_out = self.d.getDecorationsForContent(content_record_0)
        self.assertEqual(decorations_out[0],decoration_0)
        self.assertEqual(decorations_out[1],decoration_1)

        decorations_empty = self.d.getDecorationsForContent(content_record_0+"razmataz")
        self.assertEqual(decorations_empty,[])
        contents_out = self.d.getContentsForDecoration(decoration_0)
        self.assertEqual(contents_out[0],content_record_0)

    def test_export_decorations(self):
        self.d.associateDecorationWithContentSingle(decoration_0,content_record_0)
        all_decorations = self.d.exportDecorationsAsCSV()
        self.assertEqual(all_decorations,"Decoration\n\""+decoration_0+"\"\n")

    def test_export_contents(self):
        self.d.associateDecorationWithContentSingle(decoration_0,content_record_0)
        all_contents = self.d.exportContentsAsCSV()
        self.assertEqual(all_contents,"Content\n\""+content_record_0+"\"\n")

    def test_export_decorations_to_contents(self):
        self.d.associateDecorationWithContentSingle(decoration_0,content_record_0)
        decorations_to_contents = self.d.exportDecorationsToContentsAsCSV()
        self.assertTrue(decorations_to_contents is not None)

    def test_export_contents_to_deocrations(self):
        self.d.associateDecorationWithContentSingle(decoration_0,content_record_0)
        contents_to_decorations = self.d.exportDecorationsToContentsAsCSV()
        self.assertTrue(contents_to_decorations is not None)


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

if __name__ == '__main__':
    unittest.main()

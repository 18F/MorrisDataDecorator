import unittest
import morris
import morris_memory

decoration_0 = "ThisIsADecoration"    
decoration_1 = "This is a second decoration"    
content_record_0 = "http://yoyodyne"
content_record_1 = "http://bogodyne"

class TestMorrisDecorator(unittest.TestCase):
    def setUp(self):
        self.d = morris_memory.InMemoryMorrisDecorator()

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
         self.assertTrue(decoration_0 in decorations_out)
         contents_out = self.d.getContentsForDecoration(decoration_0)
         self.assertEqual(contents_out[0],content_record_0)

    def test_can_associate_multiple_decorations_to_content(self):
         """ Test that we can decorate content (i.e., either attach tag to a content 
 object or create a portfolio containing an object.
         """
         self.d.associateDecorationWithContentSingle(decoration_0,content_record_0)
         self.d.associateDecorationWithContentSingle(decoration_1,content_record_0)
         decorations_out = self.d.getDecorationsForContent(content_record_0)
         self.assertEqual(decorations_out[0],decoration_1)
         self.assertEqual(decorations_out[1],decoration_0)

         decorations_empty = self.d.getDecorationsForContent(content_record_0+"razmataz")
         self.assertEqual(decorations_empty,[])
         contents_out = self.d.getContentsForDecoration(decoration_0)
         self.assertEqual(contents_out[0],content_record_0)

    def test_export_decorations(self):
        self.d.deleteAll()
        self.d.createDecorations([decoration_0])
        self.d.associateDecorationWithContentSingle(decoration_0,content_record_0)
        all_decorations = self.d.exportDecorationsAsCSV()
        self.assertEqual(all_decorations,"Decoration\n\""+decoration_0+"\"\n")

    def test_export_contents(self):
        self.d.deleteAll()
        self.d.createContents([content_record_0])
        self.d.associateDecorationWithContentSingle(decoration_0,content_record_0)
        all_contents = self.d.exportContentsAsCSV()
        self.assertEqual(all_contents,"Content\n\""+content_record_0+"\"\n")

    def test_export_decorations_to_contents(self):
        self.d.associateDecorationWithContentSingle(decoration_0,content_record_0)
        decorations_to_contents = self.d.exportDecorationsToContentsAsCSV()
        expectedResult = """Decoration,Content
"ThisIsADecoration","['http://yoyodyne']"
"""
        self.assertEqual(expectedResult,decorations_to_contents)

    def test_export_contents_to_deocrations(self):
        self.d.associateDecorationWithContentSingle(decoration_0,content_record_0)
        contents_to_decorations = self.d.exportContentsToDecorationsAsCSV()
        expectedResult = """Content,Decoration
"http://yoyodyne","['ThisIsADecoration']"
"""
        self.assertEqual(expectedResult,contents_to_decorations)

    def test_export_decorations_to_contents_with_client_data(self):
        self.d.associateDecorationWithContentSingle(decoration_0,content_record_0)
        cd = "spud"
        data_name = "clientdata1"
        self.d.addClientDataDecoration(decoration_0,data_name,cd)
        self.d.addClientDataContent(content_record_0,data_name,cd)
        decorations_to_contents = self.d.exportDecorationsToContentsAsCSVWithClientDataColumns([data_name])
        expectedResult = """Decoration,Content,"clientdata1"
"ThisIsADecoration","['http://yoyodyne']","spud"
"""
        self.assertEqual(expectedResult,decorations_to_contents)

    def test_export_contents_to_deocrations_with_client_data(self):
        self.d.deleteAll()
        self.d.associateDecorationWithContentSingle(decoration_0,content_record_0)
        self.d.associateDecorationWithContentSingle(decoration_0,content_record_1)
        cd = "spud"
        data_name = "clientdata1"
        self.d.addClientDataDecoration(decoration_0,data_name,cd)
        self.d.addClientDataContent(content_record_0,data_name,cd)
        self.d.addClientDataContent(content_record_1,data_name,"bogosity")
        contents_to_decorations = self.d.exportContentsToDecorationsAsCSVWithClientDataColumns([data_name])
        expectedResult = """Content,Decoration,"clientdata1"
"http://bogodyne","['ThisIsADecoration']","bogosity"
"http://yoyodyne","['ThisIsADecoration']","spud"
"""
        self.assertEqual(expectedResult,contents_to_decorations)

    def test_export_contents_to_deocrations_with_client_data_2(self):
        self.d.deleteAll()
        self.d.associateDecorationWithContentSingle(decoration_0,content_record_0)
        self.d.associateDecorationWithContentSingle(decoration_0,content_record_1)
        cd = "spud"
        data_name = "clientdata1"
        self.d.addClientDataDecoration(decoration_0,data_name,cd)
        self.d.addClientDataContent(content_record_1,data_name,cd+"1")
        contents_to_decorations = self.d.exportContentsToDecorationsAsCSVWithClientDataColumns([data_name])
        expectedResult = """Content,Decoration,"clientdata1"
"http://bogodyne","['ThisIsADecoration']","spud1"
"http://yoyodyne","['ThisIsADecoration']"
"""
        self.assertEqual(expectedResult,contents_to_decorations)

    def test_can_add_client_data(self):
        cd = "spud"
        data_name = "clientdata1"
        self.d.addClientDataDecoration(decoration_0,data_name,cd)
        self.assertEqual(cd,self.d.getClientDataDecorationName(decoration_0,data_name))
        self.d.addClientDataContent(content_record_0,data_name,cd)
        self.assertEqual(cd,self.d.getClientDataContentName(content_record_0,data_name))

    def test_can_delete_decorations(self):
        """
First add a data decoration, implicitly creating a decoration
Remove the decoration
Make sure the association has been removed.
"""
        self.d.associateDecorationWithContentSingle(decoration_0,content_record_0)
        decorations_out = self.d.getDecorationsForContent(content_record_0)
        self.assertTrue(decoration_0 in decorations_out)
        contents_out = self.d.getContentsForDecoration(decoration_0)
        self.assertEqual(contents_out[0],content_record_0)

        # now that we have constructed that, let's delete the decoration
        # and make sure all the associations are removed.
        self.d.deleteDecorations([decoration_0])
        contents_out = self.d.getContentsForDecoration(decoration_0)
        self.assertEqual(contents_out,[])

        decorations_out = self.d.getDecorationsForContent(content_record_0)
        self.assertEqual(decorations_out,[])

    def test_get_returns_empty_list_if_uncreated(self):
        """
Here we test that we are properly making a distinction between a decoration
which doesn not exist at all (returning None) the empty results (empty list)
"""
        self.d.deleteAll();
        contentsShouldBeNone = self.d.getContentsForDecoration(decoration_0)
        self.assertEqual(len(contentsShouldBeNone),0)
        decorationsShouldBeNone = self.d.getDecorationsForContent(content_record_0)
        self.assertEqual(len(decorationsShouldBeNone), 0)
         

# # BEGIN tests concerning scoring
#     def test_CanVoteUp(self):
#         d = self.d
#         # Technically speaking this is better suited
#         # to be a function of the content manager,
#         # but we don't want to become dependent on that 
#         # for this test...or do we?
#         v0 = d.getRecordInteger("vote","testkey")
#         rv = d.changeRecordInteger("vote","testkey",1)
#         v1 = d.getRecordInteger("vote","testkey")
#         self.assertEqual(int(v1),(int(v0)+1))
#         self.assertEqual(int(rv),(int(v0)+1))
# # END   tests concerning scoring

if __name__ == '__main__':
    unittest.main()

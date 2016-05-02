from django.test import TestCase
from realestate.models import *

# Create your tests here.
class PropertyTestCase(TestCase):
    def setUp(self):
        Property.objects.create(id=1,
                                            title_text="Prachtig huisje",
                                           description_text="Zeer mooi huisje bla bla bla bla bla bla bla bla blalblalbalbleerverververververververver en blaejrvner en twee zeer mooie kzelkzeoinzepocnoenermn voaeurnvomuaervoe",
                                           address_text="Meistraat 11 2000 Antwerpen",
                                           constructiondate="1993-10-05",
                                           sellingprice=10000000,
                                           visible_to_public=True,
                                           featured=True,
                                           pub_date="2016-05-13")
        Property.objects.create(id=2,
                                            title_text="Lelijk huisje",
                                           description_text="Zeer lelijk huisje paireieor aleirnoernv aoierveni oeirnvo eaoinrv ervearv aervjbe oeurnvouern oernvoern kejr vjer  ervej rvioer er  rkj er vker rek erkj vrvke k vek ke veaù  ver",
                                           address_text="Boomgaardstraat 50 2070 Burcht",
                                           constructiondate="1950-08-04",
                                           sellingprice=500000,
                                           visible_to_public=False,
                                           featured=True,
                                           pub_date="2016-06-16")
        Property.objects.create(id=3,
                                            title_text="Gigantische villa",
                                           description_text="Gigiantische villa gelegen ten zuiden van antwerpen met 7000 slaapkamers en 80000 badkamers. Inclusief 50 tuinstoelen.",
                                           address_text="Kipdorp 11 2000 Antwerpen",
                                           constructiondate="1550-12-02",
                                           sellingprice=90005000000,
                                           visible_to_public=True,
                                           featured=False,
                                           pub_date="2016-12-12")
        Property.objects.create(id=4,
                                           title_text="Gezellig kraakpand",
                                           description_text="Gezellig kraakpand gelegen te zwijndrecht. Zeer weinig overlast buiten de gebeurlijke goa raves. ",
                                           address_text="Scoutsdam 2070 Zwijndrecht",
                                           constructiondate="1993-01-01",
                                           sellingprice=250,
                                           visible_to_public=False,
                                           featured=False,
                                           pub_date="2016-05-05")

    def test_property_visible_to_public(self):
        property1 =Property.objects.get(id=1)
        property2 =Property.objects.get(id=2)
        property3 =Property.objects.get(id=3)
        property4 =Property.objects.get(id=4)
        self.assertEqual(property1.visible_to_public, True)
        self.assertEqual(property2.visible_to_public, False)
        self.assertEqual(property3.visible_to_public, True)
        self.assertEqual(property4.visible_to_public, False)

from django.test import TestCase
from realestate.models import *

class CharacteristicTestCase(TestCase):
    def setUp(self):
        Characteristic.objects.create(id="0", name="Badkamers")
        Characteristic.objects.create(id="1", name="Slaapkamers")

    def test_characteristic_displays_name(self):
        """Characteristics display name test"""
        badkamers = Characteristic.objects.get(name="Badkamers")
        slaapkamers = Characteristic.objects.get(name="Slaapkamers")
        self.assertEqual(badkamer.__str__(self), 'Badkamers')
        self.assertEqual(badkamer.__str__(self), 'Slaapkamers')

#TODO: Finish characteristics_property testcase
class Characteristics_propertyTestCase(TestCase):
    def setUp(self):
    	Characteristic.objects.create(id="2", name="Terrassen")
        Property.objects.create(id="0",
                                title_text="Gezellig kraakpand",
                                description_text="Gezellig kraakpand gelegen te zwijndrecht. Zeer weinig overlast buiten de gebeurlijke goa raves. ",
                                address_text="Scoutsdam 2070 Zwijndrecht",
                                constructiondate="12/02/1950",
                                sellingprice=250,
                                visible_to_public=False,
                                featured=False,
                                pub_date="29/04/2016")
        Characteristics_property.create(id="0", property_id="0",characteristic_id="2", value="1 , vanvoor")

    def test_(self):
        """Animals that can speak are correctly identified"""
        badkamers = Animal.objects.get(name="Badkamers")
        slaapkamers = Animal.objects.get(name="Slaapkamers")
        self.assertEqual(badkamer.__str__(self), 'Badkamers')
        self.assertEqual(badkamer.__str__(self), 'Slaapkamers')
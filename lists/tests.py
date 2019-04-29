from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from lists.models import Item


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_uses_home_template(self):

        response = self.client.get("/")
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_home_page_can_save_a_POST_request(self):
        test_text = "A new list item"
        test_data = {"item_text": test_text}

        response = self.client.post("/", data=test_data)
        self.assertIn(test_text, response.content.decode())
        self.assertTemplateUsed(response, 'lists/home.html')


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        FIRST_TXT = "The 1st item"
        SECOND_TXT = "the 2nd item"
        first_item = Item()
        first_item.text = FIRST_TXT
        first_item.save()

        second_item = Item()
        second_item.text = SECOND_TXT
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        self.assertEqual(saved_items[0].text, FIRST_TXT)
        self.assertEqual(saved_items[1].text, SECOND_TXT)


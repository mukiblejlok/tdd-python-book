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

    def test_home_page_only_saves_items_when_necessary(self):
        self.client.get("/")
        self.assertEqual(Item.objects.count(), 0)

    def test_home_page_can_save_a_POST_request(self):
        test_text = "A new list item"
        test_data = {"item_text": test_text}

        response = self.client.post("/", data=test_data)
        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()
        self.assertEqual(new_item.text, test_text)

    def test_home_page_redirects_after_POST(self):
        test_text = "A new list item"
        test_data = {"item_text": test_text}

        response = self.client.post("/", data=test_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], "/lists/the-only-list-in-the-world/")

    # def test_home_page_displays_all_list_items(self):
    #     Item.objects.create(text='itemek 1')
    #     Item.objects.create(text='itemek 2')

    #     response = self.client.get("/")
    #     self.assertIn("itemek 1", response.content.decode())
    #     self.assertIn("itemek 2", response.content.decode())


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


class ListViewTest(TestCase):

    def test_list_view_uses_list_template(self):
        response = self.client.get("/lists/the-only-list-in-the-world/")
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_list_view_displays_all_list_items(self):
        Item.objects.create(text='itemek 1')
        Item.objects.create(text='itemek 2')

        response = self.client.get("/lists/the-only-list-in-the-world/")
        self.assertContains(response, "itemek 1")
        self.assertContains(response, "itemek 2")

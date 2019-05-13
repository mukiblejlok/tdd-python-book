from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from lists.models import Item, List


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

    # def test_home_page_displays_all_list_items(self):
    #     Item.objects.create(text='itemek 1')
    #     Item.objects.create(text='itemek 2')

    #     response = self.client.get("/")
    #     self.assertIn("itemek 1", response.content.decode())
    #     self.assertIn("itemek 2", response.content.decode())


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        FIRST_TXT = "The 1st item"
        SECOND_TXT = "the 2nd item"
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = FIRST_TXT
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = SECOND_TXT
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        self.assertEqual(saved_items[0].text, FIRST_TXT)
        self.assertEqual(saved_items[0].list, list_)
        self.assertEqual(saved_items[1].text, SECOND_TXT)
        self.assertEqual(saved_items[1].list, list_)


class ListViewTest(TestCase):

    def test_list_view_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f"/lists/{list_.id}/")
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_list_view_displays_only_correct_items(self):
        correct_list_ = List.objects.create()
        Item.objects.create(text='itemek 1', list=correct_list_)
        Item.objects.create(text='itemek 2', list=correct_list_)
        other_list_ = List.objects.create()
        Item.objects.create(text='other itemek 1', list=other_list_)
        Item.objects.create(text='other itemek 2', list=other_list_)
        response = self.client.get(f"/lists/{correct_list_.id}/")
        self.assertContains(response, "itemek 1")
        self.assertContains(response, "itemek 2")
        self.assertNotContains(response, "other itemek 1")
        self.assertNotContains(response, "other itemek 2")

    def test_list_view_passed_correct_list_to_template(self):
        other_list_ = List.objects.create()
        correct_list_ = List.objects.create()

        response = self.client.get(f'/lists/{correct_list_.id}/')
        self.assertEqual(response.context['list'], correct_list_)


class NewListTest(TestCase):

    def test_page_can_save_a_POST_request(self):
        test_text = "A new list item"
        test_data = {"item_text": test_text}

        self.client.post("/lists/new", data=test_data)
        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()
        self.assertEqual(new_item.text, test_text)

    def test_page_redirects_after_POST(self):
        test_text = "A new list item"
        test_data = {"item_text": test_text}

        response = self.client.post("/lists/new", data=test_data)
        list_ = List.objects.first()
        self.assertRedirects(response, f"/lists/{list_.id}/")


class NewItemTest(TestCase):

    def test_can_save_POST_request_to_existing_list(self):
        test_text = "A new list item"
        test_data = {"item_text": test_text}

        other_list_ = List.objects.create()
        correct_list_ = List.objects.create()


        self.client.post(f"/lists/{correct_list_.id}/add_item",
                         data=test_data)

        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().text, test_text)
        self.assertEqual(Item.objects.first().list, correct_list_)

    def test_page_redirects_after_POST(self):
        test_text = "A new list item"
        test_data = {"item_text": test_text}

        other_list_ = List.objects.create()
        correct_list_ = List.objects.create()

        response = self.client.post(f"/lists/{correct_list_.id}/add_item",
                                    data=test_data)

        self.assertRedirects(response, f"/lists/{correct_list_.id}/")
from django.test import TestCase, override_settings

from vehicle.views import cars


class MainPageTests(TestCase):
	@override_settings(ALLOWED_HOSTS=['testserver'])
	def test_main_page_renders_18_cards(self):
		response = self.client.get('/')

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['cars'], cars)
		self.assertContains(response, 'AUTO.RIA рекомендує')
		self.assertContains(response, 'class="card"', count=18)
		self.assertNotContains(response, '{header}')

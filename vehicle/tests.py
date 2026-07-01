from django.test import TestCase, override_settings

from .views import car


class CardViewTests(TestCase):
	@override_settings(ALLOWED_HOSTS=['testserver'])
	def test_card_view_renders_car_data(self):
		response = self.client.get('/card/')

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['car'], car)
		self.assertContains(response, 'Mark 2 100')
		self.assertContains(response, '6000 $')
		self.assertContains(response, 'Одеса')
		self.assertNotContains(response, 'Данные для карточки не найдены.')
		self.assertNotContains(response, '{{car.Model}}')

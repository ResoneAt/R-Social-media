from django.utils.deprecation import MiddlewareMixin


class CustomMiddleware(MiddlewareMixin):
    def process_template_response(self, request, response):
        custom_data = {
            'key1': 'value1',
            'key2': 'value2',
        }
        print('helooooooooooooooooooooooooooooooooooooooooooooooooooooooooo')
        response.context_data['custom_data'] = custom_data
        return response



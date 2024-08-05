import uvicorn
import time
import threading
import requests
import os
from loguru import logger
from openai import OpenAI
from datetime import datetime

class APIFixer:
    def __init__(self, **kwargs):
        self.resource = kwargs.get('resource', 'main:app')
        self.host = kwargs.get('host', '127.0.0.1')
        self.port = kwargs.get('port', 8000)
        self.openai_api_key = kwargs.get('openai_api_key')

        self.base_url = f'http://{self.host}:{self.port}'

    def __stop(self) -> None:
        try:
            self.server.should_exit = True
        except Exception as e:
            logger.error(str(e))

    def __generate_api_doc(self, paths):
        try: 
            if not self.openai_api_key:
                logger.error('Missing OPENAI_API_KEY in env!')
                return

            openai_client = OpenAI(api_key=self.openai_api_key)
            completion = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert technical writer specialized in API documentation."},
                    {"role": "user", "content": f"Generate a detailed API documentation based on the following API paths:\n\n{paths}"}
                ]
            )

            result = completion.choices[0].message.content
            with open('./API_DOC.txt', 'w') as f:
                f.write(result)

        except Exception as e:
            logger.error(str(e))

    def __generate_template(self, parameter_type):
        templates = {
            'string': '',
            'integer': 0,
            'array': [],
            'number': 0.00
        }
        return templates.get(parameter_type, None)

    def __do_record(self, message) -> None:
        now = datetime.now()
        created_at = now.strftime('%d.%m.%Y, %H:%M:%S')

        with open('./logs.txt', 'a') as f:
            f.write(f'{message} ({created_at})\n')

    def __request(self, url, method, headers={}, data={}, info_message=None):
        response_json = {'status': 'error', 'err_description': ''}
        if info_message:
            self.__do_record(info_message)

        try:
            request = requests.request(method, url=url, headers=headers, data=data)
            if request.status_code not in [200, 201, 301, 302]:
                err_description = f'ERROR: {request.status_code}: {url}, {method}'
                self.__do_record(err_description)
                response_json['err_description'] = err_description
                return response_json

            self.__do_record(f'SUCCESS: {request.status_code}: {url}, {method}')

            if 'openapi.json' in url:
                response_json['response'] = request.json()

            response_json['status'] = 'success'

        except requests.exceptions.RequestException as e:
            logger.error(str(e))
            response_json['err_description'] = str(e)
        
        except ValueError as e:
            logger.error(str(e))
            response_json['err_description'] = str(e)

        return response_json

    def __route_checker(self, auto_close_server) -> None:
        try:
            time.sleep(2)
            base_url = self.base_url

            api_request = self.__request(f'{base_url}/openapi.json', 'GET')
            if api_request['status'] == 'success':
                response = api_request.get('response', {})
                paths = response.get('paths', {})

                if paths:
                    th = threading.Thread(target=self.__generate_api_doc, args=(paths,))
                    th.start()
                    time.sleep(3)

                    for path, methods_dict in paths.items():
                        for method in methods_dict.keys():
                            headers = {}
                            data = {}
                            url = f'{base_url}{path}?'

                            parameters = methods_dict[method].get('parameters', [])
                            request_body = methods_dict[method].get('requestBody', {})
                            if parameters:
                                for parameter in parameters:
                                    name = parameter['name']
                                    parameter_type = parameter['schema']['type']
                                    template = self.__generate_template(parameter_type)
                                    parameter_method = parameter['in']

                                    if parameter_method == 'query':
                                        url += f'&{name}={template}'
                                    elif parameter_method == 'body':
                                        data[name] = template

                            args = [url, method.upper(), headers, data]
                            if request_body:
                                info_message = f'INFO: required Form parameters must to be no required and have all important exceptions: {url}, {method}'
                                args.append(info_message)

                            time.sleep(1)
                            th = threading.Thread(target=self.__request, args=args)
                            th.start()

            if auto_close_server:
                self.__stop()

        except Exception as e:
            logger.error(str(e))

    def run(self, **kwargs) -> None:
        try:
            auto_close_server = kwargs.get('auto_close_server', None)
            th = threading.Thread(target=self.__route_checker, args=(auto_close_server, ))
            th.start()

            config = uvicorn.Config(self.resource, host=self.host, port=self.port, reload=True)
            self.server = uvicorn.Server(config)
            self.server.run()

        except Exception as e:
            logger.error(str(e))

import sys
import os
import time
import requests
import contextlib
from concurrent import futures


@contextlib.contextmanager
def finish_time():
    start_time = time.time()
    yield
    print(f'Finished in %.2fs' % (time.time() - start_time))




class Browse:
    def __init__(self, **kwargs):
        self.target = kwargs['target']
        self.words = kwargs['words']
        self.config = kwargs['config']
        self.count = 0
        self.found = 0

    def request(self, payload):
        url = self.target.format(payload)
        try:
            with requests.get(url, timeout=self.config['timeout'], headers=self.config['headers']) as result:
                return {'response_code': result.status_code, 'url': url}
        except requests.exceptions.ConnectTimeout:
            return {'response_code': 408, 'url': url}


    def launch(self):
        with finish_time():
            if not os.path.exists('logs/'):
                os.mkdir('logs')
            with open(f'logs/{round(time.time())}.log', 'w+') as log:
                with futures.ThreadPoolExecutor(max_workers=self.config['threads']) as executor:
                    for response in futures.as_completed([executor.submit(self.request, payload) for payload in self.words]):
                        self.count += 1
                        result = response.result()
                        log.write('[{}] {}\n'.format(result['response_code'], result['url']))
                        if result['response_code'] in self.config['response-codes']:
                            print('[{}] {}'.format(result['response_code'], result['url']))
                            self.found += 1
                        print(f'Checked {self.count}/{len(self.words)} | Found {self.found}', end='\r')
                        sys.stdout.flush()
                    print('\n')
                    log.close()

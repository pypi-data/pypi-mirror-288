import requests
import time

server = "https://api.csolver.xyz"

class Solver:
    def __init__(self, api_key):
        self.api_key = api_key

    def solve(self, task, sitekey, site, proxy=None, rqdata=None):
        endpoint = f'{server}/solve'
        headers = {'API-Key': self.api_key}
        payload = {
            'task': task,
            'sitekey': sitekey,
            'site': site,
            'proxy': proxy,
            'rqdata': rqdata
        }

        start = time.time()
        response = requests.post(endpoint, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            job_id = data.get('job_id')

            if job_id:
                result = self.CSolver_Result(job_id, headers)
                if result:
                    end = time.time()
                    elapsed = end - start
                    e = round(elapsed, 2)
                    return result
                else:
                    end = time.time()
                    elapsed = end - start
                    e = round(elapsed, 2)
                    return None
            else:
                return None
        else:
            return None

    def CSolver_Result(self, job_id, headers):
        result_endpoint = f'{server}/result/{job_id}'
        while True:
            response = requests.get(result_endpoint, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if 'status' in data and data['status'] == 'completed':
                    return data['solution']
                elif data.get('status') == 'processing':
                    time.sleep(5) 
                elif data.get('status') == 'failed':
                    return None
            else:
                return None
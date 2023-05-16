import requests
import time
# from requests.exceptions import HTTPError


class ReedExtractor:
    '''Class for scraping the Reed jobs API.
    '''
    def __init__(self, api_key):
        '''
        Args:
        ----
        api_key     : str -> Reed API key
        '''

        self.listings = []
        self.details = []
        self.auth_header = requests.auth.HTTPBasicAuth(api_key, "")
        self.api_key = api_key
        self.request_count = 0
        self.start_time = None

    def _check_limit(self):
        '''
        The API has a limit of 2000 requests per hour.
        Method sleeps the extractor for the difference between
        an hour and the time spent pulling.
        '''

        if self.request_count == 1900:
            time_spent = time.time() - self.start_time
            if time_spent < 3600:
                time_rest = 3600 - time_spent
                time.sleep(time_rest + 60)
                self.request_count = 0
                self.start_time = time.time()

    def get_listings(self, keywords):
        '''
        Get all listings for given keywords string.
        Update listings attribute with list of listings.
        Args:
        ----
        keywords        : str -> space seperated keywords
        '''

        listings = []
        endpoint = "https://www.reed.co.uk/api/1.0/search"
        keywords = keywords.replace(' ', '%20')
        start_url = f"{endpoint}?keywords={keywords}"
        self.start_time = time.time()
        r = requests.get(start_url, auth=self.auth_header)
        self.request_count += 1
        r.raise_for_status()
        response_json = r.json()
        results = response_json['results']
        listings.append(results)
        count = response_json['totalResults']
        for idx in range(100, count, 100):
            print(idx)
            url = f"{start_url}&resultsToSkip={idx}"
            r = requests.get(url, auth=self.auth_header)
            r.raise_for_status()
            response_json = r.json()
            results = response_json['results']
            listings.append(results)
            self.request_count += 1
            time.sleep(3)
            self._check_limit()
        self.listings = [job for page in listings for job in page]

    def get_details(self):
        '''
        Get details for jobs in the listings attribute.
        '''

        endpoint = "https://www.reed.co.uk/api/1.0/jobs"
        if not self.listings:
            raise Exception('No listings to get details of.')
        i = 0
        for job in self.listings:
            if i % 100 == 0:
                print(i)
            id = job['jobId']
            url = f"{endpoint}/{id}"
            r = requests.get(url, auth=self.auth_header)
            r.raise_for_status()
            self.details.append(r.json())
            i += 1
            self.request_count += 1
            time.sleep(1)
            self._check_limit()

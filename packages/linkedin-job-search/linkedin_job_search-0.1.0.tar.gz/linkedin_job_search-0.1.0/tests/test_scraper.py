# tests/test_scraper.py

import unittest
from linkedin_search_job.scraper import scrape_jobs

class TestJobScraper(unittest.TestCase):
    def test_scrape_jobs(self):
        jobs = scrape_jobs()
        self.assertIsInstance(jobs, list)
        if jobs:
            self.assertIn('title', jobs[0])
            self.assertIn('company', jobs[0])
            self.assertIn('location', jobs[0])
            self.assertIn('job_link', jobs[0])

if __name__ == '__main__':
    unittest.main()

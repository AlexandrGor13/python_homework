import unittest
from multiprocessing import Value
import logging

from memc_load_multithreading import (
    AppsInstalled,
    parse_appsinstalled,
    insert_appsinstalled,
    process_fd,
)

logging.basicConfig(level=logging.DEBUG)


class TestAppsinstalled(unittest.TestCase):
    def test_parse_appsinstalled_valid_data(self):
        valid_line = b'gaid\t48c80bf59f951aaec39352292e72894a\t-4.43971979975\t-3.67509218856\t3938,5604'
        result = parse_appsinstalled(valid_line)
        expected_result = AppsInstalled(
            dev_type='gaid',
            dev_id='48c80bf59f951aaec39352292e72894a',
            lat=-4.43971979975,
            lon=-3.67509218856,
            apps=[3938, 5604]
        )
        self.assertEqual(result, expected_result)

    def test_insert_appsinstalled_success(self):
        appsinstalled = AppsInstalled(
            dev_type='gaid',
            dev_id='test_device_id',
            lat=-4.43971979975,
            lon=-3.67509218856,
            apps=[3938, 5604]
        )
        memc_addr = '127.0.0.1:33013'
        result = insert_appsinstalled(memc_addr, appsinstalled, dry_run=True)
        self.assertTrue(result)

    def test_process_fd_with_dry_run(self):
        lines = [
            b'gaid\t48c80bf59f951aaec39352292e72894a\t-4.43971979975\t-3.67509218856\t3938,5604',
            b'gaid\tinvalid_device_id\t-4.43971979975\t-3.67509218856\t3938,5604'
        ]
        processed = Value('i', 0)
        errors = Value('i', 0)
        device_memc = {'gaid': '127.0.0.1:33014'}
        process_fd(processed, errors, device_memc, lines, dry_run=True)
        self.assertEqual(processed.value, 2)
        self.assertEqual(errors.value, 0)


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3

import os
import unittest
import sys

SEARCH_VULNS_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(1, SEARCH_VULNS_PATH)
import search_vulns

class TestSearches(unittest.TestCase):

    def test_search_cve_ghsa_ids1(self):
        self.maxDiff = None
        query = 'CVE-2024-27286, GHSA-hfjr-m75m-wmh7, CVE-2024-12345678'
        result = search_vulns.search_vulns(query)
        expected_vulns = {'CVE-2024-27286': {'published': '2024-03-20 20:15:08', 'cvss_ver': '3.1', 'cvss': '6.5', 'cvss_vec': 'CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N', 'cisa_known_exploited': False}, 'CVE-2024-12345678': {'published': '', 'cvss_ver': '', 'cvss': '-1.0', 'cvss_vec': '', 'cisa_known_exploited': False}, 'GHSA-hfjr-m75m-wmh7': {'published': '2022-05-24 16:59:38', 'cvss_ver': '3.1', 'cvss': '7.8', 'cvss_vec': 'CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H'}}
        self.assertEqual(set(expected_vulns.keys()), set(result[query]['vulns'].keys()))
        for vuln_id, vuln_attrs in result[query]['vulns'].items():
            self.assertEqual(vuln_attrs['published'], expected_vulns[vuln_id]['published'])
            self.assertEqual(vuln_attrs['cvss_ver'], expected_vulns[vuln_id]['cvss_ver'])
            self.assertEqual(vuln_attrs['cvss'], expected_vulns[vuln_id]['cvss'])
            self.assertEqual(vuln_attrs['cvss_vec'], expected_vulns[vuln_id]['cvss_vec'])
            if 'cisa_known_exploited' in vuln_attrs or 'cisa_known_exploited' in expected_vulns[vuln_id]:
                self.assertEqual(vuln_attrs['cisa_known_exploited'], expected_vulns[vuln_id]['cisa_known_exploited'])

    def test_search_cve_ghsa_ids2(self):
        self.maxDiff = None
        # GHSA-6c3j-c64m-qhgq should be deduplicated to CVE-2019-11358
        query = 'CVE-2015-9251 ;;asd GHSA-6c3j-c64m-qhgq iuhnd CVE-2019-11358 .121w CVE-2007-2379'
        result = search_vulns.search_vulns(query)
        expected_vulns = {'CVE-2015-9251': {'published': '2018-01-18 23:29:00', 'cvss_ver': '3.0', 'cvss': '6.1', 'cvss_vec': 'CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N', 'cisa_known_exploited': False}, 'CVE-2019-11358': {'published': '2019-04-20 00:29:00', 'cvss_ver': '3.1', 'cvss': '6.1', 'cvss_vec': 'CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N', 'cisa_known_exploited': False}, 'CVE-2007-2379': {'published': '2007-04-30 23:19:00', 'cvss_ver': '2.0', 'cvss': '5.0', 'cvss_vec': 'AV:N/AC:L/Au:N/C:P/I:N/A:N', 'cisa_known_exploited': False}}
        self.assertEqual(set(expected_vulns.keys()), set(result[query]['vulns'].keys()))
        for vuln_id, vuln_attrs in result[query]['vulns'].items():
            self.assertEqual(vuln_attrs['published'], expected_vulns[vuln_id]['published'])
            self.assertEqual(vuln_attrs['cvss_ver'], expected_vulns[vuln_id]['cvss_ver'])
            self.assertEqual(vuln_attrs['cvss'], expected_vulns[vuln_id]['cvss'])
            self.assertEqual(vuln_attrs['cvss_vec'], expected_vulns[vuln_id]['cvss_vec'])
            if 'cisa_known_exploited' in vuln_attrs or 'cisa_known_exploited' in expected_vulns[vuln_id]:
                self.assertEqual(vuln_attrs['cisa_known_exploited'], expected_vulns[vuln_id]['cisa_known_exploited'])


if __name__ == '__main__':
    unittest.main()

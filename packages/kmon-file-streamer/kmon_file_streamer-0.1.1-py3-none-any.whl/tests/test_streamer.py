import json
import unittest, time
from kmon.kmsf_stream import kmsf_data_stream

class TestDataStreamService(unittest.TestCase):
    def test_data_stream(self):
        count=0
        for json_obj in kmsf_data_stream("kmon-datalake-prod",
                     "compress/kmon_v1_raw_specif/2024-01-15/kmon_v1_raw_specif_2024-01-15_43450.tar.gz",
                                         {"clazz": "RC-textile_fabricProductionStatus"}):
            count+=1
        print("Total count: ", count)
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
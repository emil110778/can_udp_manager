import unittest
from unittest.mock import patch, Mock

import can_transport

class TestDecode(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.data_fixtures = ((b'\x07\x00\x00\x00\x01\x02', (True, 0, True, True, b'\x01\x02')),
                              (b'\x05\x00\x00\x00\x01\x02', (True, 0, False, True, b'\x01\x02')),
                              (b'\x03\x00\x00\x00\x01\x02', (True, 0, True, False, b'\x01\x02')),
                              (b'\x01\x00\x00\x00\x01\x02', (True, 0, False, False, b'\x01\x02')),
                              (b'\x00\x00\x01\x02', (False, 0, False, False, b'\x01\x02')),
                              (b'\x02\x00\x01\x02', (False, 0, True, False, b'\x01\x02')),
                              (b'\x04\x00\x01\x02', (False, 0, False, True, b'\x01\x02')),
                              (b'\x06\x00\x01\x02', (False, 0, True, True, b'\x01\x02')),
                              (b'\xFE\x3F\x01\x02', (False, 0x7FF, True, True, b'\x01\x02')),
                              (b'\xFF\xFF\xFF\xFF\x01\x02', (True, 0x1FFFFFFF, True, True, b'\x01\x02')),
                              (b'\xFF\xFF\xFF\xFF\x01\x02\x03\x04\x05\x06\x07\x08', (True, 0x1FFFFFFF, True, True, b'\x01\x02\x03\x04\x05\x06\x07\x08')),
                              (b'\xFF\xFF\xFF\xFF', (True, 0x1FFFFFFF, True, True, b'')),
                             )

    @patch.object(can_transport.Vcan_socket, "__init__")
    def test_decode_data_error(self, mock_init):
        
        mock_init.return_value = None

        new_can_transport = can_transport.Vcan_socket()

        result = new_can_transport.decode_data(b'\x00')

        self.assertEqual(result, None)

    @patch.object(can_transport.Vcan_socket, "__init__")
    def test_decode_data(self, mock_init):
        mock_init.return_value = None

        new_can_transport = can_transport.Vcan_socket()

        for data in self.data_fixtures:
            result = new_can_transport.decode_data(data[0])
            self.assertEqual(result, data[1])


    @patch.object(can_transport.Vcan_socket, "__init__")
    def test_encode_data(self, mock_init):
        mock_init.return_value = None

        new_can_transport = can_transport.Vcan_socket()

        for data in self.data_fixtures:
            result = new_can_transport.encode_data(*data[1])
            self.assertEqual(result, data[0])
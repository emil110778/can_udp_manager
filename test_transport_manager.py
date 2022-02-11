import unittest
from unittest.mock import patch, Mock
from unittest import IsolatedAsyncioTestCase
import asyncio

import main
import transport


async def listen_data_value():
        return b'\x07\x00\x00\x00\x01\x02'


async def send_data_ret():
        return None

class TestListener(IsolatedAsyncioTestCase):
    
    @patch ('transport.Transport')
    @patch ('transport.Transport')
    @patch ('transport.Transport')
    @patch ('transport.Transport')
    async def test_listener(self, mock_to_listen, *mocks_to_send):

        mock_to_listen.listen_data.return_value = listen_data_value()
        for transport in mocks_to_send:
            transport.send_data.return_value = send_data_ret()

        new_transport_manager = main.Transport_manager()

        for transport in mocks_to_send:
            new_transport_manager.transport_list.append(transport)

        await new_transport_manager.listener(mock_to_listen, 1)

        mock_to_listen.listen_data.assert_called_once()

        for transport in mocks_to_send:
            transport.send_data.assert_called_once_with(b'\x07\x00\x00\x00\x01\x02')


    
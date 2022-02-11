import can
import asyncio

from transport import Transport

class Vcan_socket (Transport):
    """Class for work with vcan has asynchronous functions for work with vcan.
    Contain functions for encode and decode can massage to byte array."""

    def __init__(self, can_port: str = 'vcan0'):
        """
        Args:
            can_port (str, optional): vcan port. Defaults to 'vcan0'.
        """
        self.port = can_port
        try:
            self.bus = can.interface.Bus(self.port, bustype = 'socketcan')
        except:
            print("can't create bus for can: {}".format(self.port))
    
    def encode_data(self, arbitration_id_type: bool, arbitration_id: int, is_remote_frame: bool, is_error_frame: bool, data: bytes):
        """Function for encoded can data to byte array

        Args:
            arbitration_id_type (bool): type of arbitration_id: True - 29 bit, False - 11 bit
            arbitration_id (int): massage id
            is_remote_frame (bool): data request flag
            is_error_frame (bool): error massage flag
            data (bytes): payload data

        Returns:
            [bytes]: encoded data to byte array
        """

        ret = list(data)

        ret.insert(0, (arbitration_id_type | (is_remote_frame << 1) | (is_error_frame << 2) | ((arbitration_id & 0b11111) << 3)))
        ret.insert(1, (arbitration_id >> 5) & 0xFF)

        if arbitration_id_type:
            ret.insert(2, (arbitration_id >> (5 + 8)) & 0xFF)
            ret.insert(3, (arbitration_id >> (5 + 8*2)) & 0xFF)

        return bytes(ret)

    def decode_data(self, data: bytes):
        """Function for decode data

        Args:
            data (bytes): encoded data

        Returns:
            if decode success
            [parsed data]: data format to: arbitration_id_type, arbitration_id, is_remote_frame, is_error_frame, data
            else
            [parsed data]: None
        """
        data = list(data)

        arbitration_id_type = bool(data[0] & 0b1)
        is_remote_frame = bool(data[0] & 0b10)
        is_error_frame = bool(data[0] & 0b100)
        try:
            arbitration_id = data.pop(0) >> 3
            arbitration_id |= data.pop(0) << 5
        
            if arbitration_id_type:
                arbitration_id |= data.pop(0) << (5 + 8)
                arbitration_id |= data.pop(0) << (5 + 8 * 2)

            return  arbitration_id_type, arbitration_id, is_remote_frame, is_error_frame, bytes(data)
        except:
            return None

    async def send_data(self, data: bytes):
        """Function for sending data to can bus

        Args:
            data (bytes): encoded data for send to can bus
        """

        arbitration_id_type, arbitration_id, is_remote_frame, is_error_frame, data = self.decode_data(data)
        try:
            massage = can.Message(is_extended_id = arbitration_id_type, 
                arbitration_id = arbitration_id, 
                data = data, 
                is_remote_frame = is_remote_frame, 
                is_error_frame = is_error_frame)
            self.bus.send(massage)
        except:
            print("can't send to can: {}".format(self.port))
        

    
    async def listen_data(self):
        """Asynchronous function for received data from can bus

        Returns:
            [bytes]: !check returns to None, if bus has't data return None, else return encoded data
        """
        try:
            message = self.bus.recv(timeout = 0)
            ret = message if message == None else self.encode_data(arbitration_id_type = message.is_extended_id, 
                arbitration_id = message.arbitration_id, 
                is_remote_frame = message.is_remote_frame, 
                is_error_frame = message.is_error_frame, 
                data = message.data)

            await asyncio.sleep(0.1)
            return ret
        except:
            print("can't receive from can: {}".format(self.port))
            await asyncio.sleep(10)

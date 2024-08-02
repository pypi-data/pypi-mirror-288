import logging
import asyncio

class SDS_Connector:

    def __init__(self, parent):
        self._log = logging.getLogger(f"{__name__}.{__class__.__name__}")
        #: The parent :class:`SDS_Base` class to perform connections for.
        self.parent = parent
        #: String describing the connection to the device, for example IP address.
        self.connection_name = "Unknown"
        #: Class such as :class:`asyncio.StreamReader` used to read data from the SDS using an asynchronous write() method.
        self.reader = None
        #: Class such as :class:`asyncio.StreamWriter` used to write data to the SDS using an asynchronous read() method.
        self.writer = None

    async def open_connection(self):
        """
        Coroutine to establish connection to the device.

        In :class:`SDS_Connector` class, this method does nothing. It is up to a sub-class to
        determine the type of connection to make (e.g. network socket, USB). The sub-class should
        make the connection and set values for the :data:`connection_name`, :data:`reader`, and
        :data:`writer` properties.

        The :data:`connection_name` should be a string describing the connection, such as IP
        address. The :data:`reader` and :data:`writer` properties should point to instances of
        asynchronous stream reader and writers, such as :class:`asyncio.StreamReader` and
        :class:`asyncio.StreamWriter`.

        Once the connection is established, the implementation of this coroutine should then call
        ``await self.parent._handle_comms()`` to the pass control to the communications coroutine.
        """
        self._log.warning(
            "SDS_Connector base class does not implement a connection method, no device communication will occur."
        )


class SDS_Socket_Connector(SDS_Connector):
    """
    Class for a Siglent SDS oscilloscope connected via a network socket.

    :param host: IP address or hostname for the device.
    :param port: Port for raw TCP connections to the device.
    :param buffer_size: Size of read buffer.
    """

    def __init__(self, parent, host="10.42.0.59", port=5025, buffer_size=2**27):
        super().__init__(parent)
        self._log = logging.getLogger(f"{__name__}.{__class__.__name__}")
        self._host = host
        self._port = int(port)
        self._buffer_size = int(buffer_size)

    async def open_connection(self):
        """
        Coroutine to attempt to connect to a socket server.
        """
        first_attempt = True
        while True:
            if first_attempt:
                self._log.info(f"Connecting to server at {self._host}:{self._port}.")
                first_attempt = False
            try:
                self.reader, self.writer = await asyncio.open_connection(
                    host=self._host, port=self._port, limit=self._buffer_size
                )
            except Exception:
                self._log.debug("Unable to connect to server, will retry.")
                await asyncio.sleep(5.0)
            else:
                # Connection established, let the base class handle communications from here
                self.connection_name = self.writer.get_extra_info("peername")
                await self.parent._handle_comms()
                self._log.info("Connection lost, will retry.")
                first_attempt = True

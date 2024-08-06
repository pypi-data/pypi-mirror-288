from __future__ import annotations

from deephaven.plugin.object_type import MessageStream
from typing import Literal
import nbformat as nbf
from traitlets.config import Config
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert import HTMLExporter

CELL_CONVERTERS = {
    "markdown": nbf.v4.new_markdown_cell,
    "code": nbf.v4.new_code_cell,
}

notebook_type = list[dict[str, str]]

class DeephavenPluginNotebookObject:
    """
    This is a simple object that demonstrates how to send messages to the client.
    When the object is created, it will be passed a connection to the client.
    This connection can be used to send messages back to the client.

    Attributes:
        _connection: MessageStream: The connection to the client
    """
    def __init__(self, notebook: notebook_type):
        self._connection: MessageStream = None
        self._html_body = None
        self._create_notebook(notebook)

    def _send_notebook(self) -> None:
        """
        Send a message to the client

        Args:
            message: The message to send
        """
        if self._connection:
            self._connection.send_message(self._html_body)

    def _set_connection(self, connection: MessageStream) -> None:
        """
        Set the connection to the client.
        This is called on the object when it is created.

        Args:
            connection: The connection to the client
        """
        self._connection = connection


    def _create_notebook(self, notebook: notebook_type) -> None:
        nb = nbf.v4.new_notebook()
        nb['cells'] = [CELL_CONVERTERS[cell['type']](cell['source']) for cell in notebook]

        # execute the notebook
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        ep.preprocess(nb)

        # convert the notebook to html
        html_exporter = HTMLExporter()
        (body, resources) = html_exporter.from_notebook_node(nb)

        self._html_body = body
        self.resources = resources





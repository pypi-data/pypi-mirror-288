# -*- coding: utf-8 -*-
from typing import Optional, Any

from pip_services4_commons.errors import ConfigException
from pip_services4_components.config import IConfigurable, ConfigParams
from pip_services4_components.context import IContext, ContextResolver
from pip_services4_components.refer import IReferenceable, IReferences
from pip_services4_config.auth import CredentialResolver, CredentialParams
from pip_services4_config.connect import ConnectionResolver, ConnectionParams


class MqttConnectionResolver(IReferenceable, IConfigurable):
    """
    Helper class that resolves MQTT connection and credential parameters,
    validates them and generates connection options.

    - connection(s):
        - discovery_key:               (optional) a key to retrieve the connection from :class:`IDiscovery <pip_services4_config.connect.IDiscovery.IDiscovery>`
        - host:                        host name or IP address
        - port:                        port number
        - uri:                         resource URI or connection string with all parameters in it
    - credential(s):
        - store_key:                   (optional) a key to retrieve the credentials from :class:`ICredentialStore <pip_services4_config.auth.ICredentialStore.ICredentialStore>`
        - username:                    user name
        - password:                    user password

    ### References ###

        - `*:discovery:*:*:1.0`          (optional) :class:`IDiscovery <pip_services4_config.connect.IDiscovery.IDiscovery>` services to resolve connections
        - `*:credential-store:*:*:1.0`   (optional) Credential stores to resolve credentials

    Example:

    .. code-block:: python

        TODO: add example
    """

    def __init__(self):
        # The connections resolver.
        self._connection_resolver: ConnectionResolver = ConnectionResolver()
        # The credentials resolver.
        self._credential_resolver: CredentialResolver = CredentialResolver()

    def configure(self, config: ConfigParams):
        """
        Configures component by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        self._connection_resolver.configure(config)
        self._credential_resolver.configure(config)

    def set_references(self, references: IReferences):
        """
        Sets references to dependent components.

        :param references: references to locate the component dependencies.
        """
        self._connection_resolver.set_references(references)
        self._credential_resolver.set_references(references)

    def __validate_connection(self, context: Optional[IContext], connection: ConnectionParams):
        if connection is None:
            raise ConfigException(
                ContextResolver.get_trace_id(context),
                "NO_CONNECTION",
                "MQTT connection is not set"
            )

        uri = connection.get_uri()
        if uri is not None:
            return

        protocol = connection.get_as_string_with_default("protocol", "mqtt")
        if protocol is None:
            raise ConfigException(
                ContextResolver.get_trace_id(context),
                "NO_PROTOCOL",
                "Connection protocol is not set"
            )

        host = connection.get_host()
        if host is None:
            raise ConfigException(
                ContextResolver.get_trace_id(context),
                "NO_HOST",
                "Connection host is not set"
            )

        port = connection.get_as_integer_with_default('port', 1883)
        if port == 0:
            raise ConfigException(
                ContextResolver.get_trace_id(context),
                "NO_PORT",
                "Connection port is not set"
            )

    def __compose_options(self, connection: ConnectionParams, credential: CredentialParams) -> Any:
        # Define additional parameters parameters
        options = connection.override(credential)

        # Compose uri
        if options.get_as_nullable_string('uri') is None:
            protocol = connection.get_as_string_with_default("protocol", "mqtt")
            host = connection.get_host()
            port = connection.get_as_integer_with_default("port", 1883)
            uri = f'{protocol}://{host}:{port}'
            options.set_as_object('uri', uri)

        return options.get_as_object()

    def resolve(self, context: Optional[IContext]) -> Any:
        """
        Resolves MQTT connection options from connection and credential parameters.

        :param context: (optional) transaction id to trace execution through call chain.
        :return: resolved MQTT connection options.
        """
        connection = self._connection_resolver.resolve(context)
        # Validate connections
        self.__validate_connection(context, connection)

        credential = self._credential_resolver.lookup(context)
        # Credentials are not validated right now

        options = self.__compose_options(connection, credential)
        return options

    def compose(self, context: Optional[IContext], connection: ConnectionParams, credential: CredentialParams) -> Any:
        """
        Composes MQTT connection options from connection and credential parameters.

        :param context: (optional) transaction id to trace execution through call chain.
        :param connection: connection parameters
        :param credential: credential parameters
        :return: resolved MQTT connection options.
        """
        # Validate connections
        self.__validate_connection(context, connection)

        options = self.__compose_options(connection, credential)
        return options

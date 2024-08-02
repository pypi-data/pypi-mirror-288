"""
Type annotations for ssm-quicksetup service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_quicksetup/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_ssm_quicksetup.client import SystemsManagerQuickSetupClient

    session = Session()
    client: SystemsManagerQuickSetupClient = session.client("ssm-quicksetup")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type

from botocore.client import BaseClient, ClientMeta

from .paginator import ListConfigurationManagersPaginator
from .type_defs import (
    ConfigurationDefinitionInputTypeDef,
    CreateConfigurationManagerOutputTypeDef,
    EmptyResponseMetadataTypeDef,
    FilterTypeDef,
    GetConfigurationManagerOutputTypeDef,
    GetServiceSettingsOutputTypeDef,
    ListConfigurationManagersOutputTypeDef,
    ListQuickSetupTypesOutputTypeDef,
    ListTagsForResourceResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("SystemsManagerQuickSetupClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class SystemsManagerQuickSetupClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-quicksetup.html#SystemsManagerQuickSetup.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_quicksetup/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SystemsManagerQuickSetupClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-quicksetup.html#SystemsManagerQuickSetup.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_quicksetup/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-quicksetup.html#SystemsManagerQuickSetup.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_quicksetup/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-quicksetup.html#SystemsManagerQuickSetup.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_quicksetup/client/#close)
        """

    def create_configuration_manager(
        self,
        *,
        ConfigurationDefinitions: Sequence[ConfigurationDefinitionInputTypeDef],
        Description: str = ...,
        Name: str = ...,
        Tags: Mapping[str, str] = ...,
    ) -> CreateConfigurationManagerOutputTypeDef:
        """
        Creates a Quick Setup configuration manager resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-quicksetup.html#SystemsManagerQuickSetup.Client.create_configuration_manager)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_quicksetup/client/#create_configuration_manager)
        """

    def delete_configuration_manager(self, *, ManagerArn: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a configuration manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-quicksetup.html#SystemsManagerQuickSetup.Client.delete_configuration_manager)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_quicksetup/client/#delete_configuration_manager)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-quicksetup.html#SystemsManagerQuickSetup.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_quicksetup/client/#generate_presigned_url)
        """

    def get_configuration_manager(self, *, ManagerArn: str) -> GetConfigurationManagerOutputTypeDef:
        """
        Returns a configuration manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-quicksetup.html#SystemsManagerQuickSetup.Client.get_configuration_manager)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_quicksetup/client/#get_configuration_manager)
        """

    def get_service_settings(self) -> GetServiceSettingsOutputTypeDef:
        """
        Returns settings configured for Quick Setup in the requesting Amazon Web
        Services account and Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-quicksetup.html#SystemsManagerQuickSetup.Client.get_service_settings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_quicksetup/client/#get_service_settings)
        """

    def list_configuration_managers(
        self,
        *,
        Filters: Sequence[FilterTypeDef] = ...,
        MaxItems: int = ...,
        StartingToken: str = ...,
    ) -> ListConfigurationManagersOutputTypeDef:
        """
        Returns Quick Setup configuration managers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-quicksetup.html#SystemsManagerQuickSetup.Client.list_configuration_managers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_quicksetup/client/#list_configuration_managers)
        """

    def list_quick_setup_types(self) -> ListQuickSetupTypesOutputTypeDef:
        """
        Returns the available Quick Setup types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-quicksetup.html#SystemsManagerQuickSetup.Client.list_quick_setup_types)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_quicksetup/client/#list_quick_setup_types)
        """

    def list_tags_for_resource(self, *, ResourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Returns tags assigned to the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-quicksetup.html#SystemsManagerQuickSetup.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_quicksetup/client/#list_tags_for_resource)
        """

    def tag_resource(
        self, *, ResourceArn: str, Tags: Mapping[str, str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Assigns key-value pairs of metadata to Amazon Web Services resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-quicksetup.html#SystemsManagerQuickSetup.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_quicksetup/client/#tag_resource)
        """

    def untag_resource(
        self, *, ResourceArn: str, TagKeys: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-quicksetup.html#SystemsManagerQuickSetup.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_quicksetup/client/#untag_resource)
        """

    def update_configuration_definition(
        self,
        *,
        Id: str,
        ManagerArn: str,
        LocalDeploymentAdministrationRoleArn: str = ...,
        LocalDeploymentExecutionRoleName: str = ...,
        Parameters: Mapping[str, str] = ...,
        TypeVersion: str = ...,
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a Quick Setup configuration definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-quicksetup.html#SystemsManagerQuickSetup.Client.update_configuration_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_quicksetup/client/#update_configuration_definition)
        """

    def update_configuration_manager(
        self, *, ManagerArn: str, Description: str = ..., Name: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a Quick Setup configuration manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-quicksetup.html#SystemsManagerQuickSetup.Client.update_configuration_manager)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_quicksetup/client/#update_configuration_manager)
        """

    def update_service_settings(
        self, *, ExplorerEnablingRoleArn: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates settings configured for Quick Setup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-quicksetup.html#SystemsManagerQuickSetup.Client.update_service_settings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_quicksetup/client/#update_service_settings)
        """

    def get_paginator(
        self, operation_name: Literal["list_configuration_managers"]
    ) -> ListConfigurationManagersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-quicksetup.html#SystemsManagerQuickSetup.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_quicksetup/client/#get_paginator)
        """

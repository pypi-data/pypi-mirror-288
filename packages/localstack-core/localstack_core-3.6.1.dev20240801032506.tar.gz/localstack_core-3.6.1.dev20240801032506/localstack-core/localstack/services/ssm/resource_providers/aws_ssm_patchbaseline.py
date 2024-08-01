# LocalStack Resource Provider Scaffolding v2
from __future__ import annotations

from pathlib import Path
from typing import Optional, TypedDict

import localstack.services.cloudformation.provider_utils as util
from localstack.services.cloudformation.resource_provider import (
    OperationStatus,
    ProgressEvent,
    ResourceProvider,
    ResourceRequest,
)


class SSMPatchBaselineProperties(TypedDict):
    Name: Optional[str]
    ApprovalRules: Optional[RuleGroup]
    ApprovedPatches: Optional[list[str]]
    ApprovedPatchesComplianceLevel: Optional[str]
    ApprovedPatchesEnableNonSecurity: Optional[bool]
    Description: Optional[str]
    GlobalFilters: Optional[PatchFilterGroup]
    Id: Optional[str]
    OperatingSystem: Optional[str]
    PatchGroups: Optional[list[str]]
    RejectedPatches: Optional[list[str]]
    RejectedPatchesAction: Optional[str]
    Sources: Optional[list[PatchSource]]
    Tags: Optional[list[Tag]]


class PatchFilter(TypedDict):
    Key: Optional[str]
    Values: Optional[list[str]]


class PatchFilterGroup(TypedDict):
    PatchFilters: Optional[list[PatchFilter]]


class Rule(TypedDict):
    ApproveAfterDays: Optional[int]
    ApproveUntilDate: Optional[dict]
    ComplianceLevel: Optional[str]
    EnableNonSecurity: Optional[bool]
    PatchFilterGroup: Optional[PatchFilterGroup]


class RuleGroup(TypedDict):
    PatchRules: Optional[list[Rule]]


class PatchSource(TypedDict):
    Configuration: Optional[str]
    Name: Optional[str]
    Products: Optional[list[str]]


class Tag(TypedDict):
    Key: Optional[str]
    Value: Optional[str]


REPEATED_INVOCATION = "repeated_invocation"


class SSMPatchBaselineProvider(ResourceProvider[SSMPatchBaselineProperties]):
    TYPE = "AWS::SSM::PatchBaseline"  # Autogenerated. Don't change
    SCHEMA = util.get_schema_path(Path(__file__))  # Autogenerated. Don't change

    def create(
        self,
        request: ResourceRequest[SSMPatchBaselineProperties],
    ) -> ProgressEvent[SSMPatchBaselineProperties]:
        """
        Create a new resource.

        Primary identifier fields:
          - /properties/Id

        Required properties:
          - Name

        Create-only properties:
          - /properties/OperatingSystem

        Read-only properties:
          - /properties/Id



        """
        model = request.desired_state
        ssm = request.aws_client_factory.ssm

        params = util.select_attributes(
            model=model,
            params=[
                "OperatingSystem",
                "Name",
                "GlobalFilters",
                "ApprovalRules",
                "ApprovedPatches",
                "ApprovedPatchesComplianceLevel",
                "ApprovedPatchesEnableNonSecurity",
                "RejectedPatches",
                "RejectedPatchesAction",
                "Description",
                "Sources",
                "ClientToken",
                "Tags",
            ],
        )

        response = ssm.create_patch_baseline(**params)
        model["Id"] = response["BaselineId"]

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def read(
        self,
        request: ResourceRequest[SSMPatchBaselineProperties],
    ) -> ProgressEvent[SSMPatchBaselineProperties]:
        """
        Fetch resource information


        """
        raise NotImplementedError

    def delete(
        self,
        request: ResourceRequest[SSMPatchBaselineProperties],
    ) -> ProgressEvent[SSMPatchBaselineProperties]:
        """
        Delete a resource


        """
        model = request.desired_state
        ssm = request.aws_client_factory.ssm

        ssm.delete_patch_baseline(BaselineId=model["Id"])

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def update(
        self,
        request: ResourceRequest[SSMPatchBaselineProperties],
    ) -> ProgressEvent[SSMPatchBaselineProperties]:
        """
        Update a resource


        """
        raise NotImplementedError

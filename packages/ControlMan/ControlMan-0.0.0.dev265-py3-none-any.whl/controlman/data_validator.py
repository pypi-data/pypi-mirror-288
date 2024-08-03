from typing import Literal as _Literal
from pathlib import Path as _Path
import copy
import re as _re

import jsonschema as _jsonschema
import referencing as _referencing
from referencing import jsonschema as _referencing_jsonschema
import pkgdata as _pkgdata
from loggerman import logger as _logger
import pyserials as _ps

from controlman import exception as _exception
from controlman import _file_util


_schema_dir_path = _pkgdata.get_package_path_from_caller(top_level=True) / "_data" / "schema"


def validate(
    data: dict,
    schema: _Literal["full", "local", "cache"] = "full",
    before_substitution: bool = False,
    raise_invalid_data: bool = True,
) -> None:
    """Validate data against a schema."""
    schema_dict = _file_util.read_data_from_file(
        path=_schema_dir_path / f"{schema}.yaml",
        extension="yaml",
        raise_errors=True,
    )
    schema_dict = put_required_at_bottom(schema_dict)
    if before_substitution:
        schema_dict = modify_schema(schema_dict)["anyOf"][0]
    try:
        _ps.validate.jsonschema(
            data=data,
            schema=schema_dict,
            validator=_jsonschema.Draft202012Validator,
            registry=_registry_before if before_substitution else _registry_after,
            fill_defaults=True,
            raise_invalid_data=raise_invalid_data,
        )
    except _ps.exception.validate.PySerialsSchemaValidationError as e:
        raise _exception.ControlManSchemaValidationError(
            msg="Validation against schema failed."
        ) from e
    if not before_substitution:
        DataValidator(data).validate()
    return


class DataValidator:
    def __init__(self, data: dict):
        self._ccm = data
        return

    @_logger.sectioner("Validate Control Center Contents")
    def validate(self):
        # self.branch_names()
        # self.changelogs()
        # self.commits()
        # self.issue_forms()
        # self.labels()
        return

    def dir_paths(self):
        paths = []
        path_keys = []
        for dirpath_key in (
            "control.path",
            "local.path",
            "theme.path",
            "pkg.path.root",
            "test.path.root",
            "web.path.root",
        ):
            if self._ccm[dirpath_key]:
                path_keys.append(dirpath_key)
                paths.append(_Path(self._ccm[dirpath_key]))
        for idx, path in enumerate(paths):
            for idx2, path2 in enumerate(paths[idx + 1:]):
                if path.is_relative_to(path2):
                    main_path = path2
                    rel_path = path
                    main_key = path_keys[idx + idx2 + 1]
                    rel_key = path_keys[idx]
                elif path2.is_relative_to(path):
                    main_path = path
                    rel_path = path2
                    main_key = path_keys[idx]
                    rel_key = path_keys[idx + idx2 + 1]
                else:
                    continue
                raise _exception.ControlManSchemaValidationError(
                    f"Directory path '{rel_path}' defined at '{rel_key}' is relative to"
                    f"directory path '{main_path}' defined at '{main_key}'.",
                    key=rel_key,
                )
        return

    def branch_names(self):
        """Verify that branch names and prefixes are unique."""
        checked_branch_names = []
        for branch_key, branch_data in self._ccm["branch"].items():
            branch_name = branch_data["name"]
            for checked_branch_name in checked_branch_names:
                if checked_branch_name.startswith(branch_name):
                    raise _exception.ControlManSchemaValidationError(
                        msg=(
                            f"Branch prefix '{branch_name}' for branch type '{branch_key}' "
                            f"conflicts with another branch name/prefix: '{checked_branch_name}'"
                        ),
                        key=f"branch.{branch_key}"
                    )
            checked_branch_names.append(branch_data)
        return

    def changelogs(self):
        """Verify that changelog paths, names and sections are unique."""
        changelog_paths = []
        changelog_names = []
        for changelog_id, changelog_data in self._ccm["changelog"].items():
            if changelog_data["path"] in changelog_paths:
                raise _exception.ControlManSchemaValidationError(
                    f"The path '{changelog_data['path']}' set for changelog '{changelog_id}' "
                    f"is already used by another earlier changelog.",
                    key=f"changelog.{changelog_id}.path"
                )
            changelog_paths.append(changelog_data["path"])
            if changelog_data["name"] in changelog_names:
                raise _exception.ControlManSchemaValidationError(
                    f"The name '{changelog_data['name']}' set for changelog '{changelog_id}' "
                    f"is already used by another earlier changelog.",
                    key=f"changelog.{changelog_id}.name"
                )
            changelog_names.append(changelog_data["name"])
            # if changelog_id == "package_public_prerelease": #TODO: check package_public_prerelease
            #     continue
            section_ids = []
            for idx, section in enumerate(changelog_data.get("sections", [])):
                if section["id"] in section_ids:
                    raise _exception.ControlManSchemaValidationError(
                        f"The changelog section ID '{section['id']}' set for changelog '{changelog_id}' "
                        f"is already used by another earlier section.",
                        key=f"changelog.{changelog_id}.sections[{idx}]"
                    )
                section_ids.append(section["id"])
        return

    def commits(self):
        """Verify that commit types are unique, and that subtypes are defined."""
        commit_types = []
        for main_type in ("primary", "primary_custom"):
            for commit_id, commit_data in self._ccm["commit"][main_type].items():
                if commit_data["type"] in commit_types:
                    raise _exception.ControlManSchemaValidationError(
                        f"The commit type '{commit_data['type']}' set for commit '{main_type}.{commit_id}' "
                        f"is already used by another earlier commit.",
                        key=f"commit.{main_type}.{commit_id}.type"
                    )
                commit_types.append(commit_data["type"])
                for subtype_type, subtypes in commit_data["subtypes"]:
                    for subtype in subtypes:
                        if subtype not in self._ccm["commit"]["secondary_custom"]:
                            _logger.critical(
                                title=f"Invalid commit subtype: {subtype}",
                                msg=f"The subtype '{subtype}' set for commit '{main_type}.{commit_id}' "
                                f"in 'subtypes.{subtype_type}' is not defined in 'commit.secondary_custom'.",
                            )
        for commit_id, commit_data in self._ccm["commit"]["secondary_action"].items():
            if commit_data["type"] in commit_types:
                _logger.critical(
                    title=f"Duplicate commit type: {commit_data['type']}",
                    msg=f"The type '{commit_data['type']}' set for commit 'secondary_action.{commit_id}' "
                    f"is already used by another earlier commit.",
                )
            commit_types.append(commit_data["type"])
        changelog_sections = {}
        for commit_type, commit_data in self._ccm["commit"]["secondary_custom"].items():
            if commit_type in commit_types:
                _logger.critical(
                    title=f"Duplicate commit type: {commit_type}",
                    msg=f"The type '{commit_type}' set in 'secondary_custom' "
                    f"is already used by another earlier commit.",
                )
            commit_types.append(commit_type)
            # Verify that linked changelogs are defined
            changelog_id = commit_data["changelog_id"]
            if changelog_id not in self._ccm["changelog"]:
                _logger.critical(
                    title=f"Invalid commit changelog ID: {changelog_id}",
                    msg=f"The changelog ID '{changelog_id}' set for commit "
                    f"'secondary_custom.{commit_type}' is not defined in 'changelog'.",
                )
            if changelog_id not in changelog_sections:
                changelog_sections[changelog_id] = [
                    section["id"] for section in self._ccm["changelog"][changelog_id]["sections"]
                ]
            if commit_data["changelog_section_id"] not in changelog_sections[changelog_id]:
                _logger.critical(
                    title=f"Invalid commit changelog section ID: {commit_data['changelog_section_id']}",
                    msg=f"The changelog section ID '{commit_data['changelog_section_id']}' set for commit "
                    f"'secondary_custom.{commit_type}' is not defined in 'changelog.{changelog_id}.sections'.",
                )
        return

    def issue_forms(self):
        form_ids = []
        form_identifying_labels = []
        for form_idx, form in enumerate(self._ccm["issue"]["forms"]):
            if form["id"] in form_ids:
                _logger.critical(
                    title=f"Duplicate issue-form ID: {form['id']}",
                    msg=f"The issue-form number {form_idx} has an ID that is already used by another earlier form.",
                )
            form_ids.append(form["id"])
            identifying_labels = (form["primary_type"], form.get("subtype"))
            if identifying_labels in form_identifying_labels:
                _logger.critical(
                    title=f"Duplicate issue-form identifying labels: {identifying_labels}",
                    msg=f"The issue-form number {form_idx} has the same identifying labels as another earlier form.",
                )
            form_identifying_labels.append(identifying_labels)
            element_ids = []
            element_labels = []
            for elem_idx, elem in enumerate(form["body"]):
                if elem["type"] == "markdown":
                    continue
                elem_id = elem.get("id")
                if elem_id:
                    if elem_id in element_ids:
                        _logger.critical(
                            title=f"Duplicate issue-form body-element ID: {elem_id}",
                            msg=f"The element number {elem_idx} has an ID that is "
                            f"already used by another earlier element.",
                        )
                    else:
                        element_ids.append(elem["id"])
                if elem["attributes"]["label"] in element_labels:
                    _logger.critical(
                        title=f"Duplicate issue-form body-element label: {elem['attributes']['label']}",
                        msg=f"The element number {elem_idx} has a label that is already used by another earlier element.",
                    )
                element_labels.append(elem["attributes"]["label"])
            if not any(element_id in ("version", "branch") for element_id in element_ids):
                _logger.critical(
                    title=f"Missing issue-form body-element: version or branch",
                    msg=f"The issue-form number {form_idx} is missing a body-element "
                    f"with ID 'version' or 'branch'.",
                )
            form_post_process = form.get("post_process")
            if form_post_process:
                if form_post_process.get("body"):
                    pattern = r"{([a-zA-Z_][a-zA-Z0-9_]*)}"
                    var_names = _re.findall(pattern, form_post_process["body"])
                    for var_name in var_names:
                        if var_name not in element_ids:
                            _logger.critical(
                                title=f"Unknown issue-form post-process body variable: {var_name}",
                                msg=f"The variable '{var_name}' is not a valid element ID within the issue body.",
                            )
                assign_creator = form_post_process.get("assign_creator")
                if assign_creator:
                    if_checkbox = assign_creator.get("if_checkbox")
                    if if_checkbox:
                        if if_checkbox["id"] not in element_ids:
                            _logger.critical(
                                title=f"Unknown issue-form post-process assign_creator if_checkbox ID: {if_checkbox}",
                                msg=f"The ID '{if_checkbox}' is not a valid element ID within the issue body.",
                            )
                        for elem in form["body"]:
                            elem_id = elem.get("id")
                            if elem_id and elem_id == if_checkbox["id"]:
                                if elem["type"] != "checkboxes":
                                    _logger.critical(
                                        title=f"Invalid issue-form post-process assign_creator if_checkbox ID: {if_checkbox}",
                                        msg=f"The ID '{if_checkbox}' is not a checkbox element.",
                                    )
                                if len(elem["attributes"]["options"]) < if_checkbox["number"]:
                                    _logger.critical(
                                        title=f"Invalid issue-form post-process assign_creator if_checkbox number: {if_checkbox}",
                                        msg=f"The number '{if_checkbox['number']}' is greater than the number of "
                                        f"checkbox options.",
                                    )
                                break
        # Verify that identifying labels are defined in 'label.group' metadata
        for primary_type_id, subtype_id in form_identifying_labels:
            if primary_type_id not in self._ccm["label"]["group"]["primary_type"]["labels"]:
                _logger.critical(
                    title=f"Unknown issue-form `primary_type`: {primary_type_id}",
                    msg=f"The ID '{primary_type_id}' does not exist in 'label.group.primary_type.labels'.",
                )
            if subtype_id and subtype_id not in self._ccm["label"]["group"]["subtype"]["labels"]:
                _logger.critical(
                    title=f"Unknown issue-form subtype: {subtype_id}",
                    msg=f"The ID '{subtype_id}' does not exist in 'label.group.subtype.labels'.",
                )
        return

    def labels(self):
        """Verify that label names and prefixes are unique."""
        labels = []
        for main_type in ("auto_group", "group", "single"):
            for label_id, label_data in self._ccm["label"].get(main_type, {}).items():
                label = label_data["name"] if main_type == "single" else label_data["prefix"]
                label_type = "name" if main_type == "single" else "prefix"
                for set_label in labels:
                    if set_label.startswith(label) or label.startswith(set_label):
                        _logger.critical(
                            title=f"Ambiguous label {label_type}: {label}",
                            msg=f"The {label_type} '{label}' set for label '{main_type}.{label_id}' "
                            f"is ambiguous as it overlaps with the already set name/prefix '{set_label}'.",
                        )
                labels.append(label)
        if len(labels) > 1000:
            _logger.critical(
                title=f"Too many labels: {len(labels)}",
                msg=f"The maximum number of labels allowed by GitHub is 1000.",
            )
        for label_id, label_data in self._ccm["label"]["group"].items():
            suffixes = []
            for label_type, suffix_data in label_data["labels"].items():
                suffix = suffix_data["suffix"]
                if suffix in suffixes:
                    _logger.critical(
                        title=f"Duplicate label suffix: {suffix}",
                        msg=f"The suffix '{suffix}' set for label 'group.{label_id}.labels.{label_type}' "
                        f"is already used by another earlier label.",
                    )
                suffixes.append(suffix)
        return

    def maintainers(self):
        issue_ids = [issue["id"] for issue in self._ccm.issue__forms]
        for issue_id in self._ccm.maintainer__issue.keys():
            if issue_id not in issue_ids:
                _logger.critical(
                    f"Issue ID '{issue_id}' defined in 'maintainer.issue' but not found in 'issue.forms'."
                )
        return


def modify_schema(schema: dict) -> dict:
    if "properties" in schema:
        for key, subschema in schema["properties"].items():
            schema["properties"][key] = modify_schema(subschema)
    if "additionalProperties" in schema and isinstance(schema["additionalProperties"], dict):
        schema["additionalProperties"] = modify_schema(schema["additionalProperties"])
    if "items" in schema and isinstance(schema["items"], dict):
        schema["items"] = modify_schema(schema["items"])
    alt_schema = {
        "type": "string",
        "minLength": 6,
    }
    new_schema = {"anyOf": [schema, alt_schema]}
    if "default" in schema:
        # If the schema has a default value, add it to the new schema,
        # otherwise it is not filled when inside an 'anyOf' clause.
        new_schema["default"] = schema["default"]
    return new_schema


def put_required_at_bottom(schema: dict) -> dict:
    """Modify JSON schema to recursively put all 'required' fields at the end.

    This is done because otherwise the 'required' fields
    are checked by jsonschema before filling the defaults,
    which can cause the validation to fail.

    Returns
    -------
    dict
        Modified schema.
        Note that the input schema is modified in-place,
        so the return value is a reference to the (now modified) input schema.
    """
    if "required" in schema:
        schema["required"] = schema.pop("required")
    for key in ["anyOf", "allOf", "oneOf"]:
        if key in schema:
            for subschema in schema[key]:
                put_required_at_bottom(subschema)
    for key in ["if", "then", "else", "not", "items", "additionalProperties"]:
        if key in schema and isinstance(schema[key], dict):
            put_required_at_bottom(schema[key])
    if "properties" in schema and isinstance(schema["properties"], dict):
        for subschema in schema["properties"].values():
            put_required_at_bottom(subschema)
    return schema


def _make_registry():
    ref_resources_after = []
    ref_resources_before = []
    def_schemas_path = _schema_dir_path / "def"
    for def_schema_filepath in def_schemas_path.glob("**/*.yaml"):
        def_schema_key = def_schema_filepath.relative_to(
            def_schemas_path
        ).with_suffix("").as_posix().replace("/", "-")
        def_schema_dict = _file_util.read_data_from_file(
            path=def_schema_filepath,
            extension="yaml",
            raise_errors=True,
        )
        def_schema_dict_after = put_required_at_bottom(def_schema_dict)
        def_schema_dict_before = modify_schema(copy.deepcopy(def_schema_dict_after))
        def_schema_before_parsed = _referencing.Resource.from_contents(
            def_schema_dict_before, default_specification=_referencing_jsonschema.DRAFT202012
        )
        def_schema_after_parsed = _referencing.Resource.from_contents(
            def_schema_dict, default_specification=_referencing_jsonschema.DRAFT202012
        )
        ref_resources_before.append((def_schema_key, def_schema_before_parsed))
        ref_resources_after.append((def_schema_key, def_schema_after_parsed))
    registry_before = _referencing.Registry().with_resources(ref_resources_before)
    registry_after = _referencing.Registry().with_resources(ref_resources_after)
    return registry_before, registry_after


_registry_before, _registry_after = _make_registry()


"""- [] Confirm the presence of all required tables within the database schem."""
import pytest
from django.db import models
from inventory.models import Category


def test_model_structure_table_exists():
    try:
        from inventory.models import Category
    except ImportError:
        assert False
    else:
        assert True


"""- [] Validate the existence of expected columns in each table, ensuring correct data types."""

@pytest.mark.parametrize(
    "model, field_name, expected_type",
    [
        (Category, "id", models.AutoField),
        (Category, "name", models.CharField),
        (Category, "slug", models.SlugField),
        (Category, "is_active", models.BooleanField),
        (Category, "level", models.IntegerField),
        (Category, "parent", models.ForeignKey),
    ],
    )
def test_model_structure_column_data_types(model, field_name, expected_type):
    assert hasattr(
        model, field_name
    ), f"{model.__name__} model does not have '{field_name} field"

    field = model._meta.get_field(field_name)

    assert isinstance(
        field, expected_type
    ), f"{field} Field is not type '{expected_type} type"


# """- [] Verify nullable or not nullable fields."""

# """- [] Test columns with specific constraints to ensure they are accurately defined."""

# """- [] Verify the correctnes of default values for relevant columns."""

# """- [] Ensure that column lengths align with defined requirements."""

# """- [] Test columns with specific constraints to ensure they are accurately defined"""

""" [] Ensure that column relationships are correctly defined """

@pytest.mark.parametrize(
    "model, field_name, expected_type, related_model, on_delete_behavior, allow_null, allow_blank",
    [
        (Category, "parent", models.ForeignKey, Category, models.PROTECT, True, True),
    ],
    )
def test_model_structure_relationship(
    model, 
    field_name, 
    expected_type, 
    related_model, 
    on_delete_behavior, 
    allow_null, 
    allow_blank
    ):
    # Variables to define the model and field properties

    assert hasattr(
        model, field_name
    ), f"{model.__name__} model does not have '{field_name} field"

    field = model._meta.get_field(field_name)

    assert isinstance(
        field, expected_type
    ), f"{field} Field is not type '{expected_type} type"

    assert (field.related_model == related_model)

    assert (
        field.remote_field.on_delete == on_delete_behavior
    ), f"{field_name} field does not have on_delete={on_delete_behavior}"

    assert (
        field.null == allow_null
    ), f"{field_name} field does not allow null values as expected"

    assert (
        field.blank == allow_blank
    ), f"{field_name} field does not allow blank field as expected"




@pytest.mark.parametrize(
    "model, field_name, expected_nullable",
    [
        (Category, "id", False),
        (Category, "name", False),
        (Category, "slug", False),
        (Category, "is_active", False),
        (Category, "level", False),
    ],
    )
def test_model_structure_nullable_constraints(model, field_name, expected_nullable):
    # Get the field from the model
    field = model._meta.get_field(field_name)

    # Check if the nullable constraint matches the expected value
    assert  (
        field.null is expected_nullable
    ), f"Field {field_name} has unexpected nullable constraint"



@pytest.mark.parametrize(
    "model, field_name, expected_default_value",
    [
        (Category, "is_active", False),
        (Category, "level", 100),
    ],
    )
def test_model_structure_default_values(model, field_name, expected_default_value):
    # Get the field from the model
    field = model._meta.get_field(field_name)

    default_value = field.default

    # Check if the nullable constraint matches the expected value
    assert  (
        default_value is expected_default_value
    ), f"Field {field_name} has unexpected default value"


@pytest.mark.parametrize(
    "model, field_name, expected_length",
    [
        (Category, "name", 100),
        (Category, "slug", 120),
    ],
    )
def test_model_structure_column_length(model, field_name, expected_length):
    # Get the field from the model
    field = model._meta.get_field(field_name)

    # Check if the default value matches the expected value
    assert  (
        field.max_length == expected_length
    ), f"Field {field_name} has unexpected different length"



@pytest.mark.parametrize(
    "model, field_name, is_unique",
    [
        (Category, "id", True),
        (Category, "name", True),
        (Category, "slug", True),
        (Category, "is_active", False),
        (Category, "level", False),
    ],
    )
def test_model_structure_is_unique_fields(model, field_name, is_unique):
    # Get the field from the model
    field = model._meta.get_field(field_name)

    # Check if the default value matches the expected value
    assert  (
        field.unique == is_unique
    ), f"Field {field_name} does not have unique value"
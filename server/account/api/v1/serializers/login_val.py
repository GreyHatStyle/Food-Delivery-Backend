from rest_framework import serializers


class LoginValidation(serializers.Serializer):
    username = serializers.CharField(
        max_length=32,
        required=True,
        help_text="Username must not exceed 32 characters.",
        error_messages={
            "max_length": "Username must not exceed 32 characters.",
            "required": "Username is required",
            "blank": "Username cannot be empty",
        },
    )

    password = serializers.CharField(
        max_length=32,
        required=True,
        write_only=True,
        help_text="Password must not exceed 32 characters",
        error_messages={
            "max_length": "Password must not exceed 32 characters.",
            "required": "Password is required",
            "blank": "Password cannot be empty",
        },
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.allowed_fields = set(self.fields.keys())
        print("Self.allowed fields: ", self.allowed_fields)

    def to_internal_value(self, data):
        """
        basically check if their is any extra field other than `username` and `password`
        """
        if isinstance(data, dict):
            extra_fields = set(data.keys()) - self.allowed_fields
            if extra_fields:
                raise serializers.ValidationError(
                    {
                        # Added list here so that self.show_first_error can index it
                        "extra_fields": [
                            f'Please remove extra fields: {", ".join(extra_fields)}'
                        ],
                    }
                )

        return super().to_internal_value(data)

    def validate_username(self, value: str):
        name = value.strip()
        if not name:
            raise serializers.ValidationError("Username cannot be empty.")

        return name

    def validate_password(self, value: str):
        if not value:
            raise serializers.ValidationError("Password cannot be empty.")

        return value

    def show_first_error(self) -> str:
        """
        Traverse through error dictionary and finds first error to display to user
        """
        errors = self.errors
        first_message: str = ""

        for field in errors:
            first_message = errors[field][0]
            break

        return first_message

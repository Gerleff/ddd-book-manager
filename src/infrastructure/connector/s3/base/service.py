"""S3 вспомогательные функции."""


def create_bucket_policy(bucket_name: str) -> dict:
    """Настройка корзины."""
    return {
        # Version: http://docs.aws.amazon.com/IAM/latest/UserGuide/AccessPolicyLanguage_ElementDescriptions.html#Version
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AddPerm",
                "Effect": "Allow",
                "Principal": "*",
                "Action": ["s3:GetObject"],
                "Resource": f"arn:aws:s3:::{bucket_name}/*",
            },
        ],
    }


def create_expiration_rule(path: str, days: int, is_active: bool = True) -> dict:
    """Политика хранения файлов."""
    return {
        "Filter": {"Prefix": path},
        "Expiration": {"Days": days},
        "Status": "Enabled" if is_active else "Disabled",
    }

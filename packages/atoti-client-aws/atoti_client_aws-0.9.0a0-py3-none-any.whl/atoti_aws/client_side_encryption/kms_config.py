from typing import final

from atoti._pydantic import PYDANTIC_CONFIG as _PYDANTIC_CONFIG
from pydantic.dataclasses import dataclass

from ._config import ClientSideEncryptionConfig


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class KmsConfig(ClientSideEncryptionConfig):
    """KMS config to use for `client side encryption <https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingClientSideEncryption.html>`__.

    The AWS KMS CMK must have been created in the same AWS region as the destination bucket (Cf. `AWS documentation <https://docs.aws.amazon.com/AmazonS3/latest/dev/replication-config-for-kms-objects.html>`__).

    Note:
        Due to `a bug in Amazon's encryption library <https://github.com/aws/amazon-s3-encryption-client-java/issues/302>`__, the :attr:`region` must also be passed either through the ``AWS_REGION`` environment variable or by adding `-Daws.region` to the :attr:`~atoti.SessionConfig.java_options`.

    Example:
        >>> from atoti_aws import KmsConfig
        >>> client_side_encryption = KmsConfig(
        ...     region="eu-west-3",
        ...     key_id="key_id",
        ... )
    """

    key_id: str
    """The ID to identify the key in KMS."""

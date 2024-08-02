import json

from allotropy.parser_factory import Vendor
from allotropy.testing.utils import from_file

file_name = "softmax_error_unique.txt"

test_filepath = f"../tests/parsers/moldev_softmax_pro/testdata/{file_name}"
allotrope_dict = from_file(test_filepath, Vendor.MOLDEV_SOFTMAX_PRO, "chardet")

print(json.dumps(allotrope_dict, indent=4, ensure_ascii=False))  # noqa: T201

import json

from allotropy.parser_factory import Vendor
from allotropy.to_allotrope import allotrope_from_file

if __name__ == "__main__":
    for output_file in ("input_test",):
        test_filepath = (
            f"../tests/parsers/moldev_softmax_pro/testdata/{output_file}.txt"
        )
        allotrope_dict = allotrope_from_file(test_filepath, Vendor.MOLDEV_SOFTMAX_PRO)
        print(json.dumps(allotrope_dict, indent=4, ensure_ascii=False))  # noqa: T201

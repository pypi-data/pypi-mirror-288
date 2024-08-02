from winsay.winsay import create_parser
import sys

def test_create_parser():
    parser = create_parser()
    sys.argv=["say", "hello"]
    args = parser.parse_args()
    assert args.text == ["hello"]
    assert args.input is None

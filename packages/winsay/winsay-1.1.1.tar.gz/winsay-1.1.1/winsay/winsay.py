from __future__ import print_function

import argparse
import win32com.client as wincl

speaker = wincl.Dispatch("SAPI.SpVoice")

def say(text):
    try:
        speaker.Speak(text)
    except Exception as ex:
        print("Error in speaking: {} with this error{} ".format(text, ex))


def main():
    """
    Say in windows
    """
    parser = create_parser()

    args = parser.parse_args()
    if args.input:
        content = open(args.input).read()
        say(content)

    if args.text:
        sentence = " ".join(args.text)
        say(sentence)

def create_parser():
    parser = argparse.ArgumentParser(description="Say in windows")
    parser.add_argument("text", type=str, nargs="*",
                        help="sentence to speak", default="")
    parser.add_argument("-i", "--input", type=str,
                        help="Text File to speak", default=None)
                        
    return parser


if __name__ == "__main__":
    main()

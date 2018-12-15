import argparse


def get_parser():
    parser = argparse.ArgumentParser(
        prog='HackDay2018_Backend',
        usage='python main.py -f "feature_name"',
        description='This module demonstrates image segmentation using U-Net.',
        add_help=True
    )
    parser.add_argument('-f', '--feature', type=str, help='Features')

    return parser


def crawl():
    print("crawl")


def main():
    args = get_parser().parse_args()
    eval(args.feature + "()")


if __name__ == "__main__":
    main()

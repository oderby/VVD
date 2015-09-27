import CommonGraphDiffer as cgd
import argparse

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("cg1")
    parser.add_argument("cg2")
    parser.add_argument("out")
    return parser.parse_args()

def main():
    args = parseArgs()
    CGA = cgd.CgxToObject(args.cg1)
    CGB = cgd.CgxToObject(args.cg2)
    ds = CGA.diff(CGB)
    cgd.DSToXML(ds, args.out)

if __name__ == "__main__":
    main()

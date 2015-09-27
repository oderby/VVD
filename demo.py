import CommonGraphDiffer as cgd

def main():
    CGA = cgd.CgxToObject("examples/simple_multiply_example.cgx")

    CGB = cgd.CgxToObject("examples/simple_multiply_example_b.cgx")
    ds = CGA.diff(CGB)
    cgd.DSToXML(ds, "foo.dsx")
    ds2 = cgd.XMLToDS("foo.dsx")
    cgd.DSToXML(ds2, "foo2.dsx")

    print "========================="
    CGB2 = CGA.applyDiff(ds)
    print "========================="
    CGB3 = CGA.applyDiff(ds2)

    print "=CGA========================"
    print CGA
    print "=CGB========================"
    print CGB
    print "=CGB2========================"
    print CGB2
    print "=CGB3========================"
    print CGB3
    print "========================="

if __name__ == "__main__":
    main()

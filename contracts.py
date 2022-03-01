from pyteal import *


tmpl_group_key = Tmpl.Bytes("TMPL_GRP_KEY")
tmpl_data = Tmpl.Bytes("TMPL_DATA")


def escrow(
    data=tmpl_data
):
    return Seq(
        Assert(Ed25519Verify(data, Arg(0), Addr("BJRLVGSFC4IDXEB2B3GJ62QRJAHDDZW7JBWLSUFQ2DUD3IRNC4DHX6XELM"))),
        Approve()
    )


if __name__ == '__main__':
    with open('escrow_ed25519.tmpl.teal', 'w') as f:
        compiled = compileTeal(
            escrow(),
            mode=Mode.Signature,
            version=5,
            assembleConstants=True
        )
        f.write(compiled)

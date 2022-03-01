from pyteal import *


tmpl_group_key = Tmpl.Addr("TMPL_GRP_KEY")
tmpl_data = Tmpl.Bytes("TMPL_DATA")


def escrow(
    data=tmpl_data,
    group_key=tmpl_group_key
):
    return Seq(
        Assert(Ed25519Verify(data, Arg(0), group_key)),
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

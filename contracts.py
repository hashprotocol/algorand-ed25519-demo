from pyteal import *


tmpl_group_key = Tmpl.Bytes("TMPL_GRP_KEY")
tmpl_data = Tmpl.Bytes("TMPL_DATA")


def escrow(
    data=tmpl_data
):
    return Seq(
        Assert(Ed25519Verify(data, Arg(0), Bytes("c586a4d71217c461338a678c5b50b820c4804866d99b783c25605ffa814dde50"))),
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

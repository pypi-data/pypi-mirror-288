from bp_libc_got.util import get_all_addresses, get_got_sections


def bp_got(gdb_api, libc_name=None, flag=False):
    try:
        
        addrs = get_all_addresses(gdb_api, libc_name)
        pre_bps = [
            int(i.split(" ")[0])
            for i in gdb_api.execute("info breakpoints", to_string=True).split("\n")[1:][
                :-1
            ]
        ]
        for addr in addrs:
            gdb_api.execute(f"break *{hex(addr)}")

        bps = [
            int(i.split(" ")[0])
            for i in gdb_api.execute("info breakpoints", to_string=True).split("\n")[1:][
                :-1
            ]
        ]
        if flag:
            for bp in bps:
                if bp in pre_bps:
                    print(bp)
                    payload = f"commands {bp}\n"
                    for bpe in bps:  # breakpoint enable
                        if bpe not in pre_bps:
                            payload += f"enable {bpe}\n"
                    payload += "end"
                    gdb_api.execute(payload)
                else:
                    gdb_api.execute(f"disable {bp}")
        return 1
    except Exception as e:
        print(e)
        return 0

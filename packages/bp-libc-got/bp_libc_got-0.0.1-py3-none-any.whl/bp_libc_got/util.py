def get_got_sections(gdb_api, libc_name):
    sections = gdb_api.execute("info files", to_string=True).split("\n")
    got_sections = []
    for got_section in sections:
        if ".got.plt" in got_section:
            ss = got_section.split(" ")  # section split
            start = int(ss[0], 16)
            end = int(ss[2], 16)
            path = ss[6]
            if (libc_name == None):
                got_sections.append((start, end - start, path))
            elif (libc_name in path):
                got_sections.append((start, end - start, path))
    return got_sections


def get_all_addresses(gdb_api, libc_name):
    got_sections = get_got_sections(gdb_api, libc_name)
    addrs = []
    for got_section in got_sections:
        got_addr = got_section[0]
        got_offset = got_section[1]
        for addr in range(got_addr, got_addr + got_offset, 8):
            addr = int(
                gdb_api.execute(f"print/x *(int64_t*){addr}", to_string=True).split(
                    " "
                )[-1],
                16,
            )
            if addr >> 32:
                addrs.append(addr)
    return addrs

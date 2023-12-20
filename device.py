OPS = "addr addi mulr muli banr bani borr bori setr seti gtir gtri gtrr eqir eqri eqrr".split()


def load_program(input):
    defs = []
    insts = []
    for line in input.read().splitlines():
        parts = line.split()
        op = parts[0]
        args = list(map(int, parts[1:]))

        if op.startswith("#"):
            defs.append((op, args))
        else:
            insts.append((op, args))
    return defs, insts


def apply_op(op, a, b, c, reg):
    reg = reg[:]

    if op == "addr":
        reg[c] = reg[a] + reg[b]
    elif op == "addi":
        reg[c] = reg[a] + b
    elif op == "mulr":
        reg[c] = reg[a] * reg[b]
    elif op == "muli":
        reg[c] = reg[a] * b
    elif op == "banr":
        reg[c] = reg[a] & reg[b]
    elif op == "bani":
        reg[c] = reg[a] & b
    elif op == "borr":
        reg[c] = reg[a] | reg[b]
    elif op == "bori":
        reg[c] = reg[a] | b
    elif op == "setr":
        reg[c] = reg[a]
    elif op == "seti":
        reg[c] = a
    elif op == "gtir":
        reg[c] = int(a > reg[b])
    elif op == "gtri":
        reg[c] = int(reg[a] > b)
    elif op == "gtrr":
        reg[c] = int(reg[a] > reg[b])
    elif op == "eqir":
        reg[c] = int(a == reg[b])
    elif op == "eqri":
        reg[c] = int(reg[a] == b)
    elif op == "eqrr":
        reg[c] = int(reg[a] == reg[b])
    else:
        raise ValueError("bad op", op)

    return reg


def run_program(program, regs, ip=0):
    defs, insts = program

    ip_reg = None
    for df, args in defs:
        if df == "#ip":
            ip_reg = args[0]

    while 0 <= ip < len(insts):
        before = regs

        if ip_reg is not None:
            regs[ip_reg] = ip

        op, (a, b, c) = insts[ip]
        regs = apply_op(op, a, b, c, regs)

        next_ip = (regs[ip_reg] if ip_reg is not None else ip) + 1
        # print(f"{ip=} {before} {op} {a} {b} {c} {regs} {next_ip=}")

        if ip_reg is not None:
            ip = regs[ip_reg]

        ip += 1
    return regs

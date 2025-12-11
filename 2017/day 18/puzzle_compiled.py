
def program_0(send, receive):
    p = 0
    a = (2 ** 31) - 1
    i = 127
    p = 622
    while i > 0:
        p = (p * 8505) % a
        p = ((p * 129749) + 12345) % a
        b = p % 10000

        send(b)
        i -= 1

    while a > 0:
        b = 1
        while b > 0:
            yield
            b = receive()
        
        f = 1
        while f > 0:
            f = 0
            i = 126
            yield
            a = receive()

            while i > 0:
                yield
                b = receive()

                if b - a > 0:
                    send(b)
                    f = 1
                    i -= 1
                else:
                    send(a)
                    a = b
                    i -= 1
            
            send(a)


def program_1(send, receive):
    i = 31
    a = 1
    while a > 0:
        f = 1
        while f > 0:
            f = 0
            i = 126
            yield
            a = receive()

            while i > 0:
                yield
                b = receive()

                if b - a > 0:
                    send(b)
                    f = 1
                    i -= 1
                else:
                    send(a)
                    a = b
                    i -= 1
            
            send(a)
        
        if a > 0:
            b = 1
            while b > 0:
                yield
                b = receive()

def executor():
    total_left_sends = [0]

    left_stack, right_stack = [], []
    def left_send(x):
        total_left_sends[0] += 1
        left_stack.append(x)
    right_send = lambda x: right_stack.append(x)
    left_receive = lambda: left_stack.pop(0)
    right_receive = lambda: right_stack.pop(0)

    left_program = program_0(right_send, left_receive)
    next(left_program)

    right_program = program_1(left_send, right_receive)
    next(right_program)

    left_terminated, right_terminated = False, False

    while not left_terminated or not right_terminated:
        if len(left_stack) == 0 and len(right_stack) == 0:
            break

        if not left_terminated and len(left_stack) > 0:
            try:
                next(left_program)
            except StopIteration:
                left_terminated = True
        
        if not right_terminated and len(right_stack) > 0:
            try:
                next(right_program)
            except StopIteration:
                right_terminated = True

    if left_terminated and right_terminated:
        print("terminated because both programes terminated")

    return total_left_sends[0]

print(executor())

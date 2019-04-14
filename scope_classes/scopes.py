# def something():
#     y = 25
#
# print(y)  # NameError: name 'y' is not defined


def assign_local_x():
    x = 35


def assign_global_x():
    global x
    x = 35


def fn_with_inner():
    def inner_fn():
        y = 10

    def inner_fn_with_nonlocal():
        nonlocal y
        y = 10

    y = 5
    inner_fn()
    print(f'Value of y after inner_fn is {y}')
    inner_fn_with_nonlocal()
    print(f'Value of y after inner_fn_with_nonlocal is {y}')


if __name__ == '__main__':
    if True:
        x = 25

    print(f'Value of x is {x}')  # "x" a global scopehoz tartozik
    assign_local_x()
    print(f'Value of x after assign_local_x is {x}')
    assign_global_x()
    print(f'Value of x after assign_global_x is {x}')

    fn_with_inner()


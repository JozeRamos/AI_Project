
# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from FileReader import FileReader


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    a = FileReader.getEstablishments()
    print(a[0])
    print(a[1])
    #FileReader.getDistances()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

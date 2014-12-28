globe = "original_value"


def main():
    printGlobe()

    # update global var
    globe = "new_value"

    printGlobe()




def printGlobe():
    print globe


if __name__ == '__main__':
    main()

def happy():
    print("happy, happy world!")


def main():
    print("Hello, world!")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "happy":
        happy()
    else:
        main()
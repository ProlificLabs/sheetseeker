from src.main import run as run_main


def run_cli():
    print("Local conversation test. Type /exit to leave.")
    talking = True

    while talking:
        user_input = input(">> ")
        if user_input == "/exit":
            print("Exiting...")
            talking = False
        else:
            run_main(query=user_input)


if __name__ == "__main__":
    run_cli()

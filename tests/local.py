from main import get_csv_data, llm_query


class LocalTest:
    def __init__(self):
        print("Local conversation test. Type /exit to leave.")
        self.csv_data = None
        self.initialize_csv()

    def initialize_csv(self):
        self.csv_data = get_csv_data()
        print("Local CSV Data loaded")

    def run(self):
        talking = True

        while talking:
            user_input = input(">> ")
            if user_input == "/exit":
                print("Exiting...")
                talking = False
            else:
                llm_query(user_input, self.csv_data)


if __name__ == "__main__":
    LocalTest().run()

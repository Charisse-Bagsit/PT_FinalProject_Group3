from banker_logic import BankersAlgorithm, BankerError
from banker_format import format_state, format_safety, format_request


def main():
    print("Starting the application...")
    try:
        bank = BankersAlgorithm(
            total=[10, 5, 7],
            allocation=[[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]],
            max_claim=[[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]],
        )
    except BankerError as err:
        print(f"Invalid input: {err}")
        return

    print(format_state(bank))
    print()
    print(format_safety(bank, bank.safety_check()))
    print("\n" + "=" * 60 + "\n")
    print(format_request(bank, bank.request_resources("P1", [1, 0, 2])))


if __name__ == "__main__":
    main()

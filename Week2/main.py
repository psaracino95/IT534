#Peter Saracino
#IT-534
from variable_sorter import VariableSort
def main():
    sorter = VariableSort()

    print("===============================================")
    print("Welcome to the Variable Sorter Application!")
    print("Rules: Integers, Floats, and Alphabetic-only strings.")
    print("Type 'exit' or 'stop' at any time to end and view results.")
    print("=================================================")

    # MAIN LOOP
    while True:
        try:
            # user input here
            user_input = input("\nEnter a value to sort: ")
            
            #Check for termination commands
            if user_input.strip().lower() in ['exit', 'stop']:
                print("Terminating program loop...")
                break

            #Processes and sort the input
            result_message = sorter.validate_and_sort(user_input)
            print(result_message)
            
        except ValueError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            #Ctrl+C
            print("\n\nProgram interrupted. Exiting...")
            break

    # Display final results once the loop finishes
    print("\nFINAL RESULT")
    summary = sorter.get_summary()
    for data_type, values in summary.items():
        print(f"{data_type}: {values}")
    print("================================================")

if __name__ == "__main__":
    main()
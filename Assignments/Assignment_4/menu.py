# import utils
# import license_utils
# from datetime import datetime

# def print_menu():
#     """
#     Print the main menu options.
#     """
#     print("\n1. Register Driver's License")
#     print("2. Check Driver's License")
#     print("3. Print All License Data")
#     print("4. Print Validity Table")
#     print("5. Revoke a License")
#     print("6. Exit")

# def main_menu():
#     """
#     Main menu loop for interacting with the system.
#     """
#     while True:
#         print_menu()
#         choice = input("Enter choice: ")
#         if choice.isdigit():
#             choice = int(choice)
#             if choice == 1:
#                 aadhaar = input("Enter Aadhaar Number: ")
#                 if len(aadhaar) != 12 or not aadhaar.isdigit():
#                     print("Invalid Aadhaar Number. Please enter a 12-digit numeric value.")
#                     continue
#                 dob = input("Enter Date of Birth (YYYY-MM-DD): ")
#                 try:
#                     datetime.strptime(dob, "%Y-%m-%d")
#                 except ValueError:
#                     print("Invalid Date of Birth format. Please enter in YYYY-MM-DD format.")
#                     continue
#                 sex = input("Enter Sex (M/F/O): ").upper()
#                 if sex not in ['M', 'F', 'O']:
#                     print("Invalid Sex. Please enter M, F, or O.")
#                     continue
#                 try:
#                     encrypted_license_data, signature = license_utils.register_license(aadhaar, dob, sex)
#                     decrypted_license_data = license_utils.secure_communicate(encrypted_license_data, license_utils.private_key, "decrypt")
#                     print("License Registered. License Data:")
#                     print(decrypted_license_data)
#                     print("Digital Signature:", signature.hex())
#                 except Exception as e:
#                     print(f"Error registering license: {e}")
#             elif choice == 2:
#                 license_info_input = input("Enter License Data: ")
#                 signature_hex = input("Enter Digital Signature (hex): ")
#                 try:
#                     signature = bytes.fromhex(signature_hex)
#                     verification_result = license_utils.check_license(license_info_input, signature)
#                     print(verification_result)
#                 except ValueError:
#                     print("Invalid hex format for digital signature.")
#                 except Exception as e:
#                     print(f"Error checking license: {e}")
#             elif choice == 3:
#                 utils.print_all_licenses()
#             elif choice == 4:
#                 utils.print_validity_table()
#             elif choice == 5:
#                 utils.revoke_license()
#             elif choice == 6:
#                 break
#             else:
#                 print("Invalid choice. Please enter a number between 1 and 6.")
#         else:
#             print("Invalid choice. Please enter a number between 1 and 6.")

# if __name__ == "__main__":
#     main_menu()




import utils
import license_utils
from datetime import datetime

def print_menu():
    """
    Print the main menu options.
    """
    print("\n1. Register Driver's License")
    print("2. Check Driver's License")
    print("3. Print All License Data")
    print("4. Print Validity Table")
    print("5. Revoke a License")
    print("6. Exit")

def main_menu():
    """
    Main menu loop for interacting with the system.
    """
    while True:
        print_menu()
        choice = input("Enter choice: ")
        if choice.isdigit():
            choice = int(choice)
            if choice == 1:
                aadhaar = input("Enter Aadhaar Number: ")
                if len(aadhaar) != 12 or not aadhaar.isdigit():
                    print("Invalid Aadhaar Number. Please enter a 12-digit numeric value.")
                    continue
                dob = input("Enter Date of Birth (YYYY-MM-DD): ")
                try:
                    datetime.strptime(dob, "%Y-%m-%d")
                except ValueError:
                    print("Invalid Date of Birth format. Please enter in YYYY-MM-DD format.")
                    continue
                sex = input("Enter Sex (M/F/O): ").upper()
                if sex not in ['M', 'F', 'O']:
                    print("Invalid Sex. Please enter M, F, or O.")
                    continue
                try:
                    encrypted_aadhaar = license_utils.secure_communicate(aadhaar, license_utils.public_key)
                    encrypted_dob = license_utils.secure_communicate(dob, license_utils.public_key)
                    encrypted_sex = license_utils.secure_communicate(sex, license_utils.public_key)
                    
                    encrypted_license_data, signature = license_utils.register_license(encrypted_aadhaar, encrypted_dob, encrypted_sex)
                    decrypted_license_data = license_utils.secure_communicate(encrypted_license_data, license_utils.private_key, "decrypt")
                    print("License Registered. License Data:")
                    print(decrypted_license_data)
                    print("Digital Signature:", signature.hex())
                except Exception as e:
                    print(f"Error registering license: {e}")
            elif choice == 2:
                license_info_input = input("Enter License Data: ")
                signature_hex = input("Enter Digital Signature (hex): ")
                try:
                    signature = bytes.fromhex(signature_hex)
                    encrypted_license_data = license_utils.secure_communicate(license_info_input, license_utils.public_key)
                    verification_result = license_utils.check_license(encrypted_license_data, signature)
                    print(verification_result)
                except ValueError:
                    print("Invalid hex format for digital signature.")
                except Exception as e:
                    print(f"Error checking license: {e}")
            elif choice == 3:
                utils.print_all_licenses()
            elif choice == 4:
                utils.print_validity_table()
            elif choice == 5:
                utils.revoke_license()
            elif choice == 6:
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main_menu()

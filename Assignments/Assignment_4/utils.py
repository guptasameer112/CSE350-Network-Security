import license_utils

def print_all_licenses():
    """
    Print all registered licenses.
    """
    if license_utils.licenses_db:
        for license_id, data in license_utils.licenses_db.items():
            print(f"License ID: {license_id}, Data: {data}")
    else:
        print("No licenses registered.")

def print_validity_table():
    """
    Print the validity table.
    """
    if license_utils.validity_table:
        for license_hash, status in license_utils.validity_table.items():
            print(f"Hash: {license_hash.hex()}, Status: {status}")
    else:
        print("Validity table is empty.")

def revoke_license():
    """
    Revoke a license based on its ID.
    """
    license_id = input("Enter the License ID to revoke: ")
    if license_id.isdigit():
        license_id = int(license_id)
        if license_id in license_utils.licenses_db:
            license_data = license_utils.licenses_db[license_id]
            license_hash = license_utils.hash_license_data(license_data)
            if license_hash in license_utils.validity_table:
                if license_utils.validity_table[license_hash] == 'revoked':
                    print("License is already revoked.")
                else:
                    license_utils.validity_table[license_hash] = 'revoked'
                    print("License has been revoked.")
            else:
                print("License hash not found in validity table.")
        else:
            print("License ID not found.")
    else:
        print("Invalid License ID. Please enter a valid integer.")

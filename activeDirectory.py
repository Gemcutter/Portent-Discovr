from ldap3 import Server, Connection, SUBTREE, ALL_ATTRIBUTES

# Replace with your DC information and credentials
AD_SERVER = 'your_domain_controller_ip_or_hostname'
AD_USERNAME = 'your_ad_username'
AD_PASSWORD = 'your_ad_password'
BASE_DN = 'DC=yourdomain,DC=com'  # e.g., 'DC=example,DC=com'

try:
    # Establish a connection to the AD server
    server = Server(AD_SERVER, use_ssl=True, get_info=ALL_ATTRIBUTES) # Use use_ssl=True for LDAPS
    conn = Connection(server, user=AD_USERNAME, password=AD_PASSWORD, auto_bind=True)

    # Search for a specific user
    search_filter = '(&(objectCategory=Person)(objectClass=User)(sAMAccountName=your_target_username))'
    conn.search(search_base=BASE_DN,
                search_filter=search_filter,
                search_scope=SUBTREE,
                attributes=['sAMAccountName', 'displayName', 'mail'])

    if conn.entries:
        print("User found:")
        for entry in conn.entries:
            print(f"sAMAccountName: {entry.sAMAccountName}")
            print(f"Display Name: {entry.displayName}")
            print(f"Email: {entry.mail}")
    else:
        print("User not found.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Unbind the connection
    if 'conn' in locals() and conn.bound:
        conn.unbind()
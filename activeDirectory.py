from ldap3 import Server, Connection, SUBTREE, ALL_ATTRIBUTES, Tls
import ssl
# Replace with your DC information and credentials
AD_SERVER = 'ADDC01'
AD_USERNAME = 'Administrator'
AD_PASSWORD = 'W0nderfu1'
BASE_DN = 'DC=chris,DC=local'  # e.g., 'DC=example,DC=com'

try:
    # Establish a connection to the AD server
    tls_config = Tls(validate=ssl.CERT_NONE)
    server = Server(AD_SERVER, port=636, use_ssl=True, get_info=ALL_ATTRIBUTES) # Use use_ssl=True for LDAPS
    conn = Connection(server, user=AD_USERNAME, password=AD_PASSWORD, auto_bind=True)

   # Search for all computer objects in the domain
    search_filter = '(objectClass=computer)'
    conn.search(
        search_base=BASE_DN,
        search_filter=search_filter,
        search_scope=SUBTREE,
        attributes=['name', 'operatingSystem']
    )

    if conn.entries:
        print("Computers found:")
        for entry in conn.entries:
            print(f"Name: {entry.name}, OS: {entry.operatingSystem if 'operatingSystem' in entry else 'Unknown'}")
    else:
        print("No computers found.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    if 'conn' in locals() and conn.bound:
        conn.unbind()
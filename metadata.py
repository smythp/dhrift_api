title = "DHRIFT Application Interface"

description = """
Digital Humanities Resource Infrastructure for Teaching (DHRIFT) is humanities infrastructure consisting of deployable sites for use in courses, workshops, and intensives.

This API allows for extended DHRIFT functionality by enabling DHRIFT sites to communic ate with one another and store persistent information across the DHRIFT network.
"""


tags = [
    {
        "name": "users",
        "description": "Operations relating to users. A method for receiving an authentication token using OAuth is included.",
    },
    {
        "name": "sites",
        "description": "Operations relating to DHRIFT sites. These correspond to installations of DHRIFT at various institutions that have registered with the network.",
    },
    {
        "name": "resources",
        "description": "Operations relating to pedagogical resources such as workshops and guides.",
    },
]

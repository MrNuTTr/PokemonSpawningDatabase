## Pokemon Breeding Database

### Introduction
Welcome to the Pokémon Breeding & Research Division. You are being hired to help our startup company gain a solid foothold into the industry. We, the board of directors, understand that an operation like this requires technical expertise to setup the foundation of everything we do; that is where you come in. 

Outlined below are our requirements for a database system that will facilitate our transactions in this project.
The system will need to be able to handle an inventory of actively held Pokémon, as well as their children. These Pokémon will be delivered and removed from inventory by clients. Clients will be charged on the length of stay by the original Pokémon deposited.

It will be important to keep track of who owns what Pokémon. Mates will be limited to a client. That is, a Pokémon from one client cannot mate with a separate client’s Pokémon. Descendants of a client’s Pokémon may be withdrawn by that client.

### Business Rules
- A client deposits Pokémon into inventory
- A client withdraws Pokémon from inventory
- A Pokémon can have parents and children, and mates
- A Pokémon must have a mate to have a child
- A Pokémon can only mate with another Pokémon from the same client
- A child Pokémon has the same owner as the parents
- A client is charged with the length of stay of the Pokémon
- A room can only store a single Pokémon

## Database Design
![database_design.png](design%2Fdatabase_design.png)
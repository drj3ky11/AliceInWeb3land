from web3 import Web3

# Configuración
NODE_URL = "http://localhost:8545"  
ADDRESS = "0xf97afbf8fe3c9c7b25dd4c28f5e909765ba5c905"  # Reemplaza con la dirección a verificar

# Conectar al nodo
w3 = Web3(Web3.HTTPProvider(NODE_URL))

def is_erc4337_account(address):
    """Verifica si una dirección es una Account Abstraction (ERC-4337)."""
    abi_erc4337 = [
        {
            "constant": True,
            "inputs": [],
            "name": "entryPoint",
            "outputs": [{"name": "", "type": "address"}],
            "type": "function"
        }
    ]
    
    try:
        contract = w3.eth.contract(address=address, abi=abi_erc4337)
        entry_point = contract.functions.entryPoint().call()
        return True
    except:
        return False

def get_address_type(address):
    """Determina el tipo de dirección (EOA, Smart Contract, ERC-4337)."""
    checksum_addr = Web3.to_checksum_address(address)
    
    # 1. Verificar si es EOA (sin bytecode)
    bytecode = w3.eth.get_code(checksum_addr)
    if bytecode == b'':
        return "EOA (Externally Owned Account)"
    
    # 2. Verificar si es ERC-4337
    if is_erc4337_account(checksum_addr):
        return "ERC-4337 Account Abstraction"
    
    # 3. Si no, es un Smart Contract estándar
    return "Smart Contract"

if __name__ == "__main__":
    if w3.is_connected():
        address_type = get_address_type(ADDRESS)
        print(f"Tipo de dirección: {address_type}")
    else:
        print("Error de conexión al nodo")
# One node to rule them all

Después de La Fusión, se requieren dos clientes para ejecutar un nodo de Ethereum: un cliente para la capa de ejecución (EL) y otro para  la capa de concenso (CL). En cuanto a espacio, lo suyo es SSD con más de 3tb. Una buena conexión a internet y una RAM de mínimo 32gb.

Me gusta emplear Geth y Lighthose, una ejecución rápida sería tal que así (en Windows, si lo sé... but it works...):

```
.\lighthouse.exe bn --network mainnet --execution-endpoint http://localhost:8551 --execution-jwt D:\eth\secret\jwt-secret.txt --checkpoint-sync-url https://mainnet.checkpoint.sigp.io --datadir D:\eth\ethdata\beacon\ --http --disable-deposit-contract-sync
 ```

 ```
 ./geth.exe --syncmode "snap" --http --http.addr "localhost" --http.port 8545 --http.api "eth,net,web3" --datadir D:\eth\ethdata --authrpc.jwtsecret D:\eth\secret\jwt-secret.txt --authrpc.port 8551
 ```


Y a funcionar! Solo queda esperar a que la rede se sicronice.

## La explicación

Vamos a desgranar qué hemos ejecutado para correr el nodo

### Geth

[Geth (go-ethereum)](https://geth.ethereum.org/) is a Go implementation of Ethereum - a gateway into the decentralized web. Geth has been a core part of Ethereum since the very beginning. Geth is an Ethereum **execution client** meaning it handles transactions, deployment and execution of smart contracts and contains an embedded computer known as the Ethereum Virtual Machine.

1. --syncmode "snap" : Define el modo de sincronización como snap. Snap Sync: Descarga bloques recientes y utiliza snapshots para acelerar la sincronización. Es más rápido que el modo full (descarga toda la historia desde el bloque génesis) y consume menos recursos que fast (obsoleto).

2. --http: Habilita el servidor HTTP JSON-RPC.

3. --http.addr "localhost" Vincula el servidor HTTP a la dirección localhost.

4. --http.port 8545 Define el puerto 8545 para el servidor HTTP.

5. --http.api "eth,net,web3" Habilita las APIs especificadas (eth, net, web3) sobre HTTP.

6. --datadir D:\eth\ethdata Especifica el directorio donde se almacenan los datos de la blockchain (bloques, estados, etc.).

7. --authrpc.jwtsecret D:\eth\secret\jwt-secret.txt Define la ubicación del archivo con el secreto JWT (JSON Web Token). Para ello  ```openssl rand -hex 32 > jwt-secret.txt```

9. --authrpc.port 8551 Establece el puerto 8551 para el Engine API.


### LightHouse

[Lighthouse](https://github.com/sigp/lighthouse): Ethereum **consensus client**. An open-source Ethereum consensus client, written in Rust and maintained by Sigma Prime

1. --network mainnet Especifica que el nodo se conectará a la red principal de Ethereum (mainnet).

2. --execution-endpoint http://localhost:8551 Establece la URL del cliente de ejecución (Geth, en este caso). http://localhost:8551: Es el puerto del Engine API (habilitado en Geth con --authrpc.port 8551).

3. --execution-jwt D:\eth\secret\jwt-secret.txt Define la ruta al archivo JWT secret compartido entre el Beacon Node y Geth.

4. --checkpoint-sync-url https://mainnet.checkpoint.sigp.io Habilita la sincronización desde un checkpoint de confianza.

5. --datadir D:\eth\ethdata\beacon\ Define el directorio donde se almacenan los datos del Beacon Node (bloques de la Beacon Chain, estados, etc.).

6. --http Habilita el servidor HTTP API del Beacon Node.

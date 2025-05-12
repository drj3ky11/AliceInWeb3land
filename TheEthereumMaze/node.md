# One node to rule them all

Después de La Fusión, se requieren dos clientes para ejecutar un nodo de Ethereum: un cliente para la capa de ejecución (EL) y otro para  la capa de concenso (CL). En cuanto a espacio, lo suyo es SSD con más de 3tb. Una buena conexión a internet y una RAM de mínimo 32gb.

Me gusta emplear Geth y Lighthose, una ejecución rápida sería tal que así:

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


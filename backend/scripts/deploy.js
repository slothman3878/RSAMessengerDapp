const { exec } = require('shelljs');

async function main() {
  const contractName = 'Messenger';

  const [deployer] = await ethers.getSigners();

  console.log(
    "Deploying contracts with the account:",
    deployer.address
  );
  
  console.log("Account balance:", (await deployer.getBalance()).toString());

  const Contract = await ethers.getContractFactory(contractName);
  const contract = await Contract.deploy();

  console.log("Contract address:", contract.address);
}

main()
  .then(() => exec('yes | cp artifacts/contracts/Messenger.sol/Messenger.json ../RSAMessengerDapp/'))
  .then(() => process.exit(0))
  .catch(error => {
    console.error(error);
    process.exit(1);
  });

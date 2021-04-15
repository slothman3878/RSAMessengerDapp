//Script for transferring ether from the accounts generated with intialization of the hardhat network
let recievers = [
  '0xc7aa2134001d5fE6c0b18D5DBFD68c6cc75672B0',
]

async function main() {
  const [sender] = await ethers.getSigners();

  console.log(
    'Sending 50 ether to these addreses:'
  );

  for (const reciever of recievers){
    console.log(reciever);
    const tx = await sender.sendTransaction({
      to: reciever,
      value: ethers.utils.parseEther('50.0')
    });
  }
}

main()
  .then(() => process.exit(0))
  .catch(error => {
    console.error(error);
    process.exit(1);
  });
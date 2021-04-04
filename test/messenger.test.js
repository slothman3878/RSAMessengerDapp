const { expect } = require('chai');
const { waffle } = require('hardhat');

let provider = waffle.provider;

describe("Messenger Contract", function() {
  let Messenger;
  
  let deployer;
  let A;
  let B;

  let instances = {};

  let keys = {};
  let messages = {};

  beforeEach(async function() {
    [deployer, A, B] = await ethers.getSigners();
    Messenger = await ethers.getContractFactory("Messenger");
    instances.deployer = await Messenger.deploy();
    await instances.deployer.deployed();

    keys.A = 'keyA';
    keys.B = 'keyB';

    messages.fromAtoB = 'Hello B';
    messages.fromBtoA = 'Hello A';
  });

  it("Attach users A, B with respective public keys", async function() {
    instances.A = await instances.deployer.connect(A);
    instances.B = await instances.deployer.connect(B); 
    await instances.A.deployed();
    await instances.B.deployed();

    var receipt = await (await instances.A.setPublicKey(A.address, keys.A)).wait();
    var events = receipt.events?.filter((x)=>{return x.event=='SetPublicKey'});
    expect(events[events.length-1].args.key).to.equal(keys.A);

    receipt = await (await instances.B.setPublicKey(B.address, keys.B)).wait();
    var events = receipt.events?.filter((x)=>{return x.event=='SetPublicKey'});
    expect(events[events.length-1].args.key).to.equal(keys.B);

    expect(await instances.deployer.getPublicKey(A.address)).to.equal(keys.A);
    expect(await instances.deployer.getPublicKey(B.address)).to.equal(keys.B);
  });

  it("Send messages to and from A and B", async function(){

    var receipt = await (await instances.A.sendMessage(A.address, B.address, messages.fromAtoB)).wait();
    var events = receipt.events?.filter((x)=>{return x.event=='MessageSent'});
    expect(events[events.length-1].args.from).to.equal(A.address);
    expect(events[events.length-1].args.to).to.equal(B.address);

    expect((await instances.A.getMessage(1)).from).to.equal(A.address);
    expect((await instances.A.getMessage(1)).to).to.equal(B.address);
    expect((await instances.A.getMessage(1)).message).to.equal(messages.fromAtoB);

    receipt = await (await instances.B.sendMessage(B.address, A.address, messages.fromBtoA)).wait();
    events = receipt.events?.filter((x)=>{return x.event=='MessageSent'});
    expect(events[events.length-1].args.from).to.equal(B.address);
    expect(events[events.length-1].args.to).to.equal(A.address);

    expect((await instances.B.getMessage(2)).from).to.equal(B.address);
    expect((await instances.B.getMessage(2)).to).to.equal(A.address);
    expect((await instances.B.getMessage(2)).message).to.equal(messages.fromBtoA);
  });

  it("Check Sent and Recieved messages of A", async function(){
    expect((await instances.A.getMessage((await instances.A.getSentMessageByIndex(0)))).message).to.equal(messages.fromAtoB);
    expect((await instances.B.getMessage((await instances.A.getRecievedMessageByIndex(0)))).message).to.equal(messages.fromBtoA);

    //For convenience:
    console.log(await instances.A.getRecievedBalance(A.address));
    console.log(await instances.A.getSentBalance(A.address));
  });
})
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Messenger{
  mapping(address => string) _keys; // Contains URI to keys for each address
  mapping(address => bool) _exists;

  //Having to store the from and to addresses for each message may be needlessly costly.
  //Information about who sent and recieved the message can be appended to the message itself.
  //Also better privacy if the sender and recipient of some message is unknown
  //Edit: Cannot possibly implement an inbox without the relevent from and to information publically visible
  struct Message{
    //Declare if Message is type public or private? Private messsages require decryption, whereas public ones don't.
    address from;
    address to;
    string message;
    uint256 signed; // date signed
  }

  string private _name = "EthMessenger";

  uint256 private _messageIndex;

  mapping(uint256 => Message) private _messages;

  mapping(address => uint256) private _recievedBalance; //total recieved for each address
  mapping(address => uint256) private _sentBalance;     //total sent for each address
  
  mapping(address => mapping(uint256 => uint256)) private _recieved;  //recieved messages
  mapping(address => mapping(uint256 => uint256)) private _sent;

  event SetPublicKey(address user, string key);
  event MessageSent(address from, address to);

  function name() public virtual view returns(string memory){
    return _name;
  }

  function setPublicKey(address user, string memory keyURI) public virtual {
    require(user == msg.sender, "Messenger: User not the transaction sender");
    if(!_exists[user]) _exists[user] = true;
    _keys[user]=keyURI;
    emit SetPublicKey(user, keyURI);
  }

  function sendMessage(address from, address to, string memory URI) public virtual {
    require(from == msg.sender, "Messenger: Message not being sent by transaction sender");
    require(_exists[to], "Messenger: Trying to send message to nonexistent user");
    Message memory message = Message(from, to, URI, block.timestamp);
    //string memory message = URI;

    _messageIndex++;
    _messages[_messageIndex]=message;
    
    _recieved[to][_recievedBalance[to]]=_messageIndex;
    _recievedBalance[to]++;

    _sent[from][_sentBalance[from]]=_messageIndex;
    _sentBalance[from]++;

    emit MessageSent(from, to);
  }

  function getPublicKey(address to) public virtual view returns (string memory) {
    require(_exists[to], "Messenger: Requesting public key of nonexistent user");
    return _keys[to];
  }

  function getMessage(uint256 id) public virtual view returns (Message memory) {
    //require(_messages[id].from!=address(0),"Messenger: Requesting nonexistent message");
    return _messages[id];
  }

  function getRecievedMessageByIndex(uint256 id) public virtual view returns (uint256) {
    address user = msg.sender;
    require(id < getRecievedBalance(user), "Messenger: Index out of bounds");
    return _recieved[user][id]; 
  }

  function getSentMessageByIndex(uint256 id) public virtual view returns (uint256) {
    address user = msg.sender;
    require(id < getSentBalance(user), "Messenger: Index out of bounds");
    return _sent[user][id];
  }

  function getRecievedBalance(address user) public virtual view returns (uint256) {
    return _recievedBalance[user];
  }

  function getSentBalance(address user) public virtual view returns (uint256) {
    return _sentBalance[user];
  }
}
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract NFT is ERC721, Ownable {

    using Counters for Counters.Counter;
    Counters.Counter public currentTokenId;

    string public baseTokenURI;

    constructor(address initialOwner) ERC721("BlockFund", "NFT") Ownable(initialOwner) {
        baseTokenURI = "";
    }

    function mintNFT() public payable {
        require(msg.value > 0, "NFT: Insufficient funds sent");

        currentTokenId.increment();
        uint256 newItemId = currentTokenId.current();
        _safeMint(msg.sender, newItemId);

        payable(owner()).transfer(msg.value);
    }

    function _baseURI() internal view virtual override returns (string memory) {
        return baseTokenURI;
    }

    function setBaseTokenURI(string memory _baseTokenURI) public onlyOwner {
        baseTokenURI = _baseTokenURI;
    }
}

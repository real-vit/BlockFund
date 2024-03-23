// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract BFT is ERC20, Ownable {
    mapping(uint256 => uint256) public votes;

    constructor(address initialOwner) ERC20("BlockFundToken DAO", "BFT") Ownable(initialOwner) {
        _mint(initialOwner, 1000 * (10 ** uint256(decimals())));
    }

    function mint(address to, uint256 amount) public {
        _mint(to, amount);
    }

    function vote(uint256 proposalId) public {
        require(balanceOf(msg.sender) > 0, "Must have tokens to vote");
        require(proposalId > 0 && proposalId <= 2, "Invalid proposal ID");

        votes[proposalId]++;
    }

    function getVoteCount(uint256 proposalId) public view returns (uint256) {
        return votes[proposalId];
    }
}

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract CarbonChain is ERC20, Ownable {
    
    struct CarbonProject {
        address owner;
        string location;
        uint256 co2_tons;
        bytes32 satellite_proof_hash;
        uint256 timestamp;
        bool verified;
    }
    
    CarbonProject[] public projects;
    mapping(address => uint256[]) public userProjects;
    mapping(bytes32 => bool) public proofUsed;
    
    event ProjectTokenized(
        uint256 indexed projectId,
        address indexed owner,
        uint256 co2_tons,
        bytes32 satellite_proof
    );
    
    event ProjectVerified(uint256 indexed projectId);
    
    constructor() ERC20("CarbonChain", "CARB") {}
    
    function tokenizeProject(
        string memory location,
        uint256 co2_tons,
        bytes32 satellite_proof_hash
    ) public {
        require(co2_tons > 0, "CO2 must be positive");
        require(!proofUsed[satellite_proof_hash], "Proof already used");
        
        CarbonProject memory newProject = CarbonProject({
            owner: msg.sender,
            location: location,
            co2_tons: co2_tons,
            satellite_proof_hash: satellite_proof_hash,
            timestamp: block.timestamp,
            verified: false
        });
        
        projects.push(newProject);
        uint256 projectId = projects.length - 1;
        userProjects[msg.sender].push(projectId);
        proofUsed[satellite_proof_hash] = true;
        
        // Mint tokens: 1 token = 1 ton CO2
        uint256 tokenAmount = co2_tons * (10 ** uint256(decimals()));
        _mint(msg.sender, tokenAmount);
        
        emit ProjectTokenized(projectId, msg.sender, co2_tons, satellite_proof_hash);
    }
    
    function verifyProject(uint256 projectId) public onlyOwner {
        require(projectId < projects.length, "Project not found");
        projects[projectId].verified = true;
        emit ProjectVerified(projectId);
    }
    
    function getProject(uint256 projectId) public view returns (CarbonProject memory) {
        return projects[projectId];
    }
    
    function getProjectCount() public view returns (uint256) {
        return projects.length;
    }
}

async function main() {
    const CarbonChain = await ethers.getContractFactory("CarbonChain");
    const contract = await CarbonChain.deploy();
    await contract.deployed();
    console.log("CarbonChain deployed to:", contract.address);
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});

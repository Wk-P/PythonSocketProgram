process.on("message", (size) => {
    const buf = allocMemory(parseInt(size));
    console.log("Alloc memory finished");
    buf.fill(0);
    console.log("Memory distroied");
})

function allocMemory(n) {
    try {
        return Buffer.alloc(n);
    }
    catch (error) {
        console.log(`Error => ${error}`);
    }
}
process.on("message", (number) => {
    const result = number - 1;
    console.log(`Number => ${number}`)
    process.send(result);
})
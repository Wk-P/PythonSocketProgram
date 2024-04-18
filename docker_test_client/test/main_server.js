const express = require('express');
const { fork } = require('child_process');
const path = require('path');


// 创建 Express 应用
const app = express();
app.use(express.urlencoded({ extended: false }))
app.use(express.json());

// // 定义路由，当收到根路径的 GET 请求时，发送 "Hello, world!" 响应
// app.post('/', (req, res) => {
//     const type = req.headers.task_type;
//     const data = req.body;
//     try {

//         if (type == "C") {
//             console.log("Calculate prime number");
//         } else if (type == "M") {
//             console.log("Alloc memory");
//         } else if (type == "H") {
//             console.log("File Copy");
//         } else {
//             console.log("ERROR");
//         }
//     } catch (error) {
//         console.log(`${error}`);
//     }
//     res.send(`Hello, ${req.headers.host}`);
// });

app.post('/', (req, res) => {
    const type = req.headers.task_type;
    try {

        if (type == "C") {
            const data = req.body;
            console.log("Calculate prime number");
            const childProcPath = path.join(path.dirname(__filename), 'child_p1.js');
            const childProc = fork(childProcPath);

            childProc.send(data.number);

            childProc.on("message", (result) => {
                console.log(`Result => ${result}`);
                childProc.kill();
            })
        } else if (type == "M") {
            const data = req.body;
            console.log("Alloc memory");
            const childProcPath = path.join(path.dirname(__filename), 'child_p2.js');
            const childProc = fork(childProcPath);

            childProc.send(data.size);
        } else if (type == "H") {
            console.log("File Copy");
        } else {
            console.log("ERROR");
        }
    } catch (error) {
        console.log(`${error}`);
    }
    res.send(`Hello, ${req.headers.host}`);
});



// 指定服务器监听的端口
const port = 3000;

// 启动服务器，监听指定端口
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}/`);
});

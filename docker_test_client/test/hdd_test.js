const { exec } = require('child_process');

exec('df -h', (error, stderr, stdout) => {
    if (error) {
        console.log(`执行命令错误: ${error.message}`);
        return;
    }
    if (stderr) {
        console.log(`命令返回错误: ${stderr.message}`);
        return;
    }
    console.log(`磁盘使用情况: ${stdout}`);
});
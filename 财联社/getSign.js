const CryptoJS = require('./package/index')
// let lastTime = 1656841582

let arguments = process.argv.splice(2)

function getSign(lastTime){
    const url = `app=CailianpressWeb&category=&lastTime=${lastTime}&last_time=${lastTime}&os=web&refresh_type=1&rn=20&sv=7.7.5`
    const SHA1 = CryptoJS.SHA1(url).toString()
    const sign = CryptoJS.MD5(SHA1).toString()
    return sign
}
process.stdout.write(getSign(arguments[0]))


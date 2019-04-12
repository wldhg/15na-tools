const fs = require('fs')

const eof = Buffer.from('\u0003')
const num = [
  Buffer.from('0'),
  Buffer.from('1'),
  Buffer.from('2'),
  Buffer.from('3'),
  Buffer.from('4'),
  Buffer.from('5'),
  Buffer.from('6'),
  Buffer.from('7'),
  Buffer.from('8'),
  Buffer.from('9')
]

var y, name, time, behavior

const help = () => {
  console.info('Press <s> key to start record.')
  console.info('Press <e> key while recording to stop record.')
  console.info('Push the number key (<1> to <9>) once to record the start point of behavior, and again to record stop point.')
  console.info('Press <Ctrl> + <c> to exit.')
  console.log('============================================================================================================')
  console.warn('Do not use CAPS LOCK! Please turn off it.')
  console.info('Prepared to record Y. Read above instructions and start recording.')
}

process.stdin.setRawMode(true)
process.stdin.on('data', chunk => {
  if (chunk.toString() === 's') {
    // Start
    console.log('Wait for opening write stream...')
    var date = new Date()
    name = `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}_${date.getHours()}-${date.getMinutes()}-${date.getSeconds()}-${date.getMilliseconds()}.y`
    var _y = fs.createWriteStream(`./${name}`)
    _y.once('ready', () => {
      console.info('Write stream opened. Do it!')
      y = _y
      time = process.hrtime()[0]
    })
  } else if (chunk.toString() === 'e') {
    // End
    if (behavior) {
      console.warn('End a behavior before close stream!')
    } else if (y) {
      console.log('Closing stream...')
      y.on('close', () => {
        y = null
        console.info('Write stream is closed. File successfully saved.')
        console.log(`The name of saved y file is: ${name}`)
        console.log()
        help()
      })
      y.destroy()
    } else {
      console.warn('Write stream is not opened now.')
    }
  } else if (chunk > num[0] && chunk <= num[9]) {
    // Number
    var moment = process.hrtime()
    if (y) {
      if (behavior instanceof Buffer && behavior.compare(chunk) === 0) {
        y.write(`,${moment[0] - time}.${moment[1]}\n`)
        behavior = null
        console.log(`   └[-End-] ${chunk.toString()} th behavior.`)
      } else if (!behavior) {
        y.write(`${chunk.toString()},${moment[0] - time}.${moment[1]}`)
        behavior = num[chunk.toString()]
        console.log(`[Start] ${chunk.toString()} th behavior.`)
      }
    }
  } else if (chunk.compare(eof) === 0) {
    // EOF
    if (y) {
      console.warn('Press <e> to close y file before exit.')
    } else {
      process.exit()
    }
  }
})

help()

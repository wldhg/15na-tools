$(document).ready(() => {
  var sp = 0
  var ts = 0
  const tsData = $("#indicator-ts-data")[0]
  const rtsData = $("#indicator-rts-data")[0]
  const spData = $("#indicator-sp-data")[0]
  const ssBtn = $("#control-start-stop")[0]
  const ssLbl = $("#control-label")[0]
  const secY = $("#y")[0]
  const videoElement = $("#video-element")[0]
  var labelStarted = false
  var labelSp = 0
  var text = ""
  var vidName = ""
  const updateTs = (t) => {
    ts = t
    tsData.textContent = t
    rtsData.textContent = (Number(t) - Number(sp)).toFixed(6)
  }
  $("#control-load-video").click(() => {
    $("#hidden-file").trigger("click")
    return false
  })
  $("#control-set-sp").click(() => {
    sp = ts
    spData.textContent = Number(ts)
    rtsData.textContent = 0
  })
  $("#hidden-file").change((e) => {
    $("#video-element").attr("src", URL.createObjectURL(e.target.files[0]))
    sp = 0
    ts = 0
    labelStarted = false
    labelSp = 0
    tsData.textContent = "0"
    rtsData.textContent = "SP Unset"
    spData.textContent = "Unset"
    ssBtn.textContent = "Start"
    text = ""
    secY.innerHTML = ""
    vidName = e.target.files[0].name
    videoElement.playbackRate = 0.5
    videoElement.addEventListener('timeupdate', function () {
      updateTs(this.currentTime)
    })
  })
  $("#control-start-stop").click(() => {
    if (labelStarted) {
      var tempData = `${ssLbl.value},${labelSp},${(Number(ts) - Number(sp)).toFixed(6)}`
      text += `${tempData}\n`
      secY.innerHTML += `<span>${tempData}</span>`
      ssBtn.textContent = "Start"
      labelStarted = false
    } else {
      labelSp = (Number(ts) - Number(sp)).toFixed(6)
      ssBtn.textContent = "Stop"
      labelStarted = true
    }
  })
  $("#control-save-y-a").click(function (e) {
    $("#control-save-y-a").attr('download', `${vidName}.y`).attr('href', `data:application/octet-stream;base64,${btoa(text)}`)
  })
})

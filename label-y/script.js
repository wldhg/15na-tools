$(document).ready(() => {

  let sp = 0,
    ts = 0;
  const tsData = $("#indicator-ts-data")[0],
    rtsData = $("#indicator-rts-data")[0],
    spData = $("#indicator-sp-data")[0],
    ssBtn = $("#control-start-stop")[0],
    ssLbl = $("#control-label")[0],
    secY = $("#y")[0],
    videoElement = $("#video-element")[0];
  let labelSp = 0,
    labelStarted = false,
    text = "",
    vidName = "";
  const updateTs = (t) => {

    ts = t;
    tsData.textContent = t;
    rtsData.textContent = (Number(t) - Number(sp)).toFixed(6);

  };

  $("#control-load-video").click(() => {

    $("#hidden-file").trigger("click");

    return false;

  });
  $("#control-set-sp").click(() => {

    sp = ts;
    spData.textContent = Number(ts);
    rtsData.textContent = 0;

  });
  $("#hidden-file").change((e) => {

    $("#video-element").attr(
      "src",
      URL.createObjectURL(e.target.files[0])
    );
    sp = 0;
    ts = 0;
    labelStarted = false;
    labelSp = 0;
    tsData.textContent = "0";
    rtsData.textContent = "SP Unset";
    spData.textContent = "Unset";
    ssBtn.textContent = "Start";
    text = "";
    secY.innerHTML = "";
    vidName = e.target.files[0].name;
    videoElement.playbackRate = 0.50;
    videoElement.addEventListener(
      "timeupdate",
      function () {

        updateTs(this.currentTime);

      }
    );

  });
  $("#control-start-stop").click(() => {

    if (labelStarted) {

      const tempData = `${ssLbl.value},${labelSp},${(Number(ts) - Number(sp)).toFixed(6)}`;

      text += `${tempData}\n`;
      secY.innerHTML += `<span>${tempData}</span>`;
      ssBtn.textContent = "Start";
      labelStarted = false;

    } else {

      labelSp = (Number(ts) - Number(sp)).toFixed(6);
      ssBtn.textContent = "Stop";
      labelStarted = true;

    }

  });
  $("#control-save-y-a").click(() => {

    $("#control-save-y-a").attr(
      "download",
      `${vidName}.y`
    ).
      attr(
        "href",
        `data:application/octet-stream;base64,${btoa(text)}`
      );

  });
  let isPlay = false;

  $("#control-play-pause").click(() => {

    if (isPlay) {

      videoElement.pause();

    } else {

      videoElement.play();

    }
    isPlay = !isPlay;

  });
  $("#control-playback-10").click(() => {

    videoElement.playbackRate = 0.1;

  });
  $("#control-playback-25").click(() => {

    videoElement.playbackRate = 0.25;

  });
  $("#control-playback-50").click(() => {

    videoElement.playbackRate = 0.5;

  });
  $("#control-playback-100").click(() => {

    videoElement.playbackRate = 1;

  });

});

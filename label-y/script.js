$(document).ready(() => {

  let sp = 0,
    ts = 0;
  const tsData = $("#indicator-ts-data")[0],
    rtsData = $("#indicator-rts-data")[0],
    spData = $("#indicator-sp-data")[0],
    ssLbl = $("#control-label")[0],
    secY = $("#y")[0],
    videoElement = $("#video-element")[0];
  let labelSp = 0,
    labelStarted = false,
    text = "",
    vidName = "",
    videoLoaded = false;
  const updateTs = (t) => {

    ts = t;
    tsData.textContent = t;
    rtsData.textContent = (Number(t) - Number(sp)).toFixed(6);

  };

  $("#control-load-video").click(() => {

    if (!videoLoaded) {
      $("#hidden-file").trigger("click");
    } else if (confirm("Really reset all?")) {
      location.reload();
    }

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
    videoLoaded = true;
    labelStarted = false;
    labelSp = 0;
    tsData.textContent = "0";
    rtsData.textContent = "SP Unset";
    spData.textContent = "Unset";
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

    $("#control-play-pause").attr('disabled', false);
    $("#control-set-sp").attr('disabled', false);
    $("#control-start").attr('disabled', false);
    $("#control-load-video").text("Reset All");
    $("#video-name").text(vidName);
    $("#video-pbrate").text("x0.50");

  });
  const procSS = () => {

    if (labelStarted) {

      const tempData = `${ssLbl.value},${labelSp},${(Number(ts) - Number(sp)).toFixed(6)}`;

      text += `${tempData}\n`;
      secY.lastChild.outerHTML = `<span>${tempData}</span>`;
      labelStarted = false;
      $("#control-undo").attr('disabled', false);
      $("#control-save-y").attr('disabled', false);

    } else {

      labelSp = (Number(ts) - Number(sp)).toFixed(6);
      labelStarted = true;

      const tempData = `${ssLbl.value},${labelSp},[WaitForStop]`;
      secY.innerHTML += `<span style="opacity: 0.5">${tempData}</span>`;
      $("#control-undo").attr('disabled', true);
      $("#control-save-y").attr('disabled', true);

    }

  };
  $("#control-start").click(() => {
    procSS();
    $("#control-stop").attr('disabled', false);
    $("#control-start").attr('disabled', true);
  });
  $("#control-stop").click(() => {
    procSS();
    $("#control-start").attr('disabled', false);
    $("#control-stop").attr('disabled', true);
  });
  $("#control-undo").click(() => {
    if (text.length > 0) {
      text = text.substring(0, text.lastIndexOf('\n'));
      text = text.substring(0, text.lastIndexOf('\n') + 1);
      secY.removeChild(secY.lastChild);
      if (text.length === 0) {
        $("#control-undo").attr('disabled', true);
        $("#control-save-y").attr('disabled', true);
      }
    }
  });
  $("#control-save-y-a").click(() => {

    if (!document.getElementById('control-save-y').disabled) {
      $("#control-save-y-a").attr(
        "download",
        `${vidName.substring(0, vidName.lastIndexOf('.'))}.y`
      ).attr(
        "href",
        `data:application/octet-stream;base64,${btoa(text)}`
      );
    }

  });
  let isPlay = false;

  const cpp = $("#control-play-pause");
  cpp.click(() => {

    if (isPlay) {

      videoElement.pause();
      cpp.text("Play");

    } else {

      videoElement.play();
      cpp.text("Pause");

    }
    isPlay = !isPlay;

  });
  $("#control-playback-10").click(() => {

    videoElement.playbackRate = 0.1;
    $("#video-pbrate").text("x0.10");

  });
  $("#control-playback-25").click(() => {

    videoElement.playbackRate = 0.25;
    $("#video-pbrate").text("x0.25");

  });
  $("#control-playback-50").click(() => {

    videoElement.playbackRate = 0.5;
    $("#video-pbrate").text("x0.50");

  });
  $("#control-playback-100").click(() => {

    videoElement.playbackRate = 1;
    $("#video-pbrate").text("x1.00");

  });

});

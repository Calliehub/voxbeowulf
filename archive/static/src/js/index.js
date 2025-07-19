/* global $ */
import '../scss/index.scss';

import ajaxSendMethod from './ajax';
import handleMessageDismiss from './messages';

require('bootstrap/dist/js/bootstrap.bundle');

$(() => {
  $(document).ajaxSend(ajaxSendMethod);

  // Topbar active tab support
  $('.topbar li').removeClass('active');

  const classList = $('body').attr('class').split(/\s+/);
  $.each(classList, (index, item) => {
    const selector = `ul.nav li#tab_${item}`;
    $(selector).addClass('active');
  });

  $('#account_logout, .account_logout').click((e) => {
    e.preventDefault();
    $('#accountLogOutForm').submit();
  });

  handleMessageDismiss();

  var audio = document.getElementById("sound");
  var audioBehavior = document.getElementById("audio_behavior").value;
  var currentEnd = -1;
  var currentPosition = -1;
  var lastPlayedSegment;
  var lastVisibleSegment;
  var firstVisibleSegment;

  function playheadTracker() {
    currentPosition = audio.currentTime;

    // see if we need to pause when this halfline ends
    if (!audio.paused
        && document.getElementById("audio_behavior").value === "halfline"
        && currentPosition >= currentEnd) {
      console.log("Stopping audio at halfline boundary: " + currentPosition);
      stopAudio();
    }

    // are we playing past the end of what's visible?
    if (!audio.paused
        && lastVisibleSegment
        && currentPosition >= parseFloat(lastVisibleSegment.getAttribute("end"))) {
      console.log("Stopping audio at last visible segment's end: " + currentPosition);
      stopAudio();
    }
  }

  var playheadUpdater;

  function startAudio() {
    // 15ms interval helps make sure audio position updates are more frequent
    playheadUpdater = setInterval(playheadTracker, 15);
    audio.play();
  }

  function stopAudio() {
    clearInterval(playheadUpdater);
    audio.pause();
  }

  audio.addEventListener("play", () => {
    clearInterval(playheadUpdater);
    playheadUpdater = setInterval(playheadTracker, 15);
  });

  function setStart(seg, startPlaying) {
    var start = parseFloat(seg.getAttribute("start"));
    if (start >= 0) {
      currentPosition = start;
      currentEnd = parseFloat(seg.getAttribute("end"));
      audio.currentTime = start;
      if (startPlaying) {
        startAudio();
      }
      console.log("Setting start segment at " + currentPosition + "; currentEnd: " + currentEnd);
    }
  }

  Array.from(document.getElementsByTagName("seg")).forEach((seg) => {
    seg.addEventListener("click", (evt) => {
      setStart(seg, true);
    });
    if (!firstVisibleSegment) {
      firstVisibleSegment = seg;
      setStart(seg, false);
    }
  });

  audio.addEventListener("timeupdate", () => {
    currentPosition = audio.currentTime;
    Array.from(document.getElementsByTagName("seg")).forEach((seg) => {
      var start = parseFloat(seg.getAttribute("start"));
      if (start >= 0) {      // just skip over lines w/o a start time
        if (currentPosition >= start) {
          seg.classList.add("current");
          if (lastPlayedSegment && lastPlayedSegment !== seg) {
            lastPlayedSegment.classList.remove("current");
          }
          lastPlayedSegment = seg;
        } else {
          seg.classList.remove("current");
        }
        lastVisibleSegment = seg;
      }
    });
  });

});

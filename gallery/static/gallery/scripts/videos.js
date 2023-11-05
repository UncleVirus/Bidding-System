// JavaScript code for video functionality
const videoItems = document.querySelectorAll('.video-item');

videoItems.forEach(videoItem => {
  const overlay = videoItem.querySelector('.video-overlay');
  const video = videoItem.querySelector('video');
  const fullscreenButton = videoItem.querySelector('.video-fullscreen-button');

  overlay.addEventListener('click', () => {
    video.play();
    fullscreenButton.style.display = 'inline-block';
  });

  fullscreenButton.addEventListener('click', () => {
    if (videoItem.classList.contains('fullscreen')) {
      exitFullscreen();
    } else {
      enterFullscreen(videoItem);
    }
  });
});

function enterFullscreen(videoItem) {
  if (videoItem.requestFullscreen) {
    videoItem.requestFullscreen();
  } else if (videoItem.mozRequestFullScreen) {
    videoItem.mozRequestFullScreen();
  } else if (videoItem.webkitRequestFullscreen) {
    videoItem.webkitRequestFullscreen();
  } else if (videoItem.msRequestFullscreen) {
    videoItem.msRequestFullscreen();
  }

  videoItem.classList.add('fullscreen');
}

function exitFullscreen() {
  if (document.exitFullscreen) {
    document.exitFullscreen();
  } else if (document.mozCancelFullScreen) {
    document.mozCancelFullScreen();
  } else if (document.webkitExitFullscreen) {
    document.webkitExitFullscreen();
  } else if (document.msExitFullscreen) {
    document.msExitFullscreen();
  }

  const fullscreenVideoItem = document.querySelector('.video-item.fullscreen');
  if (fullscreenVideoItem) {
    fullscreenVideoItem.classList.remove('fullscreen');
  }
}
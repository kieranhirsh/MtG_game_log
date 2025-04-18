document.addEventListener('DOMContentLoaded', function() {
  let gif = document.getElementById('uh_uh_uh_gif');
  let mp3 = document.getElementById('uh_uh_uh_mp3');
  var uh_uh_uh_gif = '../static/img/uh_uh_uh.gif';

  mp3.addEventListener('canplaythrough', function() {
    gif.src = uh_uh_uh_gif;
  });
});

document.addEventListener('click', function() {
  document.getElementById('uh_uh_uh_mp3').play();
  document.removeEventListener('click', musicPlay);
});

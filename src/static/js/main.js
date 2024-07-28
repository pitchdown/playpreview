// 'use strict';


/**
 * 
 * @param {Window} jQuery 
 */
// Global
//
function closeDropDowns(e) {
  $("div[data-open]").hide();
}

$(window).click(closeDropDowns);
/**
 * 
 */

/**
 * Header User Control
 */
const userAvatarBTN = $('#user-avatar');
const userDropDown = $('#user-dropdown');

function userDropDownOpen(event) {
  event.stopPropagation();
  $(userDropDown).toggle();
  // $(userDropDown).data('open', true);
}

function userDropDownClick(event) {
  event.stopPropagation();
  console.log('--------')
}

userAvatarBTN.on('click', userDropDownOpen);
userDropDown.on('click', userDropDownClick);

/**
 * 
 */



/**
 * Global
 * Shared Components
 * 
 */


/**
 * Audio Playlist Controls
 */
let playingAudioId = null;

$('#tracks').on('click', '.play-track-click', function (e) {

  let trackItem = $(e.currentTarget).parents('.album-track-item');

  if (!trackItem.length) {
    trackItem = $(e.currentTarget);
  }

  const trackId = trackItem.data('id');
  const trackAudio = trackItem.find('audio')[0];
  const playButton = trackItem.find('.track-control-play');
  const pauseButton = trackItem.find('.track-control-pause');
  const seekbar = trackItem.find('.seekbar');
  const albumTracks = $(e.currentTarget).parents('.album-tracks');

  //


  if (playingAudioId && playingAudioId !== trackId) {
    const playingItem = albumTracks.find(`div[data-id="${playingAudioId}"]`);
    console.log(playingItem.find('audio'))
    playingItem.find('.track-control-play').show();
    playingItem.find('.track-control-pause').hide();
    playingItem.find('audio')[0].pause();
    playingItem.find('audio')[0].currentTime = 0;
    playingItem.removeClass('playing');

    // playingItem.currentTime = 0;
    // playingItem.find('.seekbar').attr("value", 0);
  }

  if (trackAudio.paused) {
    playButton.hide();
    pauseButton.show()
    trackAudio.play()
    playingAudioId = trackId;
    console.log('-----------------------------');
    $(trackAudio).on('timeupdate', function () {
      seekbar.attr("value", this.currentTime / this.duration);
      console.log('update');
    });
    trackItem.addClass('playing');


  } else {
    playButton.show();
    pauseButton.hide()
    trackAudio.pause();
    trackAudio.currentTime = 0;
    $(trackAudio).off('timeupdate', function () {
      console.log('off');
    });
    trackItem.removeClass('playing');
    playingAudioId = null;

  }

});
/** */

const sampleData = [
  {
    "album": "am",
    "album_cover": "https://i.scdn.co/image/ab67616d0000b2734ae1c4c5c45aabe565499163",
    "artists": [
      "Arctic Monkeys"
    ],
    "id": "5FVd6KXrgO9B3JPmC8OPst",
    "liked": true,
    "name": "do i wanna know?",
    "preview_url": "https://p.scdn.co/mp3-preview/006bc465fe3d1c04dae93a050eca9d402a7322b8?cid=6e82327445994df88d17de8cd6608f19",
    "track_number": 1
  },
  {
    "album": "am",
    "album_cover": "https://i.scdn.co/image/ab67616d0000b2734ae1c4c5c45aabe565499163",
    "artists": [
      "Arctic Monkeys"
    ],
    "id": "2AT8iROs4FQueDv2c8q2KE",
    "liked": true,
    "name": "r u mine?",
    "preview_url": "https://p.scdn.co/mp3-preview/d41c9b18f0787cc9b2ccea10740d92dd7e7f639a?cid=6e82327445994df88d17de8cd6608f19",
    "track_number": 2
  },
  {
    "album": "am",
    "album_cover": "https://i.scdn.co/image/ab67616d0000b2734ae1c4c5c45aabe565499163",
    "artists": [
      "Arctic Monkeys"
    ],
    "id": "6wNUBZNWFxdUGof6vkaykE",
    "liked": false,
    "name": "one for the road",
    "preview_url": "https://p.scdn.co/mp3-preview/8ad968049796e1234d20eba15c62de83d188c9f0?cid=6e82327445994df88d17de8cd6608f19",
    "track_number": 3
  },
  {
    "album": "am",
    "album_cover": "https://i.scdn.co/image/ab67616d0000b2734ae1c4c5c45aabe565499163",
    "artists": [
      "Arctic Monkeys"
    ],
    "id": "7nzsY8vlnKdvGOEE0rjAXZ",
    "liked": false,
    "name": "arabella",
    "preview_url": "https://p.scdn.co/mp3-preview/974bb8b08005bbc3c38a3b1389debf8e51fa1f20?cid=6e82327445994df88d17de8cd6608f19",
    "track_number": 4
  },
  {
    "album": "am",
    "album_cover": "https://i.scdn.co/image/ab67616d0000b2734ae1c4c5c45aabe565499163",
    "artists": [
      "Arctic Monkeys"
    ],
    "id": "1j9rezdE3YeC7yktZXC1em",
    "liked": true,
    "name": "i want it all",
    "preview_url": "https://p.scdn.co/mp3-preview/350cfa8b115df3bf6a843c13635fe741247bb68f?cid=6e82327445994df88d17de8cd6608f19",
    "track_number": 5
  },
  {
    "album": "am",
    "album_cover": "https://i.scdn.co/image/ab67616d0000b2734ae1c4c5c45aabe565499163",
    "artists": [
      "Arctic Monkeys"
    ],
    "id": "5TTGoX70AFrTvuEtqHK37S",
    "liked": false,
    "name": "no. 1 party anthem",
    "preview_url": "https://p.scdn.co/mp3-preview/ba38bc9842d486d94889a7803367737dc011db7f?cid=6e82327445994df88d17de8cd6608f19",
    "track_number": 6
  },
  {
    "album": "am",
    "album_cover": "https://i.scdn.co/image/ab67616d0000b2734ae1c4c5c45aabe565499163",
    "artists": [
      "Arctic Monkeys"
    ],
    "id": "75n7mraeMycQOl2sDGYaTe",
    "liked": false,
    "name": "mad sounds",
    "preview_url": "https://p.scdn.co/mp3-preview/439a1d690e8ccf29e67a623da8affa8437cd3305?cid=6e82327445994df88d17de8cd6608f19",
    "track_number": 7
  },
  {
    "album": "am",
    "album_cover": "https://i.scdn.co/image/ab67616d0000b2734ae1c4c5c45aabe565499163",
    "artists": [
      "Arctic Monkeys"
    ],
    "id": "4atMrAadB7dS8xn9vfk9PQ",
    "liked": false,
    "name": "fireside",
    "preview_url": "https://p.scdn.co/mp3-preview/9d8d30ca185e36269b78f26111074c4f10f3f57a?cid=6e82327445994df88d17de8cd6608f19",
    "track_number": 8
  },
  {
    "album": "am",
    "album_cover": "https://i.scdn.co/image/ab67616d0000b2734ae1c4c5c45aabe565499163",
    "artists": [
      "Arctic Monkeys"
    ],
    "id": "086myS9r57YsLbJpU0TgK9",
    "liked": false,
    "name": "why'd you only call me when you're high?",
    "preview_url": "https://p.scdn.co/mp3-preview/be5453a4763510679fab61e39662ab0257458be6?cid=6e82327445994df88d17de8cd6608f19",
    "track_number": 9
  },
  {
    "album": "am",
    "album_cover": "https://i.scdn.co/image/ab67616d0000b2734ae1c4c5c45aabe565499163",
    "artists": [
      "Arctic Monkeys"
    ],
    "id": "0NdTUS4UiNYCNn5FgVqKQY",
    "liked": false,
    "name": "snap out of it",
    "preview_url": "https://p.scdn.co/mp3-preview/f2ab7daa4bbd9ad5889c0dda818c40fe60b66406?cid=6e82327445994df88d17de8cd6608f19",
    "track_number": 10
  },
  {
    "album": "am",
    "album_cover": "https://i.scdn.co/image/ab67616d0000b2734ae1c4c5c45aabe565499163",
    "artists": [
      "Arctic Monkeys"
    ],
    "id": "2LGdO5MtFdyphi2EihANZG",
    "liked": false,
    "name": "knee socks",
    "preview_url": "https://p.scdn.co/mp3-preview/1760b337ef613459a069b961a1bedf65b8c1bc3f?cid=6e82327445994df88d17de8cd6608f19",
    "track_number": 11
  },
  {
    "album": "am",
    "album_cover": "https://i.scdn.co/image/ab67616d0000b2734ae1c4c5c45aabe565499163",
    "artists": [
      "Arctic Monkeys"
    ],
    "id": "5XeFesFbtLpXzIVDNQP22n",
    "liked": false,
    "name": "i wanna be yours",
    "preview_url": "https://p.scdn.co/mp3-preview/07de30bde8363d9ff78b72339245c151f67af451?cid=6e82327445994df88d17de8cd6608f19",
    "track_number": 12
  }
]


function sleep(ms = 100) {
  return new Promise((res) => {
    setTimeout(() => {
      res(true)
    }, ms);
  })
}

let testCase = !true;

$(document).ready(async function () {
  if (window.location.pathname.startsWith('/album/')) {
    var albumId = $('#tracks').data('album-id');
    var tracksHtml;
    if (testCase) {
      await sleep(2000);
      sampleData.forEach(function (track, index) {
        let trackNumber = index + 1;
        let artists = track.artists_name.join('/').toLowerCase();
        let likeImage = track.liked ? '/static/img/like.svg' : '/static/img/like.png';
        tracksHtml += `
                      <div class="album-track-item"  data-playlist-action="toggle" data-playlist-item="${track.id}">
                                <div class="track-num">
                                    ${trackNumber < 10 ? '0' + trackNumber : trackNumber}
                                </div>
                                <div class="track-controls"  >
                                    <div data-playlist-action="play" class="track-control track-control-play play-track">
                                     <i class="fa-solid fa-play"></i>
                                    </div>
                                    <div data-playlist-action="pause" class="track-control track-control-pause play-track hidden">
                                     <i class="fa-solid fa-pause"></i>
                                    </div>
<!--                                <img src="/static/img/play.svg" class="play-track w-6 cursor-pointer mr-6">-->
                                <audio  controls style="display: none;">
                                    <source src="${track.preview_url}" type="audio/ogg">
                                    <source src="${track.preview_url}" type="audio/mpeg">
                                </audio>
                                </div>


                            <div class="track-desc">
                                <p class="track-title">${track.name}</p>
                                <p class="text-artist">${artists}</p>
                                <p class="text-duration" data-playlist-item-duration></p>

                            </div>
                            <div class="track-form">
                                <form action="" id="like-form" method="POST">
                                    <input type="hidden" name="id" value="${track.id}">
                                    <input type="hidden" name="name" value="${track.name}">
                                    <input type="hidden" name="album_name" value="${track.album_name}">
                                    <input type="hidden" name="album_id" value="${track.album_id}">
                                    <input type="hidden" name="album_cover" value="${track.album_cover}">
                                    <input type="hidden" name="artists_name" value="${artists}">
                                    <input type="hidden" name="preview_url" value="${track.preview_url}">
                                    <button class="like-button" type="button">
                                        <img src="${likeImage}" class="w-7 icon">
                                    </button>
                              </form>
                            </div>
                            <div class="track-progress" data-playlist-progress>
                              <input
                                data-playlist-action="seeking"
                                type="range"
                                min="0.0"
                                max="100"
                                value="0.0"
                                step="0.01"
                                class="slider"
                              />
                            <progress class="seekbar" value="0" max="1" ></progress>
                            </div>
                      </div>`;
      });
      $('#tracks').html(tracksHtml);
      initPlaylistPlayer($('#tracks'));
    } else {
      $.ajax({
        url: '/album/' + albumId + '/tracks',
        method: 'GET',
        success: function (data) {
          let tracksHtml = '';
          console.log(data)
          data.forEach(function (track, index) {
            console.log('track', track);
            // return;
            let trackNumber = index + 1;
            let artists = track.artists_name.join('/').toLowerCase();
            let likeImage = track.liked ? '/static/img/like.svg' : '/static/img/like.png';
            tracksHtml += `<div class="album-track-item"  data-playlist-action="toggle" data-playlist-item="${track.id}">
                                <div class="track-num">
                                    ${trackNumber < 10 ? '0' + trackNumber : trackNumber}
                                </div>
                                <div class="track-controls"  >
                                    <div data-playlist-action="play" class="track-control track-control-play play-track">
                                     <i class="fa-solid fa-play"></i>
                                    </div>
                                    <div data-playlist-action="pause" class="track-control track-control-pause play-track hidden">
                                     <i class="fa-solid fa-pause"></i>
                                    </div>
<!--                                <img src="/static/img/play.svg" class="play-track w-6 cursor-pointer mr-6">-->
                                <audio  controls style="display: none;">
                                    <source src="${track.preview_url}" type="audio/ogg">
                                    <source src="${track.preview_url}" type="audio/mpeg">
                                </audio>
                                </div>


                            <div class="track-desc">
                                <p class="track-title">${track.name}</p>
                                <p class="text-artist">${artists}</p>
                                <p class="text-duration" data-playlist-item-duration></p>

                            </div>
                            <div class="track-form">
                                <form action="" id="like-form" method="POST">
                                    <input type="hidden" name="id" value="${track.id}">
                                    <input type="hidden" name="name" value="${track.name}">
                                    <input type="hidden" name="album_name" value="${track.album_name}">
                                    <input type="hidden" name="album_id" value="${track.album_id}">
                                    <input type="hidden" name="album_cover" value="${track.album_cover}">
                                    <input type="hidden" name="artists_name" value="${artists}">
                                    <input type="hidden" name="artists_id" value="${track.artists_id}">
                                    <input type="hidden" name="preview_url" value="${track.preview_url}">
                                    <button class="like-button" type="button">
                                        <img src="${likeImage}" class="w-7 icon">
                                    </button>
                              </form>
                            </div>
                            <div class="track-progress" data-playlist-progress>
                              <input
                                data-playlist-action="seeking"
                                type="range"
                                min="0.0"
                                max="100"
                                value="0.0"
                                step="0.01"
                                class="slider"
                              />
                            <progress class="seekbar" value="0" max="1" ></progress>
                            </div>
                      </div>`;
          });

          $('#tracks').html(tracksHtml);
          initPlaylistPlayer($('#tracks'));
          $('.like-button').click(function (e) {
            e.stopPropagation();
            let icon = $(this).find('.icon');
            let formData = $(this).closest('form').serialize();
            let trackId = $(this).closest('form').find('input[name="id"]').val();
            if (icon.attr('src') === '/static/img/like.png') {
              icon.attr('src', '/static/img/like.svg');
              $.ajax({
                url: '/like-track/' + trackId,
                type: 'POST',
                data: formData,
              });
            } else {
              icon.attr('src', '/static/img/like.png');
              $.ajax({
                url: '/unlike-track/' + trackId,
                type: 'POST',
                data: formData,
              });
            }
          });
        },
        error: function (xhr, status, error) {
          console.error('Error fetching tracks:', error);
          $('#tracks').html('<p>Failed to load tracks.</p>');
        }
      });
    }
  }
});



/**
 * Playlist Scope
 * 
 * 
 * 
 */

function formatTime(seconds) {
  minutes = Math.floor(seconds / 60);
  minutes = (minutes >= 10) ? minutes : "0" + minutes;
  seconds = Math.floor(seconds % 60);
  seconds = (seconds >= 10) ? seconds : "0" + seconds;
  return minutes + ":" + seconds;
}

/**
 * Playlist initialize
 */
const initPlaylistPlayer = (targetEl) => {
  const playListElement = $(targetEl);
  const playListId = playListElement.data('playlist')

  const uiEventHandler = function (e) {
    if (e.target instanceof HTMLAnchorElement) {
      return;
    }
    // e.preventDefault();
    e.stopPropagation();
    const eventTarget = $(e.currentTarget);
    const itemElement = eventTarget.data('playlistItem') ? eventTarget : eventTarget.parents('[data-playlist-item]');
    const audioTarget = itemElement.find('audio')[0];


    // events 
    const eventAction = eventTarget.data('playlistAction');
    // console.log('seeking', $(e));
    console.log(audioTarget.paused);

    switch (eventAction) {
      case 'play':
        console.log('play');
        audioTarget.play();
        break;
      case 'pause':
        audioTarget.pause();
        break;
      case 'toggle':

        if (!audioTarget.paused) {
          audioTarget.pause();
          break;
        } else {
          audioTarget.play();
        }
        break;
      case 'seeking':
        console.log('seeking', $(e));
        // audioTarget.currentTime = (audioTarget.duration / 100) * this.value;
        // audioTarget.play()
        break;

      default:
        break;
    }
  };

  playListElement.on('click', '[data-playlist-action]', uiEventHandler);

  /**
   * Audio Element Events
   * 
   */
  let playingItem = null;

  function audioEventHandler(e) {
    e.stopPropagation();
    e.preventDefault();
    const _playlistElement = $(this).parents(`[data-playlist-item]`)
    const _playingItem = _playlistElement.data('playlistItem');
    const playBtn = $(_playingItem).find('[data-playlist-action="play"]') || null;
    const pauseBtn = $(_playingItem).find('[data-playlist-action="pause"]') || null;

    // console.log('-----------', progressBar);

    switch (e.type) {
      case 'play':
        if (playingItem === null) {
          playingItem = _playingItem;
        }

        // console.log($(_playlistElement).find('[data-playlist-action="play"]')[1]);

        // !!!!
        // $(playListElement).find('audio').each((key, e) => {
        //   console.log('---', e, $(e).parents('[data-playlist-item]'));
        //   if (!$(e).parents('[data-playlist-item]').is(_playlistElement) && e && !e.paused) {
        //     e.pause()
        //   }
        // });

        if (playingItem && playingItem !== _playingItem) {
          // $(playListElement).find(`[data-playlist-item=${playingItem}] > audio`)[0].pause()
          // $($(playListElement).find(`[data-playlist-item=${playingItem}]`)).find('audio')[0].pause();
          $(playListElement).find('audio').each((key, e) => {
            // console.log('---', e, $(e).parents('[data-playlist-item]'));
            const playingAudio = $(e).parents('[data-playlist-item]');
            if (!$(playingAudio).is(_playlistElement) && e && !e.paused) {
              e.pause()
              // $(_playlistElement).find('[data-playlist-action="play"]').hide()
              // $(_playlistElement).find('[data-playlist-action="pause"]').show()
            }
          });

          playingItem = _playingItem;
        }
        break;
      case 'seeking':
        if (_playingItem !== playingItem) {
          this.play();
        }
        break;
      case 'timeupdate':
        const progressElement = $(_playlistElement).find('[data-playlist-action="progress"]');
        const sliderElement = $(_playlistElement).find('[data-playlist-action="seeking"]');

        if (!this.paused) {
          $($(_playlistElement).find('[data-playlist-action="pause"]')).show()
          $($(_playlistElement).find('[data-playlist-action="play"]')).hide()

          _playlistElement.find('[data-playlist-item-duration]').html(`<div><span style="width: 45px; display: inline-block;">${formatTime(this.currentTime)}</span><span> - </span><span style="width: 45px; display: inline-block;">${formatTime(this.duration)}</span></div>`)

        } else {
          $($(_playlistElement).find('[data-playlist-action="pause"]')).hide()
          $($(_playlistElement).find('[data-playlist-action="play"]')).show()
        }

        if (progressElement) {
          progressElement.css("width", (this.currentTime / this.duration) * 100 + '%');
          progressElement.attr("data-playlist-progress-value", this.currentTime / this.duration);
        }
        if (sliderElement) {
          $(sliderElement).val((this.currentTime / this.duration) * 100);
        }
        break;
      default:
        break;
    }
  }

  playListElement.find('[data-playlist-item]').each(function (key, element) {
    console.log($(this).find('audio'));

    if ($(this).find('audio')[0]) {
      // console.log($.data, $(this).find('audio')[0].ontimeupdate, $(document.body).data('events'));
      const playlistItem = $(element).data('playlistItem');
      const audioEl = $($(element).find('audio')[0]);
      const slideEl = $($(element).find('.slider'));
      const el = $(element).find('audio')[0];


      const progresbarHTML = ` <input
                                    data-playlist-action="seeking"
                                    type="range"
                                    min="0.0"
                                    max="100"
                                    value="0.0"
                                    step="0.01"
                                    class="slider"
                                  />
                                  `;
      const seekBarHTML = `
              <progress class="seekbar" value="0" max="1" data-playlist-action="progress"></progress>
              `;

      const progressBar = $(element).find('[data-playlist-action="progress"]');
      const seekBar = $(element).find('[data-playlist-action="seeking"]');

      // $(progressBar).replaceWith(progresbarHTML)
      // $(seekBar).replaceWith(seekBarHTML)
      // console.log('---------------', progresbarHTML);

      if ($(this).find('audio')[0].onplay) {
        console.log('------ onplay');
        return;
      }

      $(slideEl).on('input', function (e) {
        const _playlistElement = $(this).parents(`[data-playlist-item]`)
        const _audioEl = $(_playlistElement).find('audio')[0];
        if (_audioEl.preload === 'none') {
          _audioEl.load();
        } else {
        }
        _audioEl.currentTime = ($(_playlistElement).find('audio')[0].duration / 100) * this.value;
        _audioEl.play();
      })

      audioEl.on('loadedmetadata', function () {
        const slideEl = $($(element).find('.slider'));
        // console.log('---------------------------------------------', slideEl.value, this.duration);
        // this.currentTime = (this.duration / 100) * slideEl[0].value;
        // this.play();
        $(element).find('[data-playlist-item-duration]').html(`<div><span style="width: 45px; display: inline-block;">${formatTime(this.currentTime)}</span><span> - </span><span style="width: 45px; display: inline-block;">${formatTime(this.duration)}</span></div>`)
        console.log('[LoadDone]');
      });

      // Native Audi Element Event Handlers
      // audioEl.on("play", audioEventHandler);
      // audioEl.on("seeking", audioEventHandler);
      // audioEl.on("timeupdate", audioEventHandler);
      console.log('audioEl', audioEl);
      // audioEl[0].onplay = function() {
      //   console.log('play');
      // };
      audioEl[0].onplay = audioEventHandler;
      audioEl[0].onseeking = audioEventHandler;
      audioEl[0].ontimeupdate = audioEventHandler;
    }
  });



  return {
    playlistId: playListId
  }
}

const _initPlaylistPlayer = (targetEl) => {
  const playlistElement = targetEl;
  const playlistItems = $(playlistElement.find('[data-playlist-item]'));
  playlistItems.each((key, item) => {
    console.log('--', $.data(item, 'events'));
    $(item).on('click', function () {
      console.log('------ click');
    })
    if (item.onclick) {
      return
    }
    console.log('playlistItems', key, item.onclick);

    item.onclick = function (e) {
      console.log('-------', e.target, e.currentTarget);
    }
  })


  console.log('playlistItems', playlistItems.onclick);
}

const scopeQuery = '[data-playlist]';

function initApp(options) {
  $(scopeQuery).each((key, playlist) => {
    initPlaylistPlayer($(playlist));
  });
}

/**
 * Boostrap app
 */
(function () {
  $(document).ready(() => {
    initApp();
    // $.fn.extend(generatePlaylist(this));
  })
})($);


//
//
//
class PlaylistTrack {
  id = null;
  isPlaying = false;
  audiEl = null;

  constructor(e) {

  }
}

class GeneratePlaylist {
  playlistEl = null;

  constructor(e) {
    console.log(e);
    this.playlistEl = e;
    this.#initAudioEvents();
  }

  #initAudioEvents() {
    this.playlistEl.find('audio').each((key, item) => {
      this.trackList.push($(item));
    });
    console.log();
  }
}

const generatePlaylist = function (e) {
  console.log('[generatePlaylist]', e, this);
  const _playlist = this;

  if (!this) { return };

  _playlist.find('audio').on('play', function () {
    console.log('---');
  })

  return {
    some: '() => {}'
  }
}
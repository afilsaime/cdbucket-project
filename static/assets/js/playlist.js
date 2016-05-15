    $(document).ready(function(){
        // ========= jPlayer config 1 ==========
        // Home player, Track player, Single post top player
        var myPlaylist = new jPlayerPlaylist({
            jPlayer: "#jquery_jplayer_N",
            cssSelectorAncestor: "#jp_container_N"
        }, [
            {
                artist: "Tensnake ", // the artist name
                title:"See Right Through ft. Fiora", // track title
                mp3:"assets/audio/flute.mp3",// mp3 path
                oga:"assets/audio/flute.mp3",// oga path
                poster: "assets/img/albums/cover2.jpg",// poster image path
                duration: '03:29',// duration time in playlist
                buy1: '#buy1',
                buy2: '#buy2',
                buy3: '#buy3'
            },
            {
                artist: "Jack Ü ",
                title:"Take Ü There feat. Kiesza",
                mp3:"assets/audio/2.mp3",
                oga:"assets/audio/2.mp3",
                poster: "assets/img/albums/cover1.jpg",
                duration: '05:41',
                buy1: '#buy1',
                buy2: '#buy2',
                buy3: '#buy3'
            },
            {
                artist: "Bos Sinclair",
                title:"Cinderella",
                mp3:"assets/audio/3.mp3",
                oga:"assets/audio/3.mp3",
                poster: "assets/img/albums/cover3.jpg",
                duration: '04:05',
                buy1: '#buy1',
                buy2: '#buy2',
                buy3: '#buy3'
            },
            {
                artist: "Yiuna",
                title:"Lullabies",
                mp3:"assets/audio/4.mp3",
                oga:"assets/audio/4.mp3",
                poster: "assets/img/albums/cover4.jpg",
                duration: '04:27',
                buy1: '#buy1',
                buy2: '#buy2',
                buy3: '#buy3'
            },
            {
                artist: "Tensnake ", // the artist name
                title:"See Right Through ft. Fiora", // track title
                mp3:"assets/audio/flute.mp3",// mp3 path
                oga:"assets/audio/flute.mp3",// oga path
                poster: "assets/img/albums/cover2.jpg",// poster image path
                duration: '03:29',// duration time in playlist
                buy1: '#buy1',
                buy2: '#buy2',
                buy3: '#buy3'
            },
            {
                artist: "Jack Ü ",
                title:"Take Ü There feat. Kiesza",
                mp3:"assets/audio/2.mp3",
                oga:"assets/audio/2.mp3",
                poster: "assets/img/albums/cover1.jpg",
                duration: '05:41',
                buy1: '#buy1',
                buy2: '#buy2',
                buy3: '#buy3'
            },
            {
                artist: "Bos Sinclair",
                title:"Cinderella",
                mp3:"assets/audio/3.mp3",
                oga:"assets/audio/3.mp3",
                poster: "assets/img/albums/cover3.jpg",
                duration: '04:05',
                buy1: '#buy1',
                buy2: '#buy2',
                buy3: '#buy3'
            },
            {
                artist: "Yiuna",
                title:"Lullabies",
                mp3:"assets/audio/4.mp3",
                oga:"assets/audio/4.mp3",
                poster: "assets/img/albums/cover4.jpg",
                duration: '04:27',
                buy1: '#buy1',
                buy2: '#buy2',
                buy3: '#buy3'
            }
        ], {
            swfPath: "assets/jplayer/jplayer",
            supplied: "oga, mp3",
            wmode: "window",
            useStateClassSkin: true,
            autoBlur: false,
            smoothPlayBar: true,
            keyEnabled: true,
            size: {width: "80px", height: "80px"},
            loop: true
        });
        // Show The Current Track !!
        $("#jquery_jplayer_N").on(
            $.jPlayer.event.ready + ' ' + $.jPlayer.event.play,
            function(event){
                var current = myPlaylist.current;
                var playlist = myPlaylist.playlist;       
                $.each(playlist, function (index, obj) {
                    if (index == current) {
                        $("#nowPlaying").html("<span class='track-name'>" + obj.title + "</span>" + "<br>" + "<span class='artist-name'>" + obj.artist + "</span>");
                        $("#nowPlaying").html("<span class='track-name'>" + obj.title + "</span>" + "<br>" + "<span class='artist-name'>" + obj.artist + "</span>");
                    }
                });
            }
        );

        // Sidebar tracks
       $(".featured-songs").find(".song").on('click', function(e) {
          e.preventDefault();

           if ($(this).hasClass('play')) {
               myPlaylist.pause();
    //           $(".featured-songs").find(".song").addClass("play");
               $(".featured-songs").find(".song").not($this).removeClass("play");
               $(this).find('i').removeClass('fa-pause').addClass('fa-play');
           } else {
               var $this = $(this);
               myPlaylist.add({
                   mp3: $this.attr("data-mp3"),
                   artist: $this.attr("data-artist"),
                   title: $this.attr("data-song"),
                   poster:$this.attr("data-poster")
               });
               myPlaylist.play(-1);
               $(".featured-songs").find(".song").not($this).removeClass("play");
               $this.toggleClass("play");

               $(".featured-songs").find('.song i').removeClass('fa-pause').addClass('fa-play');
               $(this).find('i').removeClass('fa-play').addClass('fa-pause');
               return false;
           }
       });//End Click

        $('.jp-play').click(function() {
            if ( $(this).closest('.jplayer-home').hasClass('jp-state-playing') ) {
                $('.btnPlay').removeClass('play');
                $('.btnPlay').find('i').removeClass('fa-pause').addClass('fa-play');

                $('.jp-playlist ul li').removeClass('jp-playlist-current')
                $('.jp-playlist ul li .jp-playlist-item').removeClass('jp-playlist-current')
            }
        });

        $('.jplayerButton').one('click', function() {
            $('.jp-playlist ul li').removeClass('jp-playlist-current');
            $('.jp-playlist ul li a.jp-playlist-item').removeClass('jp-playlist-current');

            $('.jp-playlist-item').click(function() {
                if ($(this).hasClass('jp-playlist-current')) {
                    myPlaylist.pause();
                }
                $(this).addClass('jp-playlist-current');
                $(this).find('ul li a.jp-playlist-item').addClass('jp-playlist-current');
            });
        });


    });

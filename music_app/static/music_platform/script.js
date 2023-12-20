const called_songs = []

function call_api(artist_id, user_id, song_id) {
    
    if (!called_songs.includes(song_id))
    {
        called_songs.push(song_id);
        const requestData = {
            user: user_id,
            artist: artist_id
        };

        
        fetch('/api/add_user_click/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        })
        .catch(error => {
            
            console.error('Error fetching data:', error);
        });
    }
}


let handle_user_click = (artist_id, user_id, song_id) => {
    var audio = document.getElementById(song_id);

    if (audio.paused) {
        audio.play();
        call_api(artist_id, user_id, song_id);
    } else {
        audio.pause();
    }
};
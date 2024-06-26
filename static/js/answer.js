function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const answer = () => {
    const cards = document.querySelectorAll('.answer_card')
    for(const card of cards)
    {
        const truth_checkbox = card.querySelector('.truth-checkbox')
        const like_counter = card.querySelector('.like-counter')
        
        const answerId = card.dataset.answerId
        

        like_counter.addEventListener('click', () => {

            const request = new Request(`${answerId}/like_async_answer`, {
                method : 'post',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken' : getCookie('csrftoken'),
                    
                }})
            
            
            
            fetch(request)
                .then((response) => response.json())
                .then((data) => like_counter.innerHTML = data.likes_count)
            
        })
        truth_checkbox.addEventListener('click', () => {

            const request = new Request(`${answerId}/checkbox_async_answer`, {
                method : 'post',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken' : getCookie('csrftoken'),
                    
                }})
            
            
            
            fetch(request)
                .then((response) => response.json())
                .then((data) => truth_checkbox.checked = data.truth_checkbox)
            
        })
    }
}


answer()
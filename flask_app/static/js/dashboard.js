const likeButton = document.getElementById('like-button');
const likeCountElement = document.getElementById('like-count');

let likeCount = parseInt(getCookie('likeCount')) || 0;
let isLiked = getCookie('isLiked') === 'true';

likeCountElement.innerText = likeCount;

if (isLiked) {
  likeButton.classList.add('liked');
}

likeButton.addEventListener('click', () => {
  if (isLiked) {
    likeCount--;
    isLiked = false;
    likeButton.classList.remove('liked');
  } else {
    likeCount++;
    isLiked = true;
    likeButton.classList.add('liked');
  }

  likeCountElement.innerText = likeCount;
  setCookie('likeCount', likeCount.toString(), 365);
  setCookie('isLiked', isLiked.toString(), 365);
});

function setCookie(name, value, days) {
  const expires = new Date();
  expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
  document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
}

function getCookie(name) {
  const cookieArr = document.cookie.split(';');
  for (let i = 0; i < cookieArr.length; i++) {
    const cookiePair = cookieArr[i].split('=');
    if (name === cookiePair[0].trim()) {
      return cookiePair[1];
    }
  }
  return null;
}



function popUp (element) {
    element.remove();
}



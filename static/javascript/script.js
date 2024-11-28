const parallaxContainer = document.querySelector('body');

parallaxContainer.style.backgroundImage = 'url("/static/images/background.png")';

function parallaxEffect() {
  const scrollPosition = window.scrollY;
  const backgroundOffset = scrollPosition * 0.4;
  parallaxContainer.style.backgroundPositionY = `${backgroundOffset}px`;
}

window.addEventListener('scroll', parallaxEffect);

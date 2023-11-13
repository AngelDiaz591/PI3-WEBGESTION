const scrollableButtons = document.querySelector('.scrollable-buttons');
const scrollRightButton = document.querySelector('.scroll-button.right-button');
const scrollLeftButton = document.querySelector('.scroll-button.left-button');
const buttonWidth = document.querySelector('.configurable-button').offsetWidth;

scrollLeftButton.addEventListener('click', () => {
  scrollButtons(1);
});

scrollRightButton.addEventListener('click', () => {
  scrollButtons(-1);
});

function scrollButtons(direction) {
  const currentScrollPosition = scrollableButtons.scrollLeft;
  const targetScrollPosition = currentScrollPosition + direction * buttonWidth;

  scrollableButtons.scrollTo({
    left: targetScrollPosition,
    behavior: 'smooth' // Hace que el desplazamiento sea suave
  });
}


















/**
 * This script is used to show the delete confirmation button when the delete button is clicked
 * on the Admin page.
 */
const deleteConfirm = document.getElementsByClassName('delete-button')[0];
deleteConfirm.addEventListener('click', function () {
  const deleteBtn = this.parentNode.querySelector('.delete-confirm');
  deleteBtn.classList.toggle('hide');
});

/**
 * This script is used to hide the delete confirmation button when the cancel button is clicked
 */
const cancelDelete = document.getElementsByClassName('cancel-delete')[0];
cancelDelete.addEventListener('click', function () {
  this.parentNode.parentNode.parentNode.classList.toggle('hide');
});

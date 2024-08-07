/**
 * This script is used to show the delete confirmation button when the delete button is clicked
 * on the Admin page.
 */
const deleteConfirm = document.getElementsByClassName('delete-button');
// for each element
for (let i = 0; i < deleteConfirm.length; i++) {
  deleteConfirm[i].addEventListener('click', function () {
    const deleteBtn = this.parentNode.querySelector('.btn');
    deleteBtn.parentNode.querySelector('.delete-confirm').classList.toggle('hide');
  });
}

/**
 * This script is used to hide the delete confirmation button when the cancel button is clicked
 */
const cancelDelete = document.getElementsByClassName('cancel-delete');

for (let i = 0; i < cancelDelete.length; i++) {
  cancelDelete[i].addEventListener('click', function () {
    const dialogue = this.parentNode.parentNode.parentNode;
    dialogue.classList.toggle('hide');

    

  });
}

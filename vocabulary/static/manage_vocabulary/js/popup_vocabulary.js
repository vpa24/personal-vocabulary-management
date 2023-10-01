document.addEventListener("DOMContentLoaded", function () {
  const vocabModal = document.getElementById("vocabulary_popup");
  vocabModal.addEventListener("show.bs.modal", (event) => {
    const vocabulary = event.relatedTarget;
    const voabulary_name = vocabulary.getAttribute("data-bs-vocab-name");
    const modalTitle = vocabModal.querySelector(".modal-title");
    modalTitle.textContent = `${voabulary_name}`;
    load_vocabulary_detail(voabulary_name);
  });
});
function detail_template(word) {
  return `<div class="list-group">
    <div class="list-group-item py-3">
      <div class="end-0 top-0 pt-3 pe-3 position-absolute">
       
      </div>
       
      <p class="font-weight-normal">
        <span class="${word.class}">${word.type}</span>
        <span class="opacity-75">${word.definition}</span>
      </p>
      
      <h6 class="opacity-75 text-decoration-underline">Example:</h6>
      <p>${word.example}</p>
    </div>
  </div>`;
}
function load_vocabulary_detail(vocabulary_name) {
  fetch(`/dictionary-detail/${vocabulary_name}`)
    .then((response) => response.json())
    .then((result) => {
      document.querySelector(".modal-body").innerHTML = detail_template(
        result[0]
      );
      console.log(result);
    });
}

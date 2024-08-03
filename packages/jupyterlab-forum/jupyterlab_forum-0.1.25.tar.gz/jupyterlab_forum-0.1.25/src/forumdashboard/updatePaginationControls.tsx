export function updatePaginationControls(widget: any, allThemeslength: number, themesPerPage: number) {

    const paginationControls = widget.node.querySelector('#pagination-controls');
    if (!paginationControls) return;

    const totalPages = Math.ceil(allThemeslength / themesPerPage);
    let paginationHTML = '';

    for (let i = 1; i <= totalPages; i++) {
        paginationHTML += `<button class="page-link" data-page="${i}">${i}</button>`;
    }

    paginationControls.innerHTML = paginationHTML;
}

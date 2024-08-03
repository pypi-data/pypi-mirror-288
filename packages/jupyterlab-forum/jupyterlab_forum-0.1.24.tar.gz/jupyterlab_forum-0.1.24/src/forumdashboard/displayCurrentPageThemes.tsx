export function displayCurrentPageThemes(widget:any, currentPage: number, themesPerPage: number, showThemes: any[]) {
    const themesContainer = widget.node.querySelector('#themes-container');
    if (!themesContainer) return;

    // Separate sticky and non-sticky themes
    const stickyThemes = showThemes.filter(theme => theme.Sticky);
    const nonStickyThemes = showThemes.filter(theme => !theme.Sticky);

    // Sort both lists by creation time (newest first)
    stickyThemes.sort((b, a) => new Date(b.CreationTime).getTime() - new Date(a.CreationTime).getTime());
    nonStickyThemes.sort((a, b) => new Date(b.CreationTime).getTime() - new Date(a.CreationTime).getTime());

    // Combine the lists with sticky themes first
    const sortedThemes = [...stickyThemes, ...nonStickyThemes];

    const start = (currentPage - 1) * themesPerPage;
    const end = start + themesPerPage;
    const currentThemes = sortedThemes.slice(start, end);

    themesContainer.innerHTML = currentThemes.map((theme: any) => `

        <div class="subforum-row ${theme.Sticky ? 'sticky' : ''}">
            ${theme.Sticky ? '<div class="sticky-symbol">📌</div>' : ''}
            <div class="subforum-description subforum-column">
                <h4><a href="#" class="description-link" data-description-id="${theme.ThemeID}">${theme.Title}</a></h4>
                <p>Created at ${new Date(theme.CreationTime).toLocaleString()}</p>
            </div>
            <div class="subforum-info subforum-column">
                <p>
                  Posted by ${theme.Author}
                </p>
                <p class="status-indicator">
                  <span class="status-circle ${theme.Status === 'Open' ? 'status-open' : 'status-closed'}"></span>
                  Status: ${theme.Status}
                </p>
            </div>
        </div>
        <hr class="subforum-devider" />

    `).join('');
}

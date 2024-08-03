import { Widget } from '@lumino/widgets';
import { ShowThemeDetail } from './showthemedetail';
import { handleCreateThemeClick } from './forumdashboard/CreateTheme';
import {fetchAndDisplayThemes} from './forumdashboard/fetchAndDisplayThemes'
import {displayCurrentPageThemes} from './forumdashboard/displayCurrentPageThemes'
import {updatePaginationControls} from './forumdashboard/updatePaginationControls'

export class ForumDashboardWidget extends Widget {

    private originalHTML: string; // Declare the property
    private activeTab: string = 'all'; // Track the active tab
    private currentPage: number = 1; // Track the current page
    private themesPerPage: number = 5; // Maximum number of themes per page
    private allThemes: any[] = []; // Store all themes
    private showThemes: any[] = []; // Store all themes

    constructor(private username: string, private forumEndpointUrl: string) {
        super();
        this.addClass('forumWidget');
        this.originalHTML = `

            <div class="subforum">
              <div class="subforum-title">
                <h2>Current Themes </h2>
                <div class="tabs">
                  <div class="tab-group">
                    <button class="tab" data-tab="All">All</button>
                    <button class="tab" data-tab="Open">Open</button>
                    <button class="tab" data-tab="Closed">Closed</button>
                  </div>
                </div>

                <div class="search-container">
                  <input type="text" id="searchBox" placeholder="Search themes...">
                </div>

                <div class="actions-container">
                  <button class="create-theme-button" id="createThemeButton"><strong>+</strong> New Theme</button>
                </div>
              </div>
              <div id="themes-container"></div>
              <div id="pagination-controls" class="pagination-controls"></div>
            </div>

            `;
        this.node.innerHTML = this.originalHTML; // Set initial HTML

        fetchAndDisplayThemes(this, forumEndpointUrl);

        // Event listener
        this.node.addEventListener('click', (event) => {
            const target = event.target as HTMLElement; // Get the clicked element

            if (target.classList.contains('create-theme-button')) {
              handleCreateThemeClick(this, this.username, this.forumEndpointUrl);
            }

            if (target.classList.contains('tab')) {
              this.activeTab = target.dataset.tab ?? 'Open'; // Default to 'open' if undefined
              this.currentPage = 1
              this.updateTabDisplay();
            }

            if (target.classList.contains('description-link')) { // Check if it's the correct link
                const ThemeID = target.getAttribute('data-description-id');
                event.preventDefault(); // Prevent default link behavior
                ShowThemeDetail(this, ThemeID, this.forumEndpointUrl, username);
            }

            if (target.classList.contains('page-link')) { // Page navigation link
                this.currentPage = parseInt(target.dataset.page ?? '1', 10);
                displayCurrentPageThemes(this, this.currentPage, this.themesPerPage, this.showThemes);
            }
        });
    }

    private updateTabDisplay() {
      // Filter the themes based on their status
      this.showThemes = this.allThemes.filter(theme => {
          return this.activeTab === 'All' || theme.Status === this.activeTab;
      });

      displayCurrentPageThemes(this, this.currentPage, this.themesPerPage, this.showThemes);
      updatePaginationControls(this, this.allThemes.length, this.themesPerPage);
    }

}

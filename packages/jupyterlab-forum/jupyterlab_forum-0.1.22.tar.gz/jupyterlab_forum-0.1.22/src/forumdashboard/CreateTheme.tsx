import { ShowThemeDetail } from '../showthemedetail';
import { PageConfig } from '@jupyterlab/coreutils';
import {fetchAndDisplayThemes} from '../forumdashboard/fetchAndDisplayThemes'
import {initializeQuill} from './initializeQuill'


export async function handleCreateThemeClick(widget: any, username: string, forumEndpointUrl : string) {
  // Temporary HTML for theme creation form
  const createThemeFormHTML = `

  <div class="create-theme-form">
    <div class="form-group">
      <label for="themeTitle">Title:</label>
      <input type="text" id="themeTitle" name="themeTitle" required>
    </div>
    <div class="form-group">
      <label for="themeDescription">Description:</label>
      <div id="themeDescription" name="quill-editor"></div>
    </div>
    <button id="submitThemeButton" class="btn btn-secondary"">
      <strong>+</strong> Create Theme
    </button>
    <button id="back-to-forum" class="btn btn-primary">Back to Forum</button>
  </div>
  `;

  widget.node.innerHTML = createThemeFormHTML; // Update widget's HTML

  const quill = initializeQuill(widget)

  const backButton = widget.node.querySelector('#back-to-forum');
  backButton?.addEventListener('click', () => {
      widget.node.innerHTML = widget.originalHTML;
      fetchAndDisplayThemes(widget, forumEndpointUrl);
  });

  // Event listener for "Create" button
  const submitThemeButton = widget.node.querySelector('#submitThemeButton');
  if (submitThemeButton) {
    submitThemeButton.addEventListener('click', async () => {
          const titleInput = widget.node.querySelector('#themeTitle') as HTMLInputElement;
          const descriptionInput = quill.root.innerHTML;
          const token = PageConfig.getToken();

          const newTheme = {
            Title: titleInput.value,
            Description: descriptionInput,
            Author: username,
            Status: "Open",
            Sticky: false,
            Commentable : true
            // Add other relevant fields (e.g., Author, CreationTime)
          };

          try {
            // Send theme data to the server (e.g., using fetch)
            const response = await fetch(forumEndpointUrl + "createtheme", {
              method: 'POST',
              body: JSON.stringify(newTheme),
              headers: { 'Content-Type': 'application/json',
                         'Authorization': `token ${token}`,
                       },
            });

            if (response.ok) {
              // Theme created successfully
              // Optionally: Get the new theme ID from the response (if the server provides it)
              const data = await response.json();
              const newThemeId = data.ThemeID;

              ShowThemeDetail(widget, newThemeId, forumEndpointUrl, username); // Show the details of the new theme
            } else {
              // Handle errors here (e.g., display an error message in the widget)
              console.error('Failed to create theme:', response.status);
            }
          } catch (error) {
            console.error('Error creating theme:', error);
            // Handle errors here (e.g., display an error message in the widget)
          }
    });
  }

}

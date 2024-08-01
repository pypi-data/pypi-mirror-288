import{handleReplyToTheme} from './themedetail/replytheme';
import{fetchGroupData} from './themedetail/getgroupinfo';
import { PageConfig } from '@jupyterlab/coreutils';
import {fetchAndDisplayThemes} from './forumdashboard/fetchAndDisplayThemes';
import {initializeQuill} from './forumdashboard/initializeQuill'

export async function ShowThemeDetail(widget: any, ThemeID: any, forumEndpointUrl: string, username: string) {

    const token = PageConfig.getToken();

    try {
        const grouplist = await fetchGroupData( forumEndpointUrl)

        // Make a POST request to retrieve the theme details
        const response = await fetch(forumEndpointUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `token ${token}`,
            },
            body: JSON.stringify({ ThemeID: ThemeID }),
        });

        const themeDetail = await response.json();

        // Update the widget's HTML to display the theme details
        widget.node.innerHTML = `
          <div class="topic">
            <div class="topic-header">
              <h2 class="topic-title">${themeDetail.Title}</h2>
              <div class="topic-meta">
                <span class="topic-author">by ${themeDetail.Author}</span>
                <span class="topic-date">${new Date(themeDetail.CreationTime).toLocaleString()}</span>
              </div>
            </div>

            <div class="topic-body">
              <div class="topic-content">${themeDetail.Description}</div>
              <div class="topic-stats">
                <span>${themeDetail.Replies.length} Replies</span> •
              </div>
            </div>

            <div class="topic-replies">
              <h3>Replies:</h3>
              <div class="replies-container">  </div>
            </div>

            ${(themeDetail.Commentable) ? `
              <div class="form-group">
                <label for="themeDescription">Your Reply:</label>
                <div id="themeDescription" name="quill-editor"></div>
                <button id="reply-to-theme" class="btn btn-reply">Commit Reply</button>
              </div>
            ` : ''}

            <button id="back-to-forum" class="btn btn-primary">Back to Forum</button>
            ${(username === themeDetail.Author || grouplist.includes(username)) && !themeDetail.Sticky ? `
              <button id="toggle-status" class="btn btn-secondary">${themeDetail.Status === 'Open' ? 'Close' : 'Open'} Theme</button>
              <button id="delete-theme" class="btn btn-danger">Delete Theme</button>
            ` : ''}
          </div>
        `;

        // Insert replies into replies-container
        const repliesContainer = widget.node.querySelector('.replies-container');
        themeDetail.Replies.forEach((reply: any) => {
            const replyDiv = document.createElement('div');
            replyDiv.className = 'reply';
            replyDiv.innerHTML = `
              <div class="reply-header">
                <span class="reply-author">${reply.Author}</span>
                <span class="reply-date">${new Date(reply.CreationTime).toLocaleString()}</span>
              </div>
              <div class="reply-content">${reply.Content}</div>
            `;
            repliesContainer?.appendChild(replyDiv); // Add the reply div to the container
          });


          if (themeDetail.Commentable === true) {
              const quill = initializeQuill(widget);
              // Event listener for reply button
              const replyButton = widget.node.querySelector('#reply-to-theme');
              replyButton?.addEventListener('click', () => {
                  handleReplyToTheme(widget, username, ThemeID, forumEndpointUrl, quill.root.innerHTML);
              });
          }


          // Event listener for toggle status button
          const toggleStatusButton = widget.node.querySelector('#toggle-status');
          if (toggleStatusButton) {
              toggleStatusButton.addEventListener('click', async () => {
                  try {
                      const newStatus = themeDetail.Status === 'Open' ? 'Closed' : 'Open';
                      const response = await fetch(`${forumEndpointUrl}/togglestatus`, {
                          method: 'PATCH',
                          headers: {
                              'Content-Type': 'application/json',
                              'Authorization': `token ${token}`,
                          },
                          body: JSON.stringify({ ThemeID: ThemeID, Status: newStatus }),
                      });

                      if (response.ok) {
                          ShowThemeDetail(widget, ThemeID, forumEndpointUrl, username); // Refresh the theme detail
                      } else {
                          console.error('Failed to toggle status:', response.status);
                      }
                  } catch (error) {
                      console.error('Error toggling status:', error);
                  }
              });
          }

          const backButton = widget.node.querySelector('#back-to-forum');
          backButton?.addEventListener('click', () => {
              widget.node.innerHTML = widget.originalHTML;
              fetchAndDisplayThemes(widget, forumEndpointUrl);
          });


          // Event listener for delete button
          const deleteButton = widget.node.querySelector('#delete-theme');
          if (deleteButton) {
              deleteButton.addEventListener('click', async () => {
                const userConfirmed = window.confirm("Are you sure you want to delete this theme?");
                if (!userConfirmed) {
                  return; // User cancelled the deletion
                }

                  try {
                      const response = await fetch(`${forumEndpointUrl}/deletetheme`, {
                          method: 'DELETE',
                          headers: {
                              'Content-Type': 'application/json',
                              'Authorization': `token ${token}`,
                          },
                          body: JSON.stringify({ ThemeID: ThemeID }),
                      });

                      if (response.ok) {
                          widget.node.innerHTML = widget.originalHTML;
                          fetchAndDisplayThemes(widget, forumEndpointUrl);
                      } else {
                          console.error('Failed to delete theme:', response.status);
                      }
                  } catch (error) {
                      console.error('Error deleting theme:', error);
                  }
              });
          }


    } catch (error) {
        console.error('Error fetching theme details:', error);
        // Example theme data
        const themeDetail = {
          Title: "Example Theme",
          Description: "This is an example theme description.",
          Author: "User123",
          CreationTime: "2024-07-24T10:08",
          Status: "Open",
          Sticky: 0,
          Commentable : 1,
          Replies: [
            { Author: "Example Author2", Content: "This is an example reply to the theme2.", CreationTime: "2024-07-22T10:08" },
            { Author: "Example Author", Content: "This is an example reply to the theme.", CreationTime: "2024-07-24T10:08" },
          ]
        };

        // Update the widget's HTML to display the theme details
        widget.node.innerHTML = `
          <div class="topic">
            <div class="topic-header">
              <h2 class="topic-title">${themeDetail.Title}</h2>
              <div class="topic-meta">
                <span class="topic-author">by ${themeDetail.Author}</span>
                <span class="topic-date">${new Date(themeDetail.CreationTime).toLocaleString()}</span>
              </div>
            </div>

            <div class="topic-body">
              <div class="topic-content">${themeDetail.Description}</div>
              <div class="topic-stats">
                <span>${themeDetail.Replies.length} Replies</span> •
              </div>
            </div>

            <div class="topic-replies">
              <h2>Replies:</h2>
              <div class="replies-container">  </div>
            </div>

            ${(themeDetail.Commentable ) ? `
              <div class="form-group">
                <label for="themeDescription">Your Reply:</label>
                <div id="themeDescription" name="quill-editor"></div>
                <button id="reply-to-theme" class="btn btn-reply">Commit Reply</button>
              </div>
            ` : ''}

            <button id="back-to-forum" class="btn btn-primary">Back to Forum</button>


            ${(!themeDetail.Sticky) ? `
              <button id="delete-theme" class="btn btn-danger">Delete Theme</button>
              <button id="toggle-status" class="btn btn-secondary">${themeDetail.Status === 'Open' ? 'Close' : 'Open'} Theme</button>
            ` : ''}

          </div>
        `;


        const backButton = widget.node.querySelector('#back-to-forum');
        backButton?.addEventListener('click', () => {
            widget.node.innerHTML = widget.originalHTML;
            fetchAndDisplayThemes(widget, forumEndpointUrl);
        });

        // Insert replies into replies-container
        const repliesContainer = widget.node.querySelector('.replies-container');
        themeDetail.Replies.forEach((reply: any) => {
            const replyDiv = document.createElement('div');
            replyDiv.className = 'reply';
            replyDiv.innerHTML = `
              <div class="reply-header">
                <span class="reply-author">${reply.Author}</span> •
                <span class="reply-date">${new Date(reply.CreationTime).toLocaleString()}</span>
              </div>
              <div class="reply-content">${reply.Content}</div>
            `;
            repliesContainer?.appendChild(replyDiv); // Add the reply div to the container
          });

          if (themeDetail.Commentable === 1) {
              const quill = initializeQuill(widget);
              // Event listener for reply button
              const replyButton = widget.node.querySelector('#reply-to-theme');
              replyButton?.addEventListener('click', () => {
                  handleReplyToTheme(widget, username, ThemeID, forumEndpointUrl, quill.root.innerHTML);
              });
          }

        // Event listener for toggle status button
        const toggleStatusButton = widget.node.querySelector('#toggle-status');
        if (toggleStatusButton) {
            toggleStatusButton.addEventListener('click', async () => {
                try {
                    const newStatus = themeDetail.Status === 'Open' ? 'Closed' : 'Open';
                    const response = await fetch(`${forumEndpointUrl}/togglestatus`, {
                        method: 'PATCH',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ ThemeID: ThemeID, Status: newStatus }),
                    });

                    if (response.ok) {
                        ShowThemeDetail(widget, ThemeID, forumEndpointUrl, username); // Refresh the theme detail
                    } else {
                        console.error('Failed to toggle status:', response.status);
                    }
                } catch (error) {
                    console.error('Error toggling status:', error);
                }
            });
        }


        // Event listener for delete button
        const deleteButton = widget.node.querySelector('#delete-theme');
        if (deleteButton) {
            deleteButton.addEventListener('click', async () => {
              const userConfirmed = window.confirm("Are you sure you want to delete this theme?");
              if (!userConfirmed) {
                return; // User cancelled the deletion
              }

                try {
                    const response = await fetch(`${forumEndpointUrl}/deletetheme`, {
                        method: 'DELETE',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `token ${token}`,
                        },
                        body: JSON.stringify({ ThemeID: ThemeID }),
                    });

                    if (response.ok) {
                        widget.node.innerHTML = widget.originalHTML;
                        fetchAndDisplayThemes(widget, forumEndpointUrl);
                    } else {
                        console.error('Failed to delete theme:', response.status);
                    }
                } catch (error) {
                    console.error('Error deleting theme:', error);
                }
            });
        }


      }

}
